## Context

The repository is a CC BY-SA 4.0 mechanical release, not a Python project. It contains one assembled STEP document (`STEP/opentorque.step`), one STEP document for low-backlash gear variants, separately exported printable STLs, an exploded image, print instructions, and a BOM. There are no tests, kinematic tables, firmware constants, or assembly instructions beyond those sources.

The main STEP document is the assembly source of truth. Its products are the actuator housing, bearing retainer, three carrier pieces, backplate, encoder cover and magnet holder, RA-8008C cross-roller bearing, sun, planet, F625ZZ bearing, and M5x30 pin. Its occurrence structure places the gear group 40 mm along the actuator axis; the three planet centers are at radius 27 mm and 120-degree intervals. The separate STL exports are print artefacts and use part-local print frames, so they are measurements and drift evidence rather than assembly-placement authority.

The source gear profiles have an 18-tooth sun and 54-tooth planets. A fixed-ring planetary with those centers requires 126 ring teeth and gives `carrier = input / 8`. The absolute planet spin is `-input / 6`; relative to its orbiting carrier it is `-7 * input / 24`.

Catalogue evidence fills only dimensions that the upstream BOM names but the STEP omits: the Multistar 9235 envelope is 92 mm diameter by 38 mm body length (22 mm rotating can), the X8318S alternate is 91.6 mm rotor diameter by 41 mm body length, the AS5048 adapter board is 22 by 28 mm with 2.6 mm mounting holes, the RA8008 is 80 by 96 by 8 mm, and a 625 bearing is 5 by 16 by 5 mm. The model will preserve conflicting motor alternatives as a finding and use the BOM's primary Multistar envelope for the visual stand-in.

## Coordinates

- The machine frame is the main STEP frame, in millimetres.
- `+Z` is the common motor, sun, carrier, output-bearing, and encoder axis. The origin remains the STEP origin; geometry is not rebased to a bounding-box corner.
- `input_angle` is positive rotation about `+Z`, measured in degrees at the motor can/sun.
- The fixed internal ring remains stationary. `output_angle = input_angle / 8` is the carrier and output rotation about `+Z`.
- Each planet center begins at its STEP occurrence position, orbits by `output_angle`, and the planet gear spins `-7 * input_angle / 24` in its carrier-local frame. Its absolute orientation is therefore `-input_angle / 6`.
- A named 0.05 mm seating witness separates faces used only to establish axial order; it is not added to tooth engagement or to dimensions already carrying source clearance.

## Goals / Non-Goals

**Goals:**

- Import every supplied printed part from the main STEP document without changing upstream geometry.
- Show the complete rigid actuator stack and the one mechanically meaningful input.
- Preserve source placement at home and derive every moving angle from the measured tooth counts.
- Make source assumptions, catalogue substitutions, and discovered interferences explicit and testable.
- Produce finite builds, exact and faceted contract runs, and visually inspected home and driven snapshots.

**Non-Goals:**

- Predict torque, stiffness, elastic compliance, backlash under load, efficiency, life, thermal behaviour, electromagnetic behaviour, or controller response.
- Assert printability, material strength, safety, or fitness for a legged robot.
- Replace the source's standard gears with the separate low-backlash variants in this change.
- Model every screw, insert, wire, or electronic component when it does not affect rigid kinematics or a tested seat.
- Modify, repair, re-export, or reformat any upstream STEP or STL.

## Decisions

### Select STEP products rather than importing printable STLs

`solid import-step` identifies the assembly products and occurrence transforms directly. `StepNode` keeps each selected product exact and tracks the STEP source. This is thinner and more faithful than reconstructing assembly placement from print-oriented STL bounding boxes. The alternative—`StlNode` for every export—would discard exact geometry and restate placements the STEP already knows.

### Separate fixed, input, planet, and output motion groups

The generated static assembly scaffold is reorganised without altering any selected product. Fixed shell pieces remain under the root; the sun and motor can receive input rotation; each planet is nested under an orbiting unit; and all three carrier pieces plus the output-side moving bearing envelope receive carrier rotation. This separation lets the root bind every motion absolutely. Leaving the generated assembly static would render the source pose but would not make it a machine.

