# pyright: reportShadowedImports=false
# La ligne de code en-haut est pour enlever les lignes jaunes de warning
# qui apparaissent en-dessous de tout le code
import time
import math
import board
import analogio

x_axis = analogio.AnalogIn(board.A1)
y_axis = analogio.AnalogIn(board.A2)

deadzone_radius = 0.1

while True:
    x = (x_axis.value / 32768) - 1
    y = (y_axis.value / 32768) - 1

    if abs(x) < deadzone_radius and abs(y) < deadzone_radius:
        angle_degree = 0
    else:
        angle_degree = math.degrees(math.atan2(y, x))
    if (angle_degree < 0):
        degree = (angle_degree + 360) % 360
    else:
        degree = angle_degree
    print (int(degree))
    time.sleep(0.05)