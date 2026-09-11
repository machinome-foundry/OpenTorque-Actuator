"""Re-pose the real OpenTorqueActuator instance four times and confirm
``reducer.planet_1.orbit.drives(output_stack.planet_carrier_b.turn)``
tracks the CURRENT reduction, not the previous ``set_state``'s value.

Run from the project root:
    PYTHONPATH=. <venv>/bin/python <this file>
"""
import os
import sys

sys.path.insert(0, os.getcwd())

from simulation.actuator import OpenTorqueActuator  # noqa: E402
from simulation.layout import REDUCTION  # noqa: E402

root = OpenTorqueActuator()
root.set_state(input_angle=0.0)
root.assemble()

for input_angle in (10.0, 40.0, 0.0, 25.0):
    root.set_state(input_angle=input_angle)
    orbit = root.reducer.planet_1.orbit.value
    carrier = root.output_stack.planet_carrier_b.turn.value
    expected_orbit = input_angle / REDUCTION
    expected_carrier = expected_orbit
    ok = (abs(orbit - expected_orbit) < 1e-9
          and abs(carrier - expected_carrier) < 1e-9)
    print(f'input_angle={input_angle}: orbit={orbit} (exp {expected_orbit})  '
          f'carrier_b.turn={carrier} (exp {expected_carrier})  '
          f'{"OK" if ok else "STALE"}')
