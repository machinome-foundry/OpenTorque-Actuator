# OpenTorque Actuator

Licensing: Gabrael Levine's design and source-derived Foundry material retain
CC-BY-SA-4.0. Original Foundry loaders and helpers have a scoped
AGPL-3.0-or-later grant. See [CREDITS](CREDITS), [NOTICE](NOTICE) and
[simulation/README.md](simulation/README.md) for attribution and the file map.

### A powerful, compliant actuator for legged robotics.

![Exploded view](https://github.com/G-Levine/OpenTorque-Actuator/blob/master/images/exploded_view.png)

## Simulation

The additive `simulation/` package turns the released STEP assembly into a
rigid, inspectable solid-node machine. It leaves every original STEP, STL,
image, BOM, print instruction, and licence file unchanged.

From this repository, using the LibreSolid Studio workspace environment:

```sh
/home/asa/devel/libresolid-studio/.venv/bin/solid build
/home/asa/devel/libresolid-studio/.venv/bin/solid test --faceted simulation/parts.py
/home/asa/devel/libresolid-studio/.venv/bin/solid test --faceted simulation/hardware.py
/home/asa/devel/libresolid-studio/.venv/bin/solid test --faceted simulation/output_stack.py
/home/asa/devel/libresolid-studio/.venv/bin/solid test --faceted simulation/reducer.py
/home/asa/devel/libresolid-studio/.venv/bin/solid test --faceted simulation/actuator.py
```

Omit `--faceted` for the slower exact-kernel certification. `solid build`
publishes `_build/viewer.json`; a solid-node viewer presents the model's one
driver and three demonstration buttons.

### Controls and demonstration

`input_angle` is motor/sun rotation about the STEP assembly's +Z axis, in
degrees, from -2880 through +2880. The fixed-ring reducer derives carrier and
output rotation as `input_angle / 8`; each planet spins by
`-7 * input_angle / 24` in its orbiting carrier frame. No independently
drivable internal joint can create an impossible pose.

| Instruction | Target | Duration |
| --- | ---: | ---: |
| Home | 0° | 8 s |
| One Motor Turn | 360° | 1 s |
| One Output Turn | 2880° | 8 s |

Useful ground-up models are
`simulation.output_stack:OutputStackPreview`,
`simulation.reducer:ReducerPreview`, and finally the manifest's
`simulation.actuator:OpenTorqueActuator`.

### Reproduce the visual evidence

The snapshot-only previews map normalized time 0→1 to one motor turn. They do
not add another control to the published actuator. The following commands
produce the four reviewed images; generated PNGs are intentionally ignored and
not retained in Git.

```sh
/home/asa/devel/libresolid-studio/.venv/bin/solid snapshot simulation/actuator.py:ActuatorPosePreview --time 0 -o snapshot-home-iso.png --autocenter --viewall --camera 0,0,26,55,0,35,220 --imgsize 1200x900 --projection ortho --render
/home/asa/devel/libresolid-studio/.venv/bin/solid snapshot simulation/actuator.py:ActuatorPosePreview --time 1 -o snapshot-driven-iso.png --autocenter --viewall --camera 0,0,26,55,0,35,220 --imgsize 1200x900 --projection ortho --render
/home/asa/devel/libresolid-studio/.venv/bin/solid snapshot simulation/reducer.py:ReducerPosePreview --time 0 -o snapshot-home-axial.png --autocenter --viewall --camera 0,0,50,0,0,0,130 --imgsize 900x900 --projection ortho --render
/home/asa/devel/libresolid-studio/.venv/bin/solid snapshot simulation/reducer.py:ReducerPosePreview --time 1 -o snapshot-driven-axial.png --autocenter --viewall --camera 0,0,50,0,0,0,130 --imgsize 900x900 --projection ortho --render
```

The isometric pair shows one coherent closed actuator and the carrier/output
plate advancing 45°. The axial reducer pair exposes the otherwise hidden three
planets at 120° spacing and their 45° orbit.

### What the model found

- The assembled standard gears measure 18 sun teeth and 54 planet teeth. The
  implied fixed ring has 126 teeth, producing the 8:1 reduction.
- The source gears are not zero-volume contacts. At home the exact kernel finds
  about 23.615 mm³ between each planet and the housing ring, and
  10.228–10.241 mm³ between each planet and the sun. These are retained as
  named, bounded overlaps rather than silently repaired.
- The connected bought-hardware envelopes create additional reviewed capture
  interfaces: the retainer/outer race, both carrier plates/planet bearings, and
  each planet bearing/gear. `simulation/seats.py` requires exactly the 16 known
  pairs and fails for a new, removed, or out-of-range overlap with no global
  volume epsilon.
- The BOM's Multistar 9235 and X8318S alternative motors have different
  published envelopes, so the simulation uses the primary 92 mm Multistar can
  only as a visual stand-in and makes no interchangeability claim.
- The current workspace CLI can scaffold the STEP with `solid import-step`, but
  the documented `StepAssembly` import is absent. Named `StepNode` selections
  are used instead.

Detailed source readings, fingerprints, catalogue links, and kernel-specific
overlap volumes are in [docs/measurements.md](docs/measurements.md). The
simulation does not predict torque, compliance, backlash under load,
efficiency, bearing life, thermal or electromagnetic behaviour, firmware
response, printability, strength, or safety.
