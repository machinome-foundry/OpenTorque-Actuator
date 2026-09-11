# Tasks

Repository was clean at `e4a5bad` before this change (`git status
--porcelain` empty; the archived `restate-reducer-chain-per-adr-099`
revert/replace pair was already committed). Only this change's own
`openspec/changes/` directory and `simulation/actuator.py` are touched.

- [x] 1. Confirm `git rev-parse --show-toplevel` names this repository
      and `git status --porcelain` is clean before editing.
- [x] 2. Read solid-node's archived
      `deferred-read-is-current` change (`proposal.md`, `evidence.md`)
      and confirm main is past it (`9914a2e`).
- [x] 3. Capture BEFORE poses
      (`simulation.actuator:OpenTorqueActuator`, unedited) and compare
      against the campaign's own `before2` reference. **Result:** 7
      poses, 23 leaves; max deviation 0.000e+00
      (`evidence/before-vs-before2.txt`).
- [x] 4. Run the baseline suites, unedited. **Result:** faceted —
      `actuator.py` 6/6, `reducer.py` 8/8, `output_stack.py` 6/6 (20/20
      total). Exact — `reducer.py` 8/8, `output_stack.py` 6/6.
      `actuator.py`'s exact suite did not complete within the 600 s
      foreground command-timeout limit; not run, not a regression.
- [x] 5. Restate the chain in `simulation/actuator.py`: replace
      `motor_rotor.spin.drives(output_stack.planet_carrier_b.turn,
      ratio=CARRIER_RATIO)` with `reducer.planet_1.orbit.drives(
      output_stack.planet_carrier_b.turn)`; drop the now-unused
      `CARRIER_RATIO` import (the constant itself stays in `layout.py`:
      `reducer.py` and `kinematics.py` still read it); rewrite the
      retained comment to record the earlier attempt, its measured
      failure, and the upstream fix as history rather than a warning
      against the sentence now in place.
- [x] 6. Capture AFTER poses and compare against BOTH this session's
      BEFORE capture and the campaign's `before2` reference. **Result:**
      max deviation 0.000e+00 over 7 poses, 23 leaves, against both
      (`evidence/after-vs-before.txt`, `evidence/after-vs-before2.txt`).
      `capture_poses.py` re-poses one instance across all 7 poses via
      repeated `set_state`, the exact shape the earlier attempt failed
      on.
- [x] 7. Add the archived framework change's own four-re-pose probe,
      built directly against this project's real classes
      (`reducer.planet_1.orbit`, `output_stack.planet_carrier_b.turn`),
      re-posing one `OpenTorqueActuator` instance four times
      (`input_angle=10.0, 40.0, 0.0, 25.0`). **Result:** both
      coordinates match `input_angle / REDUCTION` on every one of the
      four poses (`evidence/repro_repose.py`,
      `evidence/repose-probe-output.txt`).
- [x] 8. Run the full faceted suite again across all three test-bearing
      files. **Result:** `actuator.py` 6/6, `reducer.py` 8/8,
      `output_stack.py` 6/6 — 20/20, identical test names and counts to
      the baseline in step 4.
- [x] 9. Run the exact suites for the two smaller modules again.
      **Result:** `reducer.py` 8/8, `output_stack.py` 6/6, identical to
      baseline. `actuator.py`'s exact suite was not re-run: the baseline
      measurement in step 4 already establishes the same foreground-limit
      cost, unrelated to this change's own relation statement.
- [x] 10. Write this proposal and these tasks; do not archive (the
       orchestrator reviews first).
