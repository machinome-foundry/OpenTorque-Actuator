# Restate the reducer chain and prove the subclass relation replacement (ADR-099)

## Why

solid-node main (9a2ff68) integrated `whole-tree-fixpoint` (ADR-099): a
relation, derived formula or wiring that cannot resolve in its own class's
phase is now DEFERRED and resolved once every phase in the tree has run,
instead of being refused immediately; and a subclass assigning a relation
to a name a base class used now REPLACES it at the base's position, while
a bare statement stays additive. The framework cycle's own task list
(`solid-node/openspec/changes/archive/2026-09-11-whole-tree-fixpoint/tasks.md`,
task 9.6) named this project's own reducer chain and its
`ReducerPreview`/`ReducerPosePreview` pair as the two "sentences the
project wants" to prove ON REAL PROJECT CODE, and left both unchecked on
purpose: "the four project overlays ... are proved instead by each
project's own stage B on this cycle, which is where the sentence is
written for real."

This project's own archived `move-onto-motion` proposal
(`openspec/changes/archive/2026-09-09-move-onto-motion/proposal.md`,
"Known gaps") recorded the two sightings this cycle closed:

1. **The one-class-body rule.** The root wanted to write
   `reducer.planet_1.orbit.drives(output_stack.planet_carrier_b.turn)`
   but could not: a parent's relations solved before its children's, so
   `planet_1.orbit` was not yet bound when the root's relation ran, and
   the sentence failed `UnreachedCoordinate`. `CARRIER_RATIO` was
   therefore stated twice — once in `actuator.py` for the carrier plates,
   once in `reducer.py` for the orbits.
2. **Additive-only inheritance.** `workflow/warts.md`'s entry for this
   finding records the wanted mechanism directly: "a subclass may replace
   a NAMED relation of its base, the way a redeclared port wins."

## What changes

### (a) The single 1:8 chain — tried, and reverted with the evidence

Task 9.6 asked for `actuator.py`'s
`motor_rotor.spin.drives(output_stack.planet_carrier_b.turn,
ratio=CARRIER_RATIO)` to become
`reducer.planet_1.orbit.drives(output_stack.planet_carrier_b.turn)`,
sourcing the carrier motion from the coordinate the reducer's own
relations already compute, so `CARRIER_RATIO` is written once instead of
twice.

**Tried exactly as written, and it is wrong on every pose after the
first.** On a freshly constructed instance the sentence resolves
correctly: `reducer.planet_1.orbit` starts unbound, so the pass defers
the relation and the tree-wide fixpoint fills it in, exactly as ADR-099
promises. But `OpenTorqueActuator` (the root) is reused across poses —
`capture_poses.py`, every `ScenarioTest`, and the builder's own slider all
call `set_state` repeatedly on ONE instance — and on the second and every
later `set_state`, `attempt(Root)` (root's own relations, resolved before
any child's phase runs, per the ADR's own order-of-events table) finds
`reducer.planet_1.orbit` already non-`None`: the value it was left
holding at the end of the PREVIOUS pass, because `PlanetaryReducer` — the
assembly whose phase clears and recomputes that coordinate — has not run
yet this pass. `attempt` treats a present-but-stale value exactly like a
fresh one and binds `output_stack.planet_carrier_b.turn` from it
immediately, instead of deferring to the tree-wide fixpoint where the
current pass's fresh value would land. The whole output body then always
shows the PREVIOUS pose's carrier angle, one pose behind.

Measured directly: capturing this project's 7 poses with the sentence
applied and comparing against the unmodified baseline gives **maximum
deviation 4.320e+02** — `output_stack.planet_carrier_a/b/c`,
`cross_roller_inner` and `encoder_magnet_holder` all land on the prior
pose's `.turn` value (`evidence/after-attempt1-vs-before.txt`). This is
not a legitimate pose difference to accept and explain; it is the
machine assembling wrong. The sentence is reverted: `actuator.py` keeps
`motor_rotor.spin.drives(output_stack.planet_carrier_b.turn,
ratio=CARRIER_RATIO)`, with a comment recording exactly what was tried,
why it fails, and the measurement, so the next session does not repeat
the experiment. `CARRIER_RATIO` is still stated twice, exactly as
`move-onto-motion`'s Known gaps left it — an accepted duplication cost,
not a hand-written motion.

**The sentence the project wants instead:** the one task 9.6 names,
`reducer.planet_1.orbit.drives(output_stack.planet_carrier_b.turn)` —
but only once the deferral test recognizes a value left over from the
PREVIOUS pass, on a coordinate whose owning assembly's phase has not yet
run THIS pass, as unready — the same as a genuinely unbound one — rather
than treating any non-`None` value as ready. `clear_bound`'s per-assembly
timing (clearing what an assembly bound "during its previous simulate
phase," at the start of THAT assembly's own next phase) is exactly right
for a single render; it is what leaves an ancestor's `attempt`, which
always completes before any descendant's phase begins, able to observe
the descendant's leftover value from last time as if it were current.

### (b) The subclass relation replacement — proven, on real project code

`reducer.py`'s `ReducerPreview`/`ReducerPosePreview` pair is exactly the
"two variants sharing a base" shape the whole-tree-fixpoint cycle asked
this project to supply:

- `ReducerPreview`'s relation is now NAMED —
  `drive = input_angle.drives(reducer.sun_gear.spin)` — so a subclass may
  replace it.
- `ReducerPosePreview` is now a SUBCLASS of `ReducerPreview` (previously
  a separate ground-up class that duplicated `reducer = PlanetaryReducer()`
  and hand-drove `self.reducer.sun_gear.spin = 360.0 * self.time` from
  its own `simulate()`), and REPLACES the inherited `drive` relation with
  one sourced from its own port instead of the inherited `input_angle`:

  ```python
  class ReducerPosePreview(ReducerPreview):
      free_run = RotationalPort(unit="deg")
      drive = free_run.drives(ReducerPreview.reducer.sun_gear.spin)

      def simulate(self):
          self.free_run = 360.0 * self.time
  ```

  `declared_relations` drops the base's `drive` from the subclass's
  enumeration and keeps the replacing one at the position the base's
  held, exactly as `ADR-099`/`ADR-093`'s redeclared-joint rule already
  does for joints; `ReducerPreview` itself is untouched, and an instance
  of it still solves its own `input_angle`-sourced relation. This is the
  exact shape of the framework's own proof
  (`tests/test_couplings.py::SubclassReplacesRelationTest`,
  `ReplaceBase`/`Preview`/`free_run`), written here for the first time
  against a real project's own two classes.

No geometry, placement, port count (beyond the one new `free_run` on
`ReducerPosePreview`), driver, instruction, or `actuator.py`-level test
changes. `output_stack.py` and every part/hardware module are untouched.

## Evidence

- Repository clean at `ad0230b` before this change (`git status
  --porcelain` empty); nothing staged or committed except this change's
  own `openspec/changes/` directory and the two edited simulation files.
- **Baseline (unmodified, this session).** Faceted, all three test-bearing
  files: `actuator.py` 6/6, `reducer.py` 8/8, `output_stack.py` 6/6 — 20/20
  total. Exact: `reducer.py` 8/8, `output_stack.py` 6/6. `actuator.py`'s
  exact suite did not complete within the 10-minute foreground command
  limit (this project's own prior full-exact certification measured
  ~1283 s for the five-file batch, almost entirely inside this file) —
  not run, not a regression.
- **Pose evidence, baseline.** `capture_poses.py capture
  simulation.actuator:OpenTorqueActuator` before any edit: 7 poses, 23
  leaves; compared against the campaign's own pre-existing `before2`
  reference (`OpenTorque-Actuator-OpenTorque-Actuator-before.json`,
  captured before this whole campaign started): **max deviation 0.000e+00.**
- **(a) tried.** With `reducer.planet_1.orbit.drives(
  output_stack.planet_carrier_b.turn)` applied: faceted suite regresses
  to 2/6 passing on `actuator.py` (`test_assembly_integrity_at_named_targets`,
  `test_driver_reaches_every_motion_group`,
  `ActuatorInstructionScenarioTest::test_named_moves_land_and_remain_coherent`,
  `ActuatorPosePreviewTest::test_time_one_is_one_motor_turn` all fail);
  pose comparison against the pre-edit capture: **max deviation
  4.320e+02** over 7 poses. Reverted; not committed as a passing state at
  any point.
- **(b) applied, and (a) reverted — final state.** Faceted: `actuator.py`
  6/6, `reducer.py` 8/8, `output_stack.py` 6/6 — 20/20 total, identical
  test names and counts to baseline. Exact: `reducer.py` 8/8,
  `output_stack.py` 6/6, both identical to baseline;
  `ReducerPosePreviewTest::test_time_one_is_one_motor_turn` (which reads
  `reducer.sun_gear.spin.value == 360.0` at `time=1.0`, exercised through
  the new subclass/port/replaced-relation path) passes under both
  kernels. `actuator.py`'s exact suite again did not complete within the
  10-minute foreground limit — the same pre-existing environmental cost
  as the baseline, not a consequence of this change (its `simulate()` and
  relations are unchanged by (b), and (a) was reverted).
- **Pose evidence, final.** `capture_poses.py capture
  simulation.actuator:OpenTorqueActuator` after this change, compared
  against both the pre-edit capture from this session and the campaign's
  `before2` reference: **max deviation 0.000e+00** over 7 poses, 23
  leaves, against both.

## Known gaps

- **(a) is not a project limit; it is the framework's own deferral test
  not yet distinguishing "never bound this pass" from "bound last pass,
  not yet cleared."** Both are `value is not None` before ADR-099's
  `attempt`/`run_deferred` machinery would need to tell them apart; today
  only the first is `None`. Reported for the pilot/orchestrator rather
  than worked around: no rewrite of this project's own code closes it,
  since any relation sourcing a root-level sentence from a coordinate a
  descendant's own relations bind is subject to the same staleness the
  moment the same instance is posed twice.
- (b) is proven exactly as written; no gap found. The framework's own
  `SubclassReplacesRelationTest` and this project's `ReducerPosePreview`
  now agree on the same shape.
