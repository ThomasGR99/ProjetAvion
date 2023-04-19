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

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)

while True:
    keys = keypad.pressed_keys
    time.sleep(0.2)
    if keys:
        print("Pressed: ", keys)