from main import Program
from cannonball import CannonBall

test_program = Program()
test_cannonball = CannonBall(test_program)

def test(cannonball, time):
    cannonball.time_after_firing = time
    cannonball.update_data()
    for key, value in vars(cannonball).items():
        print(f"{key}: {value}")

test(test_cannonball, 7)