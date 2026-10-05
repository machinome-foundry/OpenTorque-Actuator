# Internal mesh angle migration

Each planet's own orbit now drives its child-local spin through the common-frame
fixed-ring law:

```text
internal_mesh_angle(0, 126, 54, carrier) - carrier
```

The helper first gives the planet's absolute increment against the stationary
ring; subtracting the carrier increment converts it to the existing local
`PlanetGear.spin` frame. This is `-126/54 * carrier`, hence `-7/24 * sun` for
the retained `carrier = sun/8` reducer. All three orbit relations, +Z axes,
source phases, placements, controls, and output bindings are unchanged.
`simulation/kinematics.py` and `SUN_PLANET_MESH` deliberately retain the old
independent external-mesh derivation used by existing test oracles.

The mechanics source tested was the uncommitted `gears.py` at SHA-256
`d7433e1d8f7f9742ca5bd5da9118712d49365422dfda9d5d62a0a0798af3390b`
in `WTs/mechanics-internal-mesh-angle`; its planning HEAD was
`832252a98c6f44776ccef8817cf8034ba95dd392`.

## Actual relation comparison

The retained `scripts/check-internal-mesh-angle` probe independently derives
the carrier as `sun / (1 + 126/18)` and the old local planet spin as
`-(18/54) * (sun - carrier)`. On one actual `ReducerPreview` instance it
checks every planet's orbit, local spin and absolute orbit-plus-spin over
signed and unwrapped inputs. The sequence `10, 40, 0, 25` specifically retains
coverage of the project's former stale repeated-state regression. The probe
also evaluates all three actual bound mesh-law records with a supported
Solid2 animation-time expression.

Run it from the project root:

```console
PYTHONPATH="$PWD:/home/asa/devel/machinome-studio/WTs/mechanics-internal-mesh-angle" \
  /home/asa/devel/machinome-studio/.venv/bin/python \
  scripts/check-internal-mesh-angle
```

It reported `three actual numeric/deferred planet mesh laws match the
independent old relation`. The capped run passed in 3.48 s with maximum RSS
475,128 KiB and no swap. Its raw log is
`/tmp/opentorque-internal-mesh-probe.log`.

## CAD and pixel evidence

Every heavy command ran sequentially in a transient user scope with
`MemoryMax=768M`, `MemorySwapMax=0`, `RuntimeMaxSec=300`, and the BLAS/OpenMP
thread environment set to one:

```console
systemd-run --user --scope \
  -p MemoryMax=768M -p MemorySwapMax=0 -p RuntimeMaxSec=300 \
  env PYTHONPATH="$PWD:/home/asa/devel/machinome-studio/WTs/mechanics-internal-mesh-angle" \
  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  /usr/bin/time -v <command>
```

Results:

- `machinome test --mesh simulation/reducer.py`: 8/8 passed in 7.72 s,
  maximum RSS 591,060 KiB; log
  `/tmp/opentorque-internal-mesh-reducer-faceted.log`.
- `machinome test --brep simulation/reducer.py`: 8/8 passed in 3.42 s,
  maximum RSS 541,444 KiB; log
  `/tmp/opentorque-internal-mesh-reducer-exact.log`.
- `machinome test --mesh simulation/output_stack.py`: 6/6 passed, then
  `machinome test --mesh simulation/actuator.py`: 6/6 passed. The combined
  scope took 16.96 s with maximum RSS 572,220 KiB; log
  `/tmp/opentorque-internal-mesh-supporting-faceted.log`.
- `machinome build` passed, followed in the same scope by the snapshot below;
  together they took 11.11 s with maximum RSS 525,024 KiB. The log is
  `/tmp/opentorque-internal-mesh-build-image.log`.

The fresh nonzero axial image used:

```console
/home/asa/devel/machinome-studio/.venv/bin/machinome snapshot \
  simulation/reducer.py:ReducerPosePreview --renderer openscad --time 0.5 \
  -o _build/internal-mesh-angle-axial.png --autocenter --viewall \
  --camera 0,0,50,0,0,0,130 --imgsize 700x700 --projection ortho --render
```

At half a motor turn the image visibly shows three evenly spaced planets around
the sun, coherent bearing axes, and plausible tooth registration. The fixed
housing ring is intentionally absent from this ground-up preview, so pixels do
not independently certify ring contact; the actual bound-law probe and reducer
suites provide the motion evidence. The simulation's existing documented
limits on backlash, load, efficiency and bearing behavior remain unchanged.

The framework checkout remained clean at
`8d2bd71171be81f13ba5dd492851ed8b3a9ababb` and the viewer checkout remained
clean at `4355da1a7f64dacd7d86eb27dbdfdf7ced94598f` before and after validation.
The project manifest now records `machinome-mechanics` and Python 3.11 or newer;
the README accurately identifies mechanics as founded but not yet published
and uses its source checkout through explicit `PYTHONPATH`.
