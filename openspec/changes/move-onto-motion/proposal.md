# Move the OpenTorque simulation onto solid-node's motion layer

## Why

solid-node main integrated `solid_node.motion` (ADR-087..089): ports and
`Time` left `solid_node.node` with no re-export, so this project no longer
imports. `simulation/output_stack.py` and `simulation/reducer.py` both fail
at `from solid_node.node import AssemblyNode, RotationalPort` with the
framework's own instruction to import from `solid_node.motion.ports`.

Fixing the import alone would leave the machine stated the old way: three
`RotationalPort`s whose only job is to carry one angle down a level, five
`simulate()` methods that fan that angle out with hand-written `rotate()`
calls, and a planetary reduction that lives in `kinematics.py` as three
functions of the input angle rather than as the meshes it actually is.

The motion layer says what a body is FREE to do, once, next to the body,
and what drives what, as a sentence. This actuator is a good fit: every
freedom in it is a turn about a line the STEP already fixes, and the whole
machine is one train from the motor can to the output flange. Stated that
way the project loses all three ports, all five fan-out `simulate()` bodies
and the implicit reliance on innermost composition, and gains nine joints,
thirteen relations and three derived coordinates that read as the mechanism.

Nothing about the geometry, the placements or any pose changes.

## What changes

### The nine joints

All nine turn about the actuator's +Z axis or about a planet pin parallel
to it; `axis` and `at` are stated in the parent's frame, as the framework
requires. No joint declares a `range`: the machine turns without limit and
the builder-facing limits stay on the `input_angle` driver (±2880°, eight
motor turns). Every number below is already in `simulation/layout.py` or in
a `render()` this change does not touch.

| # | Class (file) | Joint | `axis` | `at`, in the parent's frame | Where the numbers come from |
|---|---|---|---|---|---|
| 1 | `MotorRotorEnvelope` (`hardware.py`) | `spin` | `(0, 0, 1)` | `(0, 0, 0)` — the machine axis | `OpenTorqueActuator.render()` places the can by `translate((0, 0, 13))`, which lies on that line; replaces `self.motor_rotor.rotate(self.input_angle, (0, 0, 1))` |
| 2 | `SunGear` (`parts.py`) | `spin` | `(0, 0, 1)` | `(0, 0, 0)` — the machine axis in `PlanetaryReducer`'s frame | `PlanetaryReducer.render()` places the sun by `translate((0, 0, GEAR_GROUP_Z))`, on that line; replaces `self.sun_gear.rotate(angle, (0, 0, 1))` |
| 3 | `PlanetUnit` (`reducer.py`) | `orbit` | `(0, 0, 1)` | `(0, 0, 0)` — the machine axis in `PlanetaryReducer`'s frame | this is the carrier's freedom; replaces `planet.rotate(carrier_angle, (0, 0, 1))`. The unit's own rest placement is `rotate(PLANET_PHASES[i], (0, 0, 1))` about the same line, so phase and orbit commute exactly as they do today |
| 4 | `PlanetGear` (`parts.py`) | `spin` | `(0, 0, 1)` | `(0, PLANET_RADIUS, GEAR_GROUP_Z + PLANET_GEAR_Z)` = `(0, 27, 41)` in `PlanetUnit`'s frame — the pin centre | exactly `PlanetUnit.render()`'s `translate((0, PLANET_RADIUS, GEAR_GROUP_Z + PLANET_GEAR_Z))`; `PLANET_RADIUS = 27.0` is read off the STEP and is asserted by `test_planet_bearing_and_pin_are_coaxial`. The Z component is immaterial to a Z-axis line and is written only so the anchor reads as the gear's own placed origin. This makes `parts.py` import `layout.py` (see Known gaps) |
| 5 | `PlanetCarrierA` (`parts.py`) | `turn` | `(0, 0, 1)` | `(0, 0, 0)` in `OutputStack`'s frame | placed by `translate((0, 0, 3 * SEAT_WITNESS))`, a pure Z offset on the axis; replaces its line in `OutputStack.simulate()` |
| 6 | `PlanetCarrierB` (`parts.py`) | `turn` | `(0, 0, 1)` | `(0, 0, 0)` | placed at the stack origin, unrotated; replaces its line in `OutputStack.simulate()` |
| 7 | `PlanetCarrierC` (`parts.py`) | `turn` | `(0, 0, 1)` | `(0, 0, 0)` | placed by `translate((0, 0, -SEAT_WITNESS))`; same |
| 8 | `EncoderMagnetHolder` (`parts.py`) | `turn` | `(0, 0, 1)` | `(0, 0, 0)` | placed at the stack origin; same |
| 9 | `CrossRollerInnerRace` (`hardware.py`) | `turn` | `(0, 0, 1)` | `(0, 0, 0)` | placed by `translate((0, 0, 62.5 + SEAT_WITNESS))`, on the axis; same |

Joints 5–9 are the one rigid output body, printed and bought in five
pieces. `test_source_axis_is_preserved` already asserts that every one of
them is centred on x=y=0, which is why `at` is the frame origin and why the
declaration is honest rather than a convenience.

### The one derived coordinate

**Orchestrator decision (review, 2026-09-09):** one derived coordinate, not
three. `sun_in_carrier` is stated once in `PlanetaryReducer`, against the
first planet's orbit, and drives all three planet gears — a coordinate may
be the source of several relations; only a driven end has a single binder
(`solid-node/docs/driving.rst`, "Passing a coordinate down"; Thor's
`art1.py` states `drive` once and reads it as the source of one relation,
and the same pattern here is one source read by three):

```python
sun_in_carrier = sun_gear.spin - planet_1.orbit
```

"The sun's angle seen from the carrier" is the frame a planetary mesh is
read in, and it is exactly what `kinematics.planet_relative_angle()`
computes today as `input_angle - output_angle(input_angle)`. Making it a
coordinate is what lets the mesh below be written as the one number the
tooth counts give, instead of the compound `-7/24` the current code hides
inside a function. All three planets carry the same orbit (driven by the
same `sun_gear.spin.drives(planet_N.orbit, ratio=CARRIER_RATIO)` sentence
below with the same law), so `planet_1.orbit` is exactly as valid a term as
`planet_2.orbit` or `planet_3.orbit` would be — reading any one of them
back out gives the same carrier angle at every pose.

### The thirteen `drives` sentences

Two ratios are added to `simulation/layout.py` beside the tooth counts they
come from, so each number is written once and both `kinematics.py` and the
relations read the same constant:

```python
CARRIER_RATIO = 1.0 / REDUCTION          # 0.125, and REDUCTION = 1 + 126/18 = 8.0
SUN_PLANET_MESH = -SUN_TEETH / PLANET_TEETH   # -18/54 = -1/3
```

`REDUCTION` is 8.0 exactly and `1/8` is exact in binary, so
`x * CARRIER_RATIO` and today's `x / REDUCTION` are bit-identical.

**`OpenTorqueActuator` (`actuator.py`) — 2 sentences.** The rotor's `spin`
IS the machine's drive coordinate, so no port is needed to hold it:

| Sentence | Both ends named | Law | Source of the numbers |
|---|---|---|---|
| `motor_rotor.spin.drives(reducer.sun_gear.spin)` | `MotorRotorEnvelope.spin` → `SunGear.spin` | ratio 1 (default `Affine`) | the sun is keyed to the rotor; today's `connect(self.input_angle, self.reducer.input_angle)` followed by `self.sun_gear.rotate(angle, ...)` |
| `motor_rotor.spin.drives(output_stack.planet_carrier_b.turn, ratio=CARRIER_RATIO)` | `MotorRotorEnvelope.spin` → `PlanetCarrierB.turn` | `ratio=0.125` | fixed 126-tooth ring, 18-tooth sun: `REDUCTION = 1 + RING_TEETH/SUN_TEETH = 8`; today's `connect(output_angle(self.input_angle), self.output_stack.output_angle)`. Asserted by `test_fixed_ring_planetary_relations` |

**`PlanetaryReducer` (`reducer.py`) — 6 sentences.**

| Sentence | Both ends named | Law | Source |
|---|---|---|---|
| `sun_gear.spin.drives(planet_1.orbit, ratio=CARRIER_RATIO)` | `SunGear.spin` → `PlanetUnit.orbit` (planet 1) | `ratio=0.125` | the fixed-ring reduction, as above |
| `sun_gear.spin.drives(planet_2.orbit, ratio=CARRIER_RATIO)` | `SunGear.spin` → `PlanetUnit.orbit` (planet 2) | `ratio=0.125` | same |
| `sun_gear.spin.drives(planet_3.orbit, ratio=CARRIER_RATIO)` | `SunGear.spin` → `PlanetUnit.orbit` (planet 3) | `ratio=0.125` | same |
| `sun_in_carrier.drives(planet_1.planet_gear.spin, ratio=SUN_PLANET_MESH)` | derived `sun_in_carrier` → `PlanetGear.spin` (planet 1) | `ratio=-1/3` | the sun/planet mesh, 18 teeth into 54, sign because an external mesh reverses. Tooth counts asserted by `test_source_tooth_harmonics` |
| `sun_in_carrier.drives(planet_2.planet_gear.spin, ratio=SUN_PLANET_MESH)` | derived `sun_in_carrier` → `PlanetGear.spin` (planet 2) | `ratio=-1/3` | same |
| `sun_in_carrier.drives(planet_3.planet_gear.spin, ratio=SUN_PLANET_MESH)` | derived `sun_in_carrier` → `PlanetGear.spin` (planet 3) | `ratio=-1/3` | same |

Composed, a planet gear's spin is `-1/3 · (a − a/8) = −7a/24`, and its
absolute orientation is `orbit + spin = a/8 − 7a/24 = −a/6`: the two
numbers `docs/design.md` records and `test_fixed_ring_planetary_relations`
asserts, now produced by the model instead of by a helper function.

**`OutputStack` (`output_stack.py`) — 4 sentences.** One rigid output body
in five pieces, `planet_carrier_b` (the main carrier, placed unrotated at
the stack origin) as the piece the others turn with:

| Sentence | Both ends named | Law |
|---|---|---|
| `planet_carrier_b.turn.drives(planet_carrier_a.turn)` | `PlanetCarrierB.turn` → `PlanetCarrierA.turn` | ratio 1 |
| `planet_carrier_b.turn.drives(planet_carrier_c.turn)` | `PlanetCarrierB.turn` → `PlanetCarrierC.turn` | ratio 1 |
| `planet_carrier_b.turn.drives(encoder_magnet_holder.turn)` | `PlanetCarrierB.turn` → `EncoderMagnetHolder.turn` | ratio 1 |
| `planet_carrier_b.turn.drives(cross_roller_inner.turn)` | `PlanetCarrierB.turn` → `CrossRollerInnerRace.turn` | ratio 1 |

**`ReducerPreview` (`reducer.py`) — 1 sentence.**

| Sentence | Both ends named | Law |
|---|---|---|
| `input_angle.drives(reducer.sun_gear.spin)` | root `Driver input_angle` → `SunGear.spin` | ratio 1 |

Rejected alternative for the output stack: a `Carrier` sub-assembly with
one `turn` joint and the five pieces wired down to it (`planet_carrier_a =
PlanetCarrierA(turn=turn)`). It is one coordinate instead of four
sentences, but it inserts a level in the tree, so every path in
`seats.py`'s `EXPECTED_SEATS` and in `test_output_stack.py` changes. Four
unit relations keep every node path identical and are the cheaper honesty.

### The three ports that disappear

No port survives this change; none of the three carried anything a joint
does not now own.

- `PlanetUnit.spin` (`RotationalPort`) — forwarded one angle from the
  reducer to the planet gear's hand-written `rotate`. Replaced by joint 4.
- `PlanetaryReducer.input_angle` (`RotationalPort`) — forwarded the motor
  angle from the root, then fanned it into the sun, three orbits and three
  spins. Replaced by joint 2 plus the reducer's six sentences.
- `OutputStack.output_angle` (`RotationalPort`) — forwarded the carrier
  angle from the root and fanned it into five `rotate` calls. Replaced by
  joints 5–9 plus the stack's four sentences.

### Every `simulate()` that shrinks or disappears

| Class | Today | After |
|---|---|---|
| `PlanetUnit` | 5 lines: read `spin.value`, raise if unbound, one `rotate` | **gone** |
| `PlanetaryReducer` | 10 lines: read `input_angle.value`, raise if unbound, one `rotate`, two `kinematics` calls, a loop over three planets doing a `connect` and a `rotate` each | **gone** |
| `OutputStack` | 7 lines: read `output_angle.value`, raise if unbound, five `rotate` calls | **gone** |
| `ReducerPreview` | one `connect` | **gone**, replaced by the relation above |
| `OpenTorqueActuator` | 3 lines: one `rotate`, two `connect` | **1 line**: `self.motor_rotor.spin = self.input_angle` |
| `ActuatorPosePreview` | 4 lines | **1 line**: `self.motor_rotor.spin = self.input_angle + 360.0 * self.time` |
| `ReducerPosePreview` | one `connect` into a port | **1 line**: `self.reducer.sun_gear.spin = 360.0 * self.time` |
| `OutputStackPreview` | one `connect` into a port | **1 line**: `self.output_stack.planet_carrier_b.turn = 0.0` |

