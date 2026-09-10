# Tasks

Behaviour-preserving except for the one bug ADR-097's own-frame rule
fixes (`PlanetGear.spin`'s anchor, wrong on main until this change).
Repository was clean at `1119ed7` before this change (only this change's
own new `openspec/changes/` directory and the edited `simulation/parts.py`
are touched).

- [x] 1. Confirm `git rev-parse --show-toplevel` names this repository and
      `git status --porcelain` is clean before editing.
- [x] 2. Run the faceted suite on main, unedited, across all five model
      files, to record the consequence of the early ADR-097 merge.
      **Result:** 17/20 passed, 3 failed —
      `ReducerTest.test_planet_centers_follow_carrier_angle`,
      `OpenTorqueActuatorTest.test_assembly_integrity_at_named_targets`,
      `ActuatorInstructionScenarioTest::test_named_moves_land_and_remain_coherent`.
- [x] 3. Apply the one edit in `simulation/parts.py`: delete
      `PlanetGear.spin`'s restating `at=` argument and its explanatory
      comment.
      **Result:** applied exactly as the framework cycle's
      `patch_OpenTorque-Actuator.py` derived it.
- [x] 4. Run the faceted suite again across all five model files.
      **Result:** 20/20 passed.
- [x] 5. Capture AFTER poses on main
      (`OpenTorque-Actuator-OpenTorque-Actuator-after.json`) and compare
      against the framework cycle's BEFORE file (captured on the
      pre-ADR-097 framework from the untouched source).
      **Result:** max deviation 0.000e+00 over 7 poses, 23 leaves.
- [x] 6. Run the exact suite across all five model files.
      **Result:** `parts.py` 0/0, `hardware.py` 0/0, `output_stack.py`
      6/6, `reducer.py` 8/8 all green. `actuator.py`'s exact suite did not
      complete within the available foreground time budget (10-minute
      tool limit; this file's own prior full-exact certification measured
      1283.68 s for the whole five-file batch, almost entirely inside
      this file) — flagged in `proposal.md`, not worked around by
      backgrounding or skipping quietly.
- [x] 7. Write this proposal and these tasks; do not archive (the
      orchestrator reviews first).
