## ADDED Requirements

### Requirement: Builder-facing actuator control

The complete actuator SHALL expose exactly one builder-facing driver named `input_angle`, expressed in degrees over -2880 through +2880 degrees, with all other motion derived from it.

#### Scenario: Maker changes the input angle

- **WHEN** the maker sets `input_angle` to any supported value
- **THEN** the motor rotor, sun, planets, carrier, output-side bearing envelope, and encoder magnet holder assume the uniquely derived mechanically coherent pose

### Requirement: Compact deterministic demonstration

The actuator SHALL provide `Home`, `One Motor Turn`, and `One Output Turn` instructions with finite durations consistent with a 360-degree-per-second inspection speed, and each instruction SHALL land exactly on its target.

#### Scenario: Run every instruction

- **WHEN** a scenario triggers `Home`, `One Motor Turn`, `One Output Turn`, and `Home` in sequence
- **THEN** the driver lands exactly at 0, 360, 2880, and 0 degrees respectively and the rigid-part integrity contract holds on the sampled path

### Requirement: Published model is inspectable

The default build SHALL publish the full actuator with material-distinguishing colours, the driver and instructions, and valid model files for every rigid leaf.

#### Scenario: Inspect the finite build

- **WHEN** `solid build` succeeds
- **THEN** `viewer.json` contains the complete fixed, input, planet, and output groups, the `input_angle` driver, all three instructions, symbolic motion operations, and an existing model file for every rigid leaf

### Requirement: Visual evidence covers rest and motion

The project SHALL retain no generated snapshots in Git but SHALL document inspected isometric and axial snapshots at home and at a driven pose.

#### Scenario: Review generated snapshots

- **WHEN** the documented snapshot commands are run
- **THEN** the home and driven images show one coherent actuator, three evenly spaced planets, fixed housing geometry, and output motion about the common axis
