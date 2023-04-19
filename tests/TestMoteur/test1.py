# pyright: reportShadowedImports=false
# La ligne de code en-haut est pour enlever les lignes jaunes de warning
# qui apparaissent en-dessous de tout le code
import time
import board
import pwmio
from adafruit_motor import motor


pospwm = pwmio.PWMOut(board.A0, frequency=1000)
negpwm = pwmio.PWMOut(board.A1, frequency=1000)

motor = motor.DCMotor(pospwm, negpwm)

THROTTLE_MIN = -1.0
THROTTLE_STOP = 0.0
THROTTLE_MAX = 1.0

def ramp_throttle(start, end, duration):
    if start < end:
        # ramp up
        step_size = (end - start) / duration
        t = time.monotonic()
        while time.monotonic() - t < duration:
            motor.throttle = start + (time.monotonic() - t) * step_size
            print(motor.throttle)
            time.sleep(0.05)
    else:
        # ramp down
        step_size = (start - end) / duration
        t = time.monotonic()
        while time.monotonic() - t < duration:
            motor.throttle = start - (time.monotonic() - t) * step_size
            print(motor.throttle)
            time.sleep(0.05)
while True:
   
    ramp_throttle(THROTTLE_STOP, THROTTLE_MAX, 5)
    
    ramp_throttle(THROTTLE_MAX, THROTTLE_MIN, 10)
    
    ramp_throttle(THROTTLE_MIN, THROTTLE_STOP, 5)
    

   