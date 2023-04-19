# pyright: reportShadowedImports=false
# La ligne de code en-haut est pour enlever les lignes jaunes de warning
# qui apparaissent en-dessous de tout le code

import board
import pwmio
from adafruit_motor import servo

patte_servo = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(patte_servo)

while True:
    angle_string = input('Entrez l\'angle voulu entre 0 et 180 : ')
    
    try:
        angle = int(angle_string)
        if angle < 0 or angle > 180:
            raise ValueError()
    except ValueError:
        print("Entrée invalide.")
        continue

    my_servo.angle = angle