# pyright: reportShadowedImports=false
# La ligne de code en-haut est pour enlever les lignes jaunes de warning
# qui apparaissent en-dessous de tout le code

import time
import board
import pwmio
import digitalio
import adafruit_matrixkeypad
from adafruit_motor import servo

cols = [digitalio.DigitalInOut(x) for x in (board.D9, board.D6, board.D5, board.SCL)]
rows = [digitalio.DigitalInOut(x) for x in (board.D13, board.D12, board.D11, board.D10)]
keys = ((1, 2, 3, 'A'),
        (4, 5, 6, 'B'),
        (7, 8, 9, 'C'),
        ('*', 0, '#', 'D'))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

patte_servo = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(patte_servo)

angle = 0

temps_cycle = 5 #5 secondes de temps par cycle


while True:
    for angle in range(0, 180):
        my_servo.angle = angle
        time.sleep(temps_cycle / 180)

    for angle in range(180, 0, -1):
        my_servo.angle = angle
        time.sleep(temps_cycle / 180)