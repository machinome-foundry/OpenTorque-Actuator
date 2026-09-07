## Why

The request is: “simulate Actuators/OpenTorque-Actuator”. The repository publishes printable geometry and an exploded view, but neither can show whether the sun, planets, fixed ring, carrier, output bearing, and encoder stack remain coherently assembled as the actuator turns.

## What Changes

- Add a thin `simulation/` package that selects geometry from the upstream STEP document without modifying or redrawing the supplied parts.
- Assemble the fixed housing, bearing stack, three-planet reducer, output carrier, backplate, and encoder-side parts in the source coordinate system, with catalogue-dimension stand-ins only for motion-relevant bought hardware absent from the STEP document.
- Expose one builder-facing `input_angle` driver in degrees. Derive the carrier/output rotation and each planet's spin from the measured 18/54/126-tooth planetary geometry and its fixed ring.
- Add a compact demonstration with `Home`, `One Motor Turn`, and `One Output Turn` instructions, material-based colours, and finite move durations.
- Add contracts for reducer placement and ratio, planet-pin/bearing seating, coaxial output support, connected printed solids, rigid-part interference throughout the demonstration, source drift, and deliberate geometry mutations.
- Document how to build, test, pose, and inspect the simulation, plus the measured design and framework findings.

## Capabilities

### New Capabilities

- `planetary-reduction`: The sun, three planets, fixed ring, and carrier preserve the source tooth counts, centers, phase relationship, and 8:1 input-to-output kinematics.
- `actuator-output-stack`: The printed carrier and housing parts, cross-roller bearing, planet bearings, pins, backplate, and encoder-side parts occupy their source-defined seats without unintended interference.
- `actuator-poses`: A maker can drive the actuator by input angle and run a small, deterministic set of named motions whose final states and integrity are testable.

### Modified Capabilities

None.

## Impact

- Adds `pyproject.toml`, the `simulation/` package, project-owned tests and measurements, and OpenSpec records.
- Extends `README.md` with simulation usage and findings.
- Depends on the workspace `solid-node` installation and uses the repository's CC BY-SA 4.0 STEP geometry in place; all existing STEP, STL, image, BOM, print, and licence files remain untouched.
- Excludes torque, elasticity/compliance, motor electromagnetics, thermal behaviour, controls/firmware, and manufacturing fitness because the upstream repository supplies no authoritative data from which to simulate them.
