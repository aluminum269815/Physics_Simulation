from main import Program
from cannonball import CannonBall

test_program = Program()
test_cannonball = CannonBall(test_program)

def test(cannonball, time):
    cannonball.time_after_firing = time
    cannonball.update_data()
    for key, value in vars(cannonball).items():
        if key not in ('data_lists', 'time_index', 'gravity', 'air_resistance_enabled', 'air_density'):
            print(f"{key}: {value}")

test(test_cannonball, 3)