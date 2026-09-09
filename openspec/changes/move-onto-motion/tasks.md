# Tasks

Behaviour-preserving throughout: the acceptance is that every leaf's
composed world matrix is unchanged at every pose, so evidence is captured
before the first refactoring edit and compared after the last. The project
repository is clean at `0ba5f51`, so there is no stage 0 commit.

Run everything from the project root with `PYTHONPATH=.` and the workspace
venv (`/home/asa/devel/libresolid-studio/.venv/bin/python`,
`.venv/bin/solid`). Never run two suites at once. Never edit a test: the
three port reads flagged in `proposal.md` are the orchestrator's decision,
not the implementer's — stop and report if one blocks the run.

**Orchestrator decisions (review, 2026-09-09), applied here and in
`proposal.md`:**

1. One derived coordinate, not three: `sun_in_carrier = sun_gear.spin -
   planet_1.orbit` in `PlanetaryReducer`, driving all three planet gears
   via `sun_in_carrier.drives(planet_N.planet_gear.spin,
   ratio=SUN_PLANET_MESH)` for N = 1, 2, 3. The three
   `sun_gear.spin.drives(planet_N.orbit, ratio=CARRIER_RATIO)` sentences
   stay as proposed.
2. The three test edits `proposal.md` flags under "Tests" are AUTHORISED,
   in stage B only, because the removed ports' values now live on joints
   and the assertions keep their meaning:
   - `test_actuator.py::OpenTorqueActuatorTest::test_driver_reaches_every_motion_group`:
     `reducer.input_angle.value` → `reducer.sun_gear.spin.value`;
     `output_stack.output_angle.value` → `output_stack.planet_carrier_b.turn.value`.
   - `test_actuator.py::ActuatorPosePreviewTest::test_time_one_is_one_motor_turn`:
     the same two replacements.
   - `test_reducer.py::ReducerPosePreviewTest::test_time_one_is_one_motor_turn`:
     `reducer.input_angle.value` → `reducer.sun_gear.spin.value`.
   Nothing else in any test changes. If any other test fails after stage B,
   stop and report the exact assertion.
3. Everything else proceeds exactly as proposed.

## 0. Pre-existing state

- [x] 0.1 Confirm `git rev-parse --show-toplevel` is this repository and
      `git status --porcelain` is empty on `master` at `0ba5f51`. Record
      "clean, no stage 0 commit" in this file. Leave `_build/`,
      `_build.lock` and `__pycache__/` alone.

      **Result:** clean, no stage 0 commit. `git rev-parse --show-toplevel`
      names this repository. Only untracked entry was
      `openspec/changes/move-onto-motion/`, committed with stage A below.

## 1. Stage A — baseline

- [x] 1.1 Fix imports only: `simulation/reducer.py` and
      `simulation/output_stack.py` take `RotationalPort` from
      `solid_node.motion.ports` instead of `solid_node.node`; `AssemblyNode`
      still comes from `solid_node.node`. Change nothing else.
- [x] 1.2 Run the declared model's suite:
      `solid test --faceted simulation.actuator:OpenTorqueActuator`, then
      the preview modules' suites
      (`simulation/test_reducer.py`, `simulation/test_output_stack.py`).
      Record the per-test result — pass, fail, error, with the assertion —
      in this file. This is the baseline; a red test here stays red.

      **Result — all 20 tests green, no plain pytest suite in this project.**

      - `solid test --faceted simulation.actuator:OpenTorqueActuator` — 5
        passed (`OpenTorqueActuatorTest` ×4,
        `ActuatorInstructionScenarioTest` ×1).
      - `solid test --faceted simulation.actuator:ActuatorPosePreview` — 1
        passed (`ActuatorPosePreviewTest`).
      - `solid test --faceted simulation.reducer:ReducerPreview` — 7 passed
        (`ReducerTest` ×7).
      - `solid test --faceted simulation.reducer:ReducerPosePreview` — 1
        passed (`ReducerPosePreviewTest`).
      - `solid test --faceted simulation.output_stack:OutputStackPreview` —
        6 passed (`OutputStackTest` ×6).

      Total baseline: **20 passed, 0 failed.**
- [x] 1.3 Capture poses with the shop's
      `docs/motion-general-refactor/capture_poses.py`, one file per model:
      `OpenTorqueActuator` (with an `extra` file for `Home`,
      `One Motor Turn` and `One Output Turn`), `ActuatorPosePreview`,
      `ReducerPreview`, `ReducerPosePreview`, `OutputStackPreview`, to
      `/tmp/opentorque-<model>-before.json`.

      **Result:** all five captured.
      `/tmp/opentorque-OpenTorqueActuator-before.json` (10 poses incl. the
      three named instruction targets, 23 leaves),
      `/tmp/opentorque-ActuatorPosePreview-before.json` (7 poses, 23
      leaves), `/tmp/opentorque-ReducerPreview-before.json` (7 poses, 10
      leaves), `/tmp/opentorque-ReducerPosePreview-before.json` (4 poses,
      10 leaves), `/tmp/opentorque-OutputStackPreview-before.json` (4
      poses, 10 leaves).