Binding one joint in `simulate()` and letting the relations solve outward
is the documented pattern (clock 01 binds `escape.turn` and the train
solves backwards). It is also what keeps `ActuatorPosePreview` a subclass:
relations are inherited and additive, never overridden, so the two classes
must differ in a `simulate()` line rather than in a relation — which is
precisely why the root's drive coordinate is the rotor's joint and not a
`Driver`-sourced relation.

### Frame arithmetic that leaves

The project writes no explicit frame inversion, but it does depend on an
unwritten one: `PlanetUnit.simulate()` calls
`self.planet_gear.rotate(spin, (0, 0, 1))` and is correct only because a
node's own operations compose innermost, before the `translate` that puts
the gear at y=27. A reader has to know both facts to know which line the
gear turns about. Joint 4 states that line in the parent's frame and the
framework carries it in.

## What does not change

- **Geometry and sources.** `STEP/opentorque.step`, every `StepNode`
  selection, `part` names, colours, `angular_deflection`, the CadQuery
  envelopes, `STEP_SHA256`.
- **Placements.** Every `render()` is untouched: the 40 mm gear group, the
  27 mm planet radius, the 120° phases, the `SEAT_WITNESS` increments, the
  motor and encoder-board offsets.
- **Poses.** Every pose is bit-identical by construction. `1/8` is exact in
  binary; each joint's carried line is the same line the current `rotate`
  turns about; the composition order of orbit-then-spin is the one the tree
  already imposes.
- **Node paths.** `reducer.planet_1.planet_gear`,
  `output_stack.planet_carrier_b` and every other path stay as they are, so
  `seats.py`'s `EXPECTED_SEATS` and its sixteen bounded pairs are untouched.
- **Control surface.** One driver `input_angle` (default 0, range ±2880°,
  deg) and three instructions `Home`, `One Motor Turn`, `One Output Turn`,
  with the same durations and targets. Joints are ports, not drivers, so
  `qualified_drivers` still reports exactly `["input_angle"]`.
- **`kinematics.py`.** Its three public functions keep their names,
  signatures and values; only their two ratio literals are replaced by the
  `layout.py` constants the relations also use. They remain the tested
  statement of the algebra even though the simulation no longer calls
  `planet_relative_angle` or `planet_absolute_angle`.
- **Contracts.** `seats.py` and every assertion in the three test modules,
  except the three port reads listed under Tests.
- **`pyproject.toml`,** the declared model, the profile, `docs/design.md`
  and `README.md` (the design document's "Motion architecture" section
  describes the same machine; a follow-up may reword "Ports bind those
  groups at the root", but that is documentation, not this refactor).

## Known gaps

**The orbit is not a missing primitive here, and the project is not
deferred.** A planet's centre moves on a circle while it spins, which is
not one coordinate on one axis — but this model already holds each planet
inside `PlanetUnit`, the carrier body it orbits with. The motion is
therefore two serial one-coordinate pairs on two bodies, which is exactly
what the framework expresses: the unit's `orbit` about the machine axis,
and the gear's `spin` about its pin in the unit's frame. Nothing about the
planetary set stays hand-written. (Had the model held `PlanetGear` directly
under `PlanetaryReducer` with no carrier body, there would be no sentence
to write and the project would be deferred; it does not, so it is not.)

Two sightings of already-recorded limits. Both cost duplication, not
hand-written motion, so neither defers the project.

1. **A relation chain must be stated in one class body**
   (`warts.md`, 2026-09-09). The sentence the project wants to write is

   ```python
   reducer.planet_1.orbit.drives(output_stack.planet_carrier_b.turn)
   ```

   — the carrier plates in the output stack ARE the body the planets orbit
   with, and saying so would state the 8:1 reduction exactly once, inside
   the reducer that owns the tooth counts. It is refused: a parent's
   relations solve before its children's, so `planet_1.orbit` is not yet
   bound when the root's relation runs, and it fails `UnreachedCoordinate`
   at `OpenTorqueActuator`. The change therefore states `CARRIER_RATIO`
   twice — once at the root for the carrier plates, once in the reducer for
   the orbits — both reading the same `layout.py` constant, so the two
   cannot drift.

2. **A joint's anchor belongs to the declaration site as often as to the
   class** (`warts.md`, 2026-09-09, the poseidon/OpenMANIPULATOR-X
   sighting). `PlanetGear` is a STEP selection with no knowledge of where
   it is bolted, yet it must carry
   `spin = Revolute(axis=(0, 0, 1), at=(0, PLANET_RADIUS, GEAR_GROUP_Z + PLANET_GEAR_Z))`
   and `parts.py` must import `layout.py` to say it, repeating the exact
   translate `PlanetUnit.render()` already writes. The sentence the project
   wants is either the own-placed-origin anchor
   (`spin = Revolute(axis=(0, 0, 1))`, meaning the line through my own
   placed origin) or the joint given at the declaration site:

   ```python
   planet_gear = PlanetGear(spin=Revolute(axis=(0, 0, 1)))
   ```

   Joints 1, 2, 5–9 are the same shape but cost nothing, because their axis
   passes through the parent frame's origin and `at` may be left at its
   default.

**Not hit.** The third recorded limit — a node's own derived coordinate is
unbound inside its own `simulate()` — cannot bite here: the only class with
derived coordinates, `PlanetaryReducer`, has no `simulate()` left.

**No new framework limit was found.**

## Pre-existing state

The repository is **clean**: `git status --porcelain` is empty on branch
`master` at `0ba5f51 feat: simulate OpenTorque actuator`. `_build/`,
`_build.lock` and `__pycache__/` are present but gitignored. Stage 0 of the
protocol therefore has nothing to commit and is recorded as a no-op.

## Tests

Three modules, all `solid_node.test.TestCase` / `ScenarioTest`, plus
`simulation/seats.py`, which is contract code rather than a test module.
Their baseline pass/fail is not known and stage A establishes it.

`simulation/test_output_stack.py` (`OutputStackPreview`) — 6 tests: every
printed STEP product is selected; source axial bounds per part; the coaxial
parts are centred on x=y=0; the cross-roller seat bounds and races not
intersecting; printed solids connected; the STEP SHA-256 fingerprint. None
reads a port. **No change expected.**

`simulation/test_reducer.py` — 7 tests: sun and planet tooth harmonics from
the STLs; the fixed-ring relations from `kinematics.py`; the three planet
bore centres; 120° spacing; bearing and pin coaxial with the gear; planet
centres follow the carrier angle at `input_angle=360`; reducer solids
connected. Plus `ReducerPosePreviewTest`.

`simulation/test_actuator.py` — 4 tests on `OpenTorqueActuator` (control
surface, driver reaches every motion group, solid integrity, seat inventory
at 0/360/2880°), one `ScenarioTest` over the three instructions with
`meshes=True`, and `ActuatorPosePreviewTest`.

**Flagged — three assertions read ports this change removes.** They assert
values, not structure, and the same values are readable from the joints
that replace those ports; the orchestrator decides.

1. `test_actuator.py::OpenTorqueActuatorTest::test_driver_reaches_every_motion_group`
   reads `self.node.reducer.input_angle.value` (expects 360.0) and
   `self.node.output_stack.output_angle.value` (expects 45.0). Both ports
   are gone. The same two numbers live at
   `self.node.reducer.sun_gear.spin.value` and
   `self.node.output_stack.planet_carrier_b.turn.value`. Why it must
   change: the port it names no longer exists, so it fails with
   `AttributeError` rather than a wrong value.
2. `test_actuator.py::ActuatorPosePreviewTest::test_time_one_is_one_motor_turn`
   reads the same two ports, for the same reason and with the same
   replacements.
3. `test_reducer.py::ReducerPosePreviewTest::test_time_one_is_one_motor_turn`
   reads `self.node.reducer.input_angle.value` (expects 360.0); the
   replacement is `self.node.reducer.sun_gear.spin.value`.

If the orchestrator would rather change no test, the only way is to keep
the three forwarding ports, which is the thing this change exists to
remove.

**Flagged as at risk, no change expected.**

- `test_reducer.py::test_planet_centers_follow_carrier_angle` measures a
  planet bore centre at `input_angle=360` and expects 27 mm at 135°. It is
  the sharpest check that the `orbit` joint reproduces the current
  `planet.rotate(carrier_angle)` exactly. If it moves, the orbit anchor or
  the composition order is wrong, not the test.
- `test_actuator.py::test_assembly_integrity_at_named_targets` and the
  scenario test call `assert_seat_inventory`, whose sixteen pairs are keyed
  by node path and bounded by measured volume. They will fail loudly if any
  path or any pose moved; both are intended to stay exactly as they are.
- `test_actuator.py::test_builder_control_surface` asserts the driver list
  is exactly `["input_angle"]`. Nine new joints are ports, not drivers, so
  it must stay green; if it does not, a joint has been declared as a driver.
