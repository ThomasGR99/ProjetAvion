# pyright: reportShadowedImports=false
# La ligne de code en-haut est pour enlever les lignes jaunes de warning
# qui apparaissent en-dessous de tout le code
import time
import board
import pwmio
from analogio import AnalogIn
from adafruit_motor import motor

MAX_VOLT = 3.3
POINT_ZERO = MAX_VOLT/2

analog_in = AnalogIn(board.A3)

pospwm = pwmio.PWMOut(board.A0, frequency=1000)
negpwm = pwmio.PWMOut(board.A1, frequency=1000)

motor_one = motor.DCMotor(pospwm, negpwm)

def get_voltage(pin):
    return (pin.value * MAX_VOLT / 51200)

while True:
    voltage = get_voltage(analog_in)
    
    new_throttle = (voltage - POINT_ZERO) / POINT_ZERO
    new_throttle = max(-1, min(new_throttle, 1))
    
    if voltage < 0.20:
        new_throttle = -1

    motor_one.throttle = new_throttle
    print(new_throttle)
    time.sleep(0.02)
    

    

   