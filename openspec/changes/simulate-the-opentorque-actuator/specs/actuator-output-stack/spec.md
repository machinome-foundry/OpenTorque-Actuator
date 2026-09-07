## ADDED Requirements

### Requirement: Source geometry remains authoritative

The simulation SHALL select supplied printed parts from `STEP/opentorque.step` without modifying their geometry and SHALL keep the upstream STEP, STL, image, BOM, print, and licence files unchanged.

#### Scenario: Build from the released design

- **WHEN** the actuator model is built
- **THEN** every supplied printed component resolves to its named STEP product and the build records the STEP document as its geometry source

### Requirement: Coaxial output support

The housing, carrier, cross-roller bearing, backplate, and encoder-side stack SHALL share the STEP-defined actuator axis and axial order, with a moving output side and a fixed housing side.

#### Scenario: Output rotates in its seat

- **WHEN** `input_angle` advances through its supported range
- **THEN** the carrier, output-side bearing envelope, and encoder magnet holder remain coaxial within 0.01 mm while the housing, backplate, bearing retainer, and encoder cover remain fixed

### Requirement: Planet hardware remains seated

Each planet gear SHALL remain centred on its STEP-defined M5x30 pin and 625 bearing throughout the carrier orbit.

#### Scenario: Planet unit follows the carrier

- **WHEN** the carrier advances through one output revolution
- **THEN** each planet gear, pin, and bearing axis follows the same 27 mm-radius orbit and their mutual radial-axis offset remains within 0.01 mm

### Requirement: Rigid assembly integrity is explicit

Every represented rigid component SHALL be one connected body, and the complete actuator SHALL have no positive-volume rigid overlap except an exact, named inventory of overlaps already present in the upstream assembled design.

#### Scenario: Integrity at every named pose

- **WHEN** the actuator is evaluated at home, one motor turn, and one output turn
- **THEN** every rigid component is connected and the intersection pair set and volumes match the recorded source-seat inventory exactly

### Requirement: Source measurements cannot drift silently

The project SHALL retain a reproducible probe and recorded readings for source frames, bounds, volumes, connectivity, gear counts, and STEP occurrence layout, and SHALL fail its drift contract when the source fingerprint changes without review.

#### Scenario: Upstream geometry changes

- **WHEN** a supplied STEP or STL changes after measurements were accepted
- **THEN** the source-drift contract fails and identifies the changed source before the simulation can be certified
