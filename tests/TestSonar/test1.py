import board
import adafruit_hcsr04
import time
import neopixel

colors = {'red': (255, 0, 0),
        'yellow': (255, 255, 0),
        'green': (0, 255, 0)}

neoLED = neopixel.NeoPixel(board.NEOPIXEL, 1)
neoLED.show()

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

while True:
    try:
        if sonar.distance < 5:
            neoLED.fill(colors.get('red'))
        elif sonar.distance >= 5 and sonar.distance <= 15:
            neoLED.fill(colors.get('yellow'))
        elif sonar.distance > 15:
            neoLED.fill(colors.get('green'))
        print((sonar.distance))
    except RuntimeError:
        print("Retrying!")
        neoLED.fill(colors.get('green'))
    time.sleep(0.1)    	