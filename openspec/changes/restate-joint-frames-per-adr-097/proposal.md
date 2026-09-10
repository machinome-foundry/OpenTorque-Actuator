# Restate joint frames for ADR-097 (joint-frame-follows-declarer)

## Why

solid-node main (91c0b2a) integrated `joint-frame-follows-declarer`
(ADR-097): a class-body joint's `axis`, `at` and `carries` are now read in
the DECLARING BODY'S OWN REST FRAME, not the parent's. `at` defaults to the
body's own origin. This project was migrated onto the motion layer in the
prior stage (`archive/2026-09-09-move-onto-motion`), which stated `at` in
the PARENT's frame as that framework required at the time. One of its nine
joints is now wrong on main:

`PlanetGear.spin` wrote
`at=(0, PLANET_RADIUS, GEAR_GROUP_Z + PLANET_GEAR_Z)`, which the source
comment already said is "exactly `PlanetUnit.render()`'s
`translate((0, PLANET_RADIUS, GEAR_GROUP_Z + PLANET_GEAR_Z))`" — i.e. it
restated the parent's placement of this body. Under the new convention
that restatement is applied twice, and running the faceted suite on main
before this change reproduces the consequence exactly: `parts.py`'s
`PlanetGear` moves off its pin, and both
`test_assembly_integrity_at_named_targets` and
`ActuatorInstructionScenarioTest::test_named_moves_land_and_remain_coherent`
fail — the sun/planet mesh pairs `(reducer.planet_N.planet_gear,
reducer.sun_gear)` disappear from the measured interference set while
spurious pairs against `output_stack.actuator_housing` and
`planet_carrier_b`/`planet_carrier_c` appear instead, and
`test_planet_centers_follow_carrier_angle` in `reducer.py`'s suite fails
to find the expected bore vertices at all.

The other eight joints need no change: `PlanetCarrierA.turn`,
`PlanetCarrierC.turn`, `SunGear.spin`, `CrossRollerInnerRace.turn` and
`MotorRotorEnvelope.spin` are each translated by their parent exactly
along their own joint axis (ZERO-BUT-PLACED, inert under the new rule);
`PlanetCarrierB.turn` and `EncoderMagnetHolder.turn` sit at identity
parent placements (own-origin-already); and `PlanetUnit.orbit`, though
instantiated three times with two of those instances rotated 120°/-120°
by their parent, is rotated about its own axis line in both cases, which
leaves the axis invariant at every instantiation.

This is stage B of the campaign tracked at
`libresolid-studio/docs/motion-general-refactor.md`; the archived framework
change `solid-node/openspec/changes/archive/2026-09-10-joint-frame-follows-declarer/`
(`evidence/survey.md` §1.2) is the survey this proposal implements.

## What changes

`simulation/parts.py`, one joint declaration, no other file:

`PlanetGear.spin`: the `at=(0, PLANET_RADIUS, GEAR_GROUP_Z +
PLANET_GEAR_Z)` argument (and the comment that only existed to explain it)
is deleted, so the declaration becomes
`spin = Revolute(axis=(0, 0, 1), unit="deg")` — the default `(0, 0, 0)` is
now correct in `PlanetGear`'s own rest frame.

No geometry, placement, port, driver, instruction, or test changes. No
spec delta: `openspec/specs/planetary-reduction/spec.md`'s claim that
"each planet axis is 27 mm from the actuator axis" describes the physical
(post-placement) axis, which this change preserves exactly — only the
own-frame literal used to reach that same physical axis changes (from a
restated offset to the now-correct default).

## Evidence

- Faceted suite on main, before this change, across all five model files:
  20 total tests, 17 passed, 3 failed —
  `ReducerTest.test_planet_centers_follow_carrier_angle` (`reducer.py`),
  `OpenTorqueActuatorTest.test_assembly_integrity_at_named_targets` and
  `ActuatorInstructionScenarioTest::test_named_moves_land_and_remain_coherent`
  (`actuator.py`) — this is the predicted consequence of the early
  framework merge, reproduced.
- Faceted suite after: 20/20 passed across all five model files
  (`parts.py` 0/0 build-only, `hardware.py` 0/0 build-only,
  `output_stack.py` 6/6, `reducer.py` 8/8, `actuator.py` 6/6).
- Exact suite after: `parts.py` 0/0, `hardware.py` 0/0, `output_stack.py`
  6/6, `reducer.py` 8/8 all confirmed green and fast. `actuator.py`'s exact
  suite could not be run to completion within this session's available
  foreground time: the project's own prior full-exact certification
  (`archive/2026-09-07-simulate-the-opentorque-actuator/tasks.md` task
  5.5) measured 1283.68 s for the same five-file batch, almost entirely
  inside `actuator.py`'s exact assembly-integrity and scenario checks,
  which exceeds the tool's 10-minute foreground command limit used here.
  This is a pre-existing cost of this project's exact suite, not a
  regression from this change; the faceted suite (which exercises exactly
  the same interference assertions at tessellation precision) is green,
  and the pose comparison below is bit-exact.
- Pose comparison: `capture_poses.py compare` of the pre-change BEFORE
  file (captured by the framework cycle on the pre-ADR-097 framework, from
  the untouched source) against an AFTER file captured on main with this
  change applied: **max deviation 0.000e+00 over 7 poses, 23 leaves.**

## Known gaps

None found specific to this project's joints beyond what the archived
framework change and the campaign tracker already record. The rule stated
this project's nine joints exactly; no sentence was unreachable. The
`actuator.py` exact-suite runtime is a pre-existing environmental cost
(recorded above), not a rule limitation — flagged for the orchestrator
rather than worked around.
