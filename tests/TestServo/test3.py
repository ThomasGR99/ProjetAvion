# pyright: reportShadowedImports=false
# La ligne de code en-haut est pour enlever les lignes jaunes de warning
# qui apparaissent en-dessous de tout le code
import time
import board
import pwmio
from adafruit_motor import servo
from analogio import AnalogIn

patte_servo = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(patte_servo)

analog_in = AnalogIn(board.A1)

def get_voltage(pin):
    return (pin.value * 2.5 / 51000)

volt_multiplier = 180 / 2.5

while True:
    voltage = get_voltage(analog_in)
    angle = voltage * volt_multiplier

    if angle >= 0 and angle <= 180:
        my_servo.angle = angle
   