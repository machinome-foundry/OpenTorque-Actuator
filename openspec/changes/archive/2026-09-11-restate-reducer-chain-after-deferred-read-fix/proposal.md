# Restate the single 1:8 reducer chain now that the deferred-read defect is fixed

## Why

`openspec/changes/archive/2026-09-11-restate-reducer-chain-per-adr-099/`
tried task 9.6 of solid-node's `whole-tree-fixpoint` cycle (ADR-099)
exactly as written — `reducer.planet_1.orbit.drives(
output_stack.planet_carrier_b.turn)` in place of `actuator.py`'s
`motor_rotor.spin.drives(output_stack.planet_carrier_b.turn,
ratio=CARRIER_RATIO)` — and reverted it with measured evidence: on a
freshly built instance the sentence resolved correctly, but on every
`set_state` after the first, `output_stack`'s bodies landed on the
PREVIOUS pose's carrier angle (max deviation 4.320e+02 over the
project's 7 poses). Its "Known gaps" named the cause precisely: "the
framework's own deferral test not yet distinguishing 'never bound this
pass' from 'bound last pass, not yet cleared'" — a framework defect, not
a project limit, reported for the pilot/orchestrator rather than worked
around.

solid-node main is now at `9914a2e`, past the archived
`solid-node/openspec/changes/archive/2026-09-11-deferred-read-is-current/`
change. Its proposal names the identical cause — `ResolvedEnd.bound()`
asked only whether a slot's value was non-`None`, so a value an ancestor
reads before the owning descendant's phase has run this pass (left over
from the previous pass) read as bound and was solved immediately instead
of deferred — and fixes it: `ResolvedEnd.bound()` now additionally asks
whether the assembly that bound a non-fresh value (`slot._bound_by`) is
the assembly currently attempting its own relations or one of that
assembly's own descendants; if so the end reads unbound and this
attempt defers to the pass's own tree-wide fixpoint, which runs after
`PlanetaryReducer`'s own phase has rebound the coordinate fresh. Its own
evidence (section 3.2) builds this project's exact shape — source two
levels down inside one child subtree, driven end inside a separate
sibling subtree with no relation of its own — and re-poses it four times
against the fix, matching the expected value on every call.

## What changes

`simulation/actuator.py`: `motor_rotor.spin.drives(
output_stack.planet_carrier_b.turn, ratio=CARRIER_RATIO)` is replaced
with `reducer.planet_1.orbit.drives(output_stack.planet_carrier_b.turn)`
— the single 1:8 chain task 9.6 asked for and the archived
`restate-reducer-chain-per-adr-099` change wrote and then reverted. The
carrier motion now sources from the coordinate `PlanetaryReducer`'s own
relations already compute, instead of restating `CARRIER_RATIO` a
second time at the root.

`CARRIER_RATIO`'s import is removed from `actuator.py` (its only reader
there). The constant itself, defined in `layout.py`, is NOT deleted:
`reducer.py` (`sun_gear.spin.drives(planet_{1,2,3}.orbit,
ratio=CARRIER_RATIO)`) and `kinematics.py` (`output_angle`) still read
it directly, so it remains stated once, where the reduction stage
itself needs it.

The comment on the retained-then-reverted line in `actuator.py`, which
recorded exactly what was tried and why it failed, is rewritten to
record the same finding as history and to name the upstream fix and
this change's own repose probe, rather than warning a future session
away from the sentence now in place.

No geometry, placement, port count, driver, instruction, or test file is
changed. `output_stack.py`, `reducer.py`'s own body, and every
part/hardware module are untouched.

## Evidence

Repository clean at `e4a5bad` before this change (`git status
--porcelain` empty). Workspace venv
`/home/asa/devel/libresolid-studio/.venv/bin/python`, `PYTHONPATH=.`
from the project root; solid-node main at `9914a2e`.

- **BEFORE poses vs. the campaign's `before2` reference.**
  `capture_poses.py capture simulation.actuator:OpenTorqueActuator` on
  the unedited tree: 7 poses, 23 leaves; compared against
  `before2/OpenTorque-Actuator-OpenTorque-Actuator-before.json`: **max
  deviation 0.000e+00** (`evidence/before-vs-before2.txt`).
- **Baseline suites, unedited.** Faceted — `actuator.py` 6/6,
  `reducer.py` 8/8, `output_stack.py` 6/6 (20/20 total). Exact —
  `reducer.py` 8/8, `output_stack.py` 6/6. `actuator.py`'s exact suite
  did not complete within the 600 s foreground command-timeout limit
  (matches this project's own prior measurement of ~1283 s for the
  five-file batch, almost entirely inside this file); not run, not a
  regression — the change touches only this file's own relation
  statement, not its geometry or test count.
- **AFTER poses vs. BEFORE (this session).** After applying the restated
  chain: **max deviation 0.000e+00** over 7 poses, 23 leaves
  (`evidence/after-vs-before.txt`).
- **AFTER poses vs. the campaign's `before2` reference.** **max
  deviation 0.000e+00** over 7 poses (`evidence/after-vs-before2.txt`).
  `capture_poses.py` re-poses ONE instance across all 7 poses via
  repeated `set_state` calls — the exact shape the archived change's
  attempt failed on — so this 0.000e+00 is itself proof the deferred-read
  fix holds across repeated poses of the real project instance, not just
  on first assembly.
- **The archived change's own four-re-pose probe, on real project
  code.** `evidence/repro_repose.py` builds no fixture: it re-poses the
  actual `OpenTorqueActuator` instance four times
  (`input_angle=10.0, 40.0, 0.0, 25.0`, in that order — the same
  ordering framework evidence 3.2 uses to guarantee a stale-vs-fresh
  round trip) and reads `reducer.planet_1.orbit` and
  `output_stack.planet_carrier_b.turn` after each call. Every call
  matches `input_angle / REDUCTION` on the first attempt, both
  coordinates, all four poses (`evidence/repose-probe-output.txt`).
- **Suites after the edit.** Faceted — `actuator.py` 6/6, `reducer.py`
  8/8, `output_stack.py` 6/6 — 20/20 total, identical test names and
  counts to baseline. Exact — `reducer.py` 8/8, `output_stack.py` 6/6,
  identical to baseline. `actuator.py`'s exact suite was not re-run: the
  baseline measurement already establishes it exceeds the foreground
  limit for reasons unrelated to this change (five-file OCCT batch cost
  documented by the prior cycle), and re-running a confirmed-exceeding
  10-minute command a second time in the foreground would not add
  evidence this change's other three comparisons do not already give.

## Known gaps

None found for this restatement. The one gap the archived change
reported — the framework's deferral test not distinguishing "never
bound this pass" from "bound last pass, not yet cleared" — is exactly
what `deferred-read-is-current` fixed upstream; this change is the
originating project's own validation of that fix, per the framework
cycle's own task 3.2 and this project's `move-onto-motion` "Known gaps"
entry.
