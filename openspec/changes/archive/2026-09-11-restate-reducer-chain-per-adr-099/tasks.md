# Tasks

Repository was clean at `ad0230b` before this change (`git status
--porcelain` empty; the archived `c7f2602` ADR-097 stage B was already
committed). Only this change's own `openspec/changes/` directory,
`simulation/actuator.py` and `simulation/reducer.py` are touched.

- [x] 1. Confirm `git rev-parse --show-toplevel` names this repository
      and `git status --porcelain` is clean before editing.
- [x] 2. Capture BEFORE poses (`simulation.actuator:OpenTorqueActuator`,
      unedited) and compare against the campaign's own pre-existing
      `before2` reference. **Result:** 7 poses, 23 leaves; max deviation
      0.000e+00 against `before2`.
- [x] 3. Run the baseline suites, unedited. **Result:** faceted —
      `actuator.py` 6/6, `reducer.py` 8/8, `output_stack.py` 6/6 (20/20
      total). Exact — `reducer.py` 8/8, `output_stack.py` 6/6.
      `actuator.py`'s exact suite exceeded the 10-minute foreground
      command limit; not run (matches the briefing's own prediction, not
      a regression).
- [x] 4. Apply task 9.6's literal sentence for (a): replace
      `actuator.py`'s `motor_rotor.spin.drives(
      output_stack.planet_carrier_b.turn, ratio=CARRIER_RATIO)` with
      `reducer.planet_1.orbit.drives(output_stack.planet_carrier_b.turn)`
      and drop the now-unused `CARRIER_RATIO` import.
      **Result:** faceted suite on `actuator.py` regresses to 2/6 —
      `test_assembly_integrity_at_named_targets`,
      `test_driver_reaches_every_motion_group`,
      `ActuatorInstructionScenarioTest::test_named_moves_land_and_remain_coherent`
      and `ActuatorPosePreviewTest::test_time_one_is_one_motor_turn` all
      fail. Traced to `attempt(Root)` reading `reducer.planet_1.orbit`'s
      STALE value from the previous `set_state` pass, because
      `PlanetaryReducer`'s own phase — which clears and recomputes that
      coordinate — has not run yet when the root's own relations are
      attempted. Captured AFTER poses with this sentence applied and
      compared against step 2's capture: **max deviation 4.320e+02**
      over 7 poses (`evidence/after-attempt1-vs-before.txt`).
- [x] 5. Revert step 4 exactly (restore
      `motor_rotor.spin.drives(output_stack.planet_carrier_b.turn,
      ratio=CARRIER_RATIO)` and the `CARRIER_RATIO` import), and record
      the finding as a comment on the retained line: what was tried, the
      exact failure mechanism, and the measured deviation, so the
      sentence is not silently re-attempted by a later session.
      **Result:** faceted suite on `actuator.py` back to 6/6.
- [x] 6. Apply (b): name `ReducerPreview`'s relation
      (`drive = input_angle.drives(reducer.sun_gear.spin)`) and rewrite
      `ReducerPosePreview` as a SUBCLASS of `ReducerPreview` that
      REPLACES `drive` with `free_run.drives(ReducerPreview.reducer
      .sun_gear.spin)`, sourced from a new `free_run = RotationalPort
      (unit="deg")` bound in `simulate()` from `360.0 * self.time` —
      the exact shape of the framework's own
      `SubclassReplacesRelationTest` (`ReplaceBase`/`Preview`/
      `free_run`), written here against a real project's own classes.
      **Result:** faceted suite on `reducer.py` 8/8 (unchanged count and
      names), including `ReducerPosePreviewTest::test_time_one_is_one_motor_turn`
      passing through the new port/relation path.
- [x] 7. Run the full faceted suite again across all three test-bearing
      files. **Result:** `actuator.py` 6/6, `reducer.py` 8/8,
      `output_stack.py` 6/6 — 20/20, identical test names and counts to
      the baseline in step 3.
- [x] 8. Run the exact suites for the two smaller modules again.
      **Result:** `reducer.py` 8/8, `output_stack.py` 6/6, identical to
      baseline. `actuator.py`'s exact suite again exceeded the
      10-minute foreground limit — the same pre-existing environmental
      cost as step 3, not a consequence of this change; not run.
- [x] 9. Capture AFTER poses on the final state (step 5 reverted, step 6
      applied) and compare against both step 2's capture and the
      campaign's `before2` reference.
      **Result:** max deviation 0.000e+00 over 7 poses, 23 leaves,
      against both (`evidence/final-vs-session-before.txt`,
      `evidence/final-vs-campaign-before2.txt`).
- [x] 10. Write this proposal and these tasks; do not archive (the
      orchestrator reviews first, per this session's instructions).
