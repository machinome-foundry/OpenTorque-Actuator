## 1. Project and source evidence

- [ ] 1.1 Add `pyproject.toml` with the `simulation.actuator:OpenTorqueActuator` model and builder profile, create the importable package, and ignore build/snapshot artefacts while leaving every upstream file untouched.
- [ ] 1.2 Add `simulation/tools/probe.py`; record merged STL connectivity, bounds, volumes, tooth-frequency evidence, STEP occurrence readings, source fingerprints, and catalogue citations in `docs/measurements.md`.
- [ ] 1.3 Generate the STEP product scaffold with `solid import-step`, reduce it to project-owned named `StepNode` selections with source-relative paths and material colours, and make the root render the first fixed shell subassembly.

## 2. Output stack

- [ ] 2.1 Write output-stack contracts first for named STEP products, axial order, coaxiality, connected rigid bodies, and source fingerprint drift; run them faceted and retain the expected red evidence.
- [ ] 2.2 Implement the fixed housing/backplate/retainer/encoder-cover group, moving three-piece carrier and encoder-magnet group, and connected catalogue-dimension envelopes for compound or absent bought hardware until the output-stack contracts pass faceted.
- [ ] 2.3 Mutate one carrier axial placement beyond its measured seat margin, confirm the coaxial/seat contract fails, restore the source placement, and record the mutation result here.

## 3. Planetary reducer

- [ ] 3.1 Write reducer contracts first for the 18/54/126 tooth evidence, 27 mm planet radius, 120-degree spacing, home phase, pin/bearing coaxiality, and the 8:1/planet-spin relations; run them faceted and retain the expected red evidence.
- [ ] 3.2 Implement the sun input group and three orbiting planet units from the STEP-selected sun/planet geometry, bearings, and pins; bind all motion through ports and make the reducer contracts pass faceted.
- [ ] 3.3 Mutate the carrier ratio and one planet-center placement in node code, confirm the ratio and seating contracts fail respectively, restore both, and record any structural blind spot here.

## 4. Actuator control and scenarios

- [ ] 4.1 Write root contracts first for exactly one `input_angle` driver, all three instruction targets/durations, complete port binding, connected solids, and rigid-part interference over the named-motion scenario; run them faceted and retain the expected red evidence.
- [ ] 4.2 Implement the motor/encoder envelopes, root driver, derived fixed/input/planet/output motion, `Home`, `One Motor Turn`, and `One Output Turn` instructions, and material-based colours until all root and scenario contracts pass faceted.
- [ ] 4.3 If upstream seated geometry overlaps, add `simulation/seats.py` with the exact pair-and-volume inventory and make both changed and newly introduced overlap fail without an epsilon.
- [ ] 4.4 Mutate the output-ratio sign and remove one root port binding, confirm the scenario/ratio and wiring contracts fail, restore both, and record any contract blind spot here.

## 5. Verification and project record

- [ ] 5.1 Run the faceted full regression separately for every simulation node file, including the root, with no warning from a touched class.
- [ ] 5.2 Run `solid build`; inspect `viewer.json` for the fixed/input/planet/output tree, symbolic operations, one driver, three instructions, piece inventory, and existence of every rigid model file.
- [ ] 5.3 Render and inspect home and driven snapshots in isometric and axial views with the default renderer, then remove the generated images.
- [ ] 5.4 Extend `README.md` with exact build/test/snapshot commands, driver and instruction meanings, ground-up models, source/catalogue boundary, limitations, and measured findings.
- [ ] 5.5 Run the exact full regression once for every node file, record the certified result and tested source fingerprint, and leave the default build green.
- [ ] 5.6 Fill `Purpose` in every capability spec, sync the delta specs, validate and archive `simulate-the-opentorque-actuator`, then commit the completed simulation record inside the OpenTorque repository.