### Use one input-angle driver

An actuator has one commanded mechanical input in this rigid model. The root declares `input_angle` over -2880 to +2880 degrees so the maker can inspect one output revolution in either direction. Exposing sun, planet, carrier, and bearing-race sliders separately would permit impossible states and obscure the reduction.

### Use the standard gear set from the assembled STEP

The main STEP is internally assembled around the standard sun and planet products. The low-backlash variants live in a separate STEP and have no complete occurrence tree. They remain available upstream but outside this first simulation. Mixing them into the assembly would silently choose an unrecorded configuration.

### Model absent purchased hardware only as mechanical envelopes

The motor and encoder board are absent from the STEP but named by the BOM. Simple CadQuery envelopes use catalogue dimensions, distinct rotor/stator bodies, and explicit radial clearance; they communicate placement and motion without pretending to reproduce vendor geometry. Fasteners and inserts remain omitted unless a contract needs their volume. The alternative—drawing recognisable vendor replicas—would add unlicensed detail and unsupported dimensions.

### Treat upstream overlaps as an inventory

The exact STEP may contain deliberate seated/contacting geometry or exported overlap. If the first full sweep finds positive-volume intersections, `simulation/seats.py` will record the exact pair set and measured volumes at home, and the contract will require that inventory rather than introduce a tolerance. A changed, added, or removed overlap then fails.

### Detect source drift with measurements and a source fingerprint

`simulation/tools/probe.py` will reproduce STL bounds, connectivity, volumes, tooth-frequency evidence, and STEP-scaffold occurrence readings. `docs/measurements.md` records its output and sources. Because the installed framework currently lacks the documented public `StepAssembly` import, the automated drift contract will pin the measured STEP fingerprint and layout table; a source change fails and requires the probe to be rerun and the design re-evaluated.

## Findings

- All printable STLs are watertight single bodies after coincident vertices are merged, but their raw files duplicate vertices; probing with processing disabled falsely reports thousands of bodies.
- The printable STL frames are not the assembly frame. For example, the planet gear is centred at its own origin while the STEP occurrence places it 27 mm from the actuator axis.
- The herringbone tooth trace has a half-count fundamental at the centre seam (9 lobes for the sun and 27 for the planet); the full tooth counts appear as the 18 and 54 harmonics. A tooth-count probe must record both rather than count naive radial maxima.
- The BOM treats Herlea X8318S and Multistar 9235 as alternatives, but their published envelopes and shaft descriptions differ. The simulation uses the BOM's primary Multistar envelope and makes no interchangeability claim.
- The current workspace `solid-node` command can import the STEP, but `StepAssembly` is not exported from `solid_node.node` as the public API skill describes. The implementation uses the supported CLI-generated scaffold and records this framework packaging discrepancy without inspecting framework source.

## Risks / Trade-offs

- **[Risk] The STEP product frames contain modelling-in-context offsets that are easy to double-apply.** → Build and inspect the generated scaffold first; preserve its occurrence operations verbatim and test the 27 mm planet centers in world coordinates.
- **[Risk] Exact herringbone meshes make scenario interference checks expensive.** → Use the faceted kernel for red/green work, sample named moves at physically meaningful intervals, and certify once on the exact kernel.
- **[Risk] Purchased-bearing STEP products may contain multiple disconnected solids.** → Represent moving/fixed bearing envelopes as separate connected nodes when necessary, retaining catalogue dimensions and source seats; do not weaken connectivity.
- **[Risk] Source gears may intentionally occupy zero-clearance mesh contact.** → Require zero positive-volume interference; if the source itself overlaps, inventory the measured pair and report it as a design finding.
- **[Risk] The motor envelope is not an exact model of either BOM alternative.** → Keep it visually distinct, dimension-labelled in documentation, and excluded from fine fit or performance claims.

## Migration Plan

Additive only: introduce the manifest, package, tests, measurements, and documentation; run the project from the workspace environment. Rollback is removal of those added files and the README section. No upstream geometry or build artefact is migrated.

## Open Questions

No pilot decision blocks this rigid first slice. Any discovered source interference that cannot be represented honestly without changing the upstream geometry returns to the pilot rather than being repaired here.