- [x] 1.4 Commit as `refactor(simulation): import ports from
      solid_node.motion`, with the baseline in the message body.

## 2. Stage B — the motion refactor

- [ ] 2.1 `simulation/layout.py`: add `CARRIER_RATIO = 1.0 / REDUCTION` and
      `SUN_PLANET_MESH = -SUN_TEETH / PLANET_TEETH` beside the tooth
      counts. Rewrite `kinematics.output_angle` and
      `kinematics.planet_relative_angle` to read them, keeping their
      names, signatures and values unchanged.
- [ ] 2.2 Declare the nine joints exactly as tabled in `proposal.md`:
      `spin` on `MotorRotorEnvelope` and `CrossRollerInnerRace.turn` in
      `hardware.py`; `spin` on `SunGear` and `PlanetGear`, `turn` on
      `PlanetCarrierA`, `PlanetCarrierB`, `PlanetCarrierC` and
      `EncoderMagnetHolder` in `parts.py`; `orbit` on `PlanetUnit` in
      `reducer.py`. No `range` on any of them. `parts.py` imports
      `PLANET_RADIUS`, `GEAR_GROUP_Z` and `PLANET_GEAR_Z` for the planet
      gear's anchor.
- [ ] 2.3 `simulation/reducer.py`: delete `PlanetUnit.spin`,
      `PlanetaryReducer.input_angle` and both `simulate()` methods. State
      **one** derived coordinate `sun_in_carrier = sun_gear.spin -
      planet_1.orbit` (orchestrator decision, review 2026-09-09: a
      coordinate may source several relations; only a driven end has a
      single binder) and the six sentences (three orbits at
      `ratio=CARRIER_RATIO`, three meshes at `ratio=SUN_PLANET_MESH`, all
      three read from `sun_in_carrier`) in `PlanetaryReducer`'s class body.
- [ ] 2.4 `simulation/reducer.py`: `ReducerPreview` states
      `input_angle.drives(reducer.sun_gear.spin)` and loses its
      `simulate()`; keep its `output_angle` property. `ReducerPosePreview`
      binds `self.reducer.sun_gear.spin = 360.0 * self.time`.
- [ ] 2.5 `simulation/output_stack.py`: delete `OutputStack.output_angle`
      and its `simulate()`; state the four unit relations from
      `planet_carrier_b.turn`. `OutputStackPreview` binds
      `self.output_stack.planet_carrier_b.turn = 0.0`.
- [ ] 2.6 `simulation/actuator.py`: state the two root sentences
      (`motor_rotor.spin` to `reducer.sun_gear.spin`, and to
      `output_stack.planet_carrier_b.turn` at `ratio=CARRIER_RATIO`).
      `OpenTorqueActuator.simulate()` becomes the single line
      `self.motor_rotor.spin = self.input_angle`;
      `ActuatorPosePreview.simulate()` the single line
      `self.motor_rotor.spin = self.input_angle + 360.0 * self.time`.
      `render()`, the driver and the instructions are untouched.
- [ ] 2.7 Confirm nothing imports a removed port and that no `render()`,
      no `seats.py` entry and no node path changed.

## 3. Evidence again

- [ ] 3.1 Re-capture every model's poses to
      `/tmp/opentorque-<model>-after.json` and run
      `capture_poses.py compare before after`. Expected maximum deviation
      0 at every pose, including the three named instruction targets and
      `time=1.0` on both pose previews. Any non-zero deviation stops the
      work and is reported, not accepted.
- [ ] 3.2 Run the same suites as 1.2 and compare against the baseline: the
      same tests green, none newly red. The three port reads flagged in
      `proposal.md` will fail with `AttributeError` until the orchestrator
      rules on them — report them, do not edit them.
- [ ] 3.3 Record in this file: the pose comparison line, the test counts
      before and after, every deviation from the proposal and why, and any
      framework behaviour that contradicted it (in particular whether the
      reducer's derived coordinates solve in the same fixpoint as the
      relations that bind their terms).
- [ ] 3.4 Commit as `refactor(simulation): move OpenTorque onto solid-node
      joints and couplings`, with the pose result and the test result in
      the body. Do not sync or archive this change; the orchestrator does
      that after review.
