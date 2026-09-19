# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
# Design: Gabrael Levine (G-Levine); source and modifications in root NOTICE.

"""Measure the upstream geometry without changing it.

Run with the workspace Python from the project root:

    /home/asa/devel/machinome-studio/.venv/bin/python simulation/tools/probe.py

The STEP occurrence report is obtained through the public ``machinome import-step``
command because the current workspace package does not export the documented
``StepAssembly`` helper from ``machinome.node``.
"""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import trimesh


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GEOMETRY_PATHS = tuple(sorted((PROJECT_ROOT / "STEP").glob("*.step"))) + tuple(
    sorted((PROJECT_ROOT / "STL").glob("*.stl"))
)
TOOTH_PROBES = {
    "STL/Sun Gear.stl": (9, 18),
    "STL/Planet Gear.stl": (27, 54),
    "STL/Sun Gear low backlash.stl": (9, 18),
    "STL/Planet Gear low backlash.stl": (27, 54),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_mesh(path: Path) -> trimesh.Trimesh:
    loaded = trimesh.load_mesh(path, process=True)
    if isinstance(loaded, trimesh.Scene):
        return loaded.dump(concatenate=True)
    return loaded


def mesh_reading(path: Path) -> dict[str, object]:
    mesh = load_mesh(path)
    return {
        "bounds_mm": np.round(mesh.bounds, 6).tolist(),
        "components_after_merge": len(mesh.split(only_watertight=False)),
        "volume_mm3": round(float(mesh.volume), 3),
        "watertight_after_merge": bool(mesh.is_watertight),
    }


def radial_harmonics(path: Path, frequencies: tuple[int, int]) -> dict[str, object]:
    mesh = load_mesh(path)
    mid_z = float((mesh.bounds[0, 2] + mesh.bounds[1, 2]) / 2)
    section = mesh.vertices[np.abs(mesh.vertices[:, 2] - mid_z) < 0.05]
    angles = np.mod(np.arctan2(section[:, 1], section[:, 0]), 2 * np.pi)
    radii = np.hypot(section[:, 0], section[:, 1])

    bin_count = 2048
    bins = np.floor(angles / (2 * np.pi) * bin_count).astype(int)
    envelope = np.full(bin_count, -np.inf)
    np.maximum.at(envelope, bins, radii)
    present = np.isfinite(envelope)
    indices = np.flatnonzero(present)
    envelope = np.interp(
        np.arange(bin_count),
        np.concatenate((indices - bin_count, indices, indices + bin_count)),
        np.tile(envelope[present], 3),
    )
    amplitudes = np.abs(np.fft.rfft(envelope - envelope.mean()))
    strongest = np.argsort(amplitudes[1:151])[-8:] + 1
    strongest = sorted(strongest, key=lambda index: amplitudes[index], reverse=True)

    return {
        "midplane_z_mm": round(mid_z, 6),
        "radial_range_mm": [round(float(radii.min()), 6), round(float(radii.max()), 6)],
        "expected_half_and_full_counts": list(frequencies),
        "expected_amplitudes": {
            str(index): round(float(amplitudes[index]), 3) for index in frequencies
        },
        "strongest_frequencies": [
            [int(index), round(float(amplitudes[index]), 3)] for index in strongest
        ],
    }


def literal(node: ast.AST) -> object:
    return ast.literal_eval(node)


def step_occurrence_reading() -> dict[str, object]:
    interpreter_solid = Path(sys.executable).with_name("solid")
    solid = str(interpreter_solid) if interpreter_solid.is_file() else shutil.which("solid")
    if solid is None:
        raise RuntimeError("solid is not on PATH; activate the workspace environment")

    with tempfile.TemporaryDirectory(prefix="opentorque-step-probe-") as temporary:
        command = [
            solid,
            "import-step",
            str(PROJECT_ROOT / "STEP" / "opentorque.step"),
            "--into",
            temporary,
            "--model",
            "OpenTorque",
        ]
        subprocess.run(command, cwd=PROJECT_ROOT, check=True, capture_output=True, text=True)
        tree = ast.parse((Path(temporary) / "assembly.py").read_text())

    classes: dict[str, object] = {}
    for class_node in (node for node in tree.body if isinstance(node, ast.ClassDef)):
        children: dict[str, list[list[object]]] = {}
        for statement in class_node.body:
            if not isinstance(statement, ast.FunctionDef) or statement.name != "render":
                continue
            for child_statement in statement.body:
                if not isinstance(child_statement, ast.Expr):
                    continue
                call = child_statement.value
                if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Attribute):
                    continue
                target = call.func.value
                if not isinstance(target, ast.Attribute) or not isinstance(target.value, ast.Name):
                    continue
                if target.value.id != "self" or call.func.attr not in {"rotate", "translate"}:
                    continue
                arguments = [literal(argument) for argument in call.args]
                children.setdefault(target.attr, []).append([call.func.attr, *arguments])
        classes[class_node.name] = children
    return classes


def main() -> None:
    report = {
        "source_sha256": {
            str(path.relative_to(PROJECT_ROOT)): sha256(path) for path in GEOMETRY_PATHS
        },
        "stl": {
            str(path.relative_to(PROJECT_ROOT)): mesh_reading(path)
            for path in GEOMETRY_PATHS
            if path.suffix.lower() == ".stl"
        },
        "tooth_harmonics": {
            relative: radial_harmonics(PROJECT_ROOT / relative, frequencies)
            for relative, frequencies in TOOTH_PROBES.items()
        },
        "step_occurrence_operations": step_occurrence_reading(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
