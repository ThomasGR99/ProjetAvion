# pyright: reportShadowedImports=false
# La ligne de code en-haut est pour enlever les lignes jaunes de warning
# qui apparaissent en-dessous de tout le code
import time
import math
import board
import pwmio
import adafruit_hcsr04
import adafruit_dht
import digitalio
import neopixel
import analogio
from adafruit_motor import motor
from adafruit_motor import servo
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import ROUnaryStruct
from adafruit_tca8418 import TCA8418
import mfrc522
#from examples import read
#import busio


MAX_VOLT = 3.3
POINT_ZERO = MAX_VOLT/2
# Initialize I2C bus
i2c = board.I2C()

# Initialize TCA expander
tca = TCA8418(i2c)

# Mapping keys for keypad
keys = (('*', 0, '#', 'D'),
        (7, 8, 9, 'C'),
        (4, 5, 6, 'B'),
        (1, 2, 3, 'A'))

# Mapping pins for keypad
KEYPADPINS = (
     TCA8418.R0,
     TCA8418.R1,
     TCA8418.R2,
     TCA8418.R3,
     TCA8418.C0,
     TCA8418.C1,
     TCA8418.C2,
     TCA8418.C3,
)

# Loop to enable pins for keypad
for pin in KEYPADPINS:
    tca.keypad_mode[pin] = True
    tca.enable_int[pin] = True
    tca.event_mode_fifo[pin] = True
    

tca.key_intenable = True

# Button to use as interruptor
INPIN = TCA8418.R7
tca.gpio_mode[INPIN] = True
tca.gpio_direction[INPIN] = False
tca.pullup[INPIN] = True

# DHT setup for temp and humidity
dht_pin = board.A2
dht_device = adafruit_dht.DHT11(dht_pin)

# Angles for neoled ring
angles = [0, 45, 90, 135, 180, 225, 270, 315]

# Initialize neoled ring
neoled_ring = neopixel.NeoPixel(board.D9, 8)

# Colors for neoled on board
neoled_colors = {'red': (255, 0, 0),
        'yellow': (255, 255, 0),
        'green': (0, 255, 0)}

# Initialize neopixel for current state
neoPixelEtat = neopixel.NeoPixel(board.NEOPIXEL, 1)

# Initialize joystick controls
x_axis_joystick = analogio.AnalogIn(board.A3)
y_axis_joystick = analogio.AnalogIn(board.A4)
button_joystick = digitalio.DigitalInOut(board.A1)
button_joystick.direction = digitalio.Direction.INPUT
button_joystick.pull = digitalio.Pull.UP
deadzone_radius = 0.1
MAX_X_JOYSTICK = 53639

# Initialize motor pins
pos_pin_motor = board.D6
neg_pin_motor = board.D5

pospwm = pwmio.PWMOut(pos_pin_motor, frequency=1000)
negpwm = pwmio.PWMOut(neg_pin_motor, frequency=1000)

# Initialize motor
motor_one = motor.DCMotor(pospwm, negpwm)

# Initialize servomotor 
patte_servo = pwmio.PWMOut(board.A5, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(patte_servo)

# Sonar
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.TX, echo_pin=board.RX)

# Dictionnary for airports
code_airport = {'101': 'YUL Montreal',
                '111': 'ATL Atlanta',
                '222': 'HND Tokyo',
                '764': 'LHR London',
                '492': 'CAN Baiyun',
                '174': 'CDG Paris',
                '523': 'AMS Amsterdam'}


# Functions declarations
def get_voltage(pin):
    return (pin.value * MAX_VOLT / 65535)

def get_angle_from_x(x_value):
    return (x_value.value / MAX_X_JOYSTICK) * 180

def do_read():
    rdr = mfrc522.MFRC522(board.D12, board.D11, board.D13, board.A0, board.D10)
    rdr.set_antenna_gain(0x07 << 4)
    print("\nPlace card before reader to read card's UID\n")
    try:      
        while True:

            (stat, tag_type) = rdr.request(rdr.REQIDL)
            
            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]), end='\n\n')

                    if rdr.select_tag(raw_uid) == rdr.OK:
                        return raw_uid
                        
                    else:
                        print("Failed to select tag")
    except KeyboardInterrupt:
        print("Bye")

def temperature():
     temperature = dht_device.temperature
     return temperature

def humidity():
    humidity = dht_device.humidity
    return humidity

def joystick_servo():
    angle_servo = get_angle_from_x(x_axis_joystick)
    my_servo.angle = angle_servo
    return angle_servo

def led_ring(x, y):
    if abs(x) < deadzone_radius and abs(y) < deadzone_radius:
        neoled_ring.fill((0,0,0))
        angle_degree = 0
    else:
        angle_degree = math.degrees(math.atan2(y, x)) + 90

        if (angle_degree < 0):
            degree = (angle_degree + 360) % 360
        else:
            degree = angle_degree

        closest_angle_led = min(angles, key=lambda x: abs(x - degree))
        neoled_ring.fill((0,0,0))

        neoled_ring[angles.index(closest_angle_led)] = (0, 0, 32)

        neoled_ring.show()

def motor_range(y, in_min, in_max, out_min, out_max):
     return (y - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def motor():
    voltage = get_voltage(y_axis_joystick)
    
    throttle = ((voltage / 3.3) * 2) - 1
    throttle = max(min(throttle, 1), -1)
    if throttle < 0.1 and throttle > -0.1:
        throttle = 0

    motor_one.throttle = throttle
    return motor_one.throttle

# Définition des états

def etat_1():
    # Actions à effectuer lors de l'entrée dans l'état 1
    neoPixelEtat.fill(neoled_colors['red'])
    uid = None

    temps = time.monotonic()
    while uid == None:
        #uid = do_read()
        print(uid)
        estValide = True
        uid = True
        if uid:
            #print(uid)
            print('Going to etat 2')
            time.sleep(1)
            etat_2()

def etat_2():
    # Actions à effectuer lors de l'entrée dans l'état 2
    neoPixelEtat.fill(neoled_colors['yellow'])
    user_input = ""
    tca.interrupts_enabled = True
    print("Entrez un code a 3 chiffre")
    while True:
        if tca.key_int:
            events = tca.events_count

            for _ in range(events):
                keyevent = tca.next_event
                if keyevent & 0x80:
                    event = keyevent & 0x7F
                    event -= 1
                    row = event // 10
                    col = event % 10
                    pressed = keys[col][row]
                    if pressed != '#' and isinstance(pressed, int):
                        user_input += str(keys[col][row])
                        print(user_input)
                    
                        if len(user_input) == 3:
                            if user_input in code_airport:
                                global nom_airport
                                nom_airport = code_airport[user_input]
                                print(nom_airport)
                                print('Demarrer l\'avion en appuyant sur le bouton')
                                while True:
                                    if tca.input_value[INPIN] == False:
                                        etat_3()
                                    time.sleep(0.1)
                            else:
                                print('code invalide')
                                etat_2()
                    else:
                        user_input = ""
                        print("Going to etat 1")
                        etat_1() 

            tca.key_int = True
            time.sleep(0.5)
   

def etat_3():
    neoPixelEtat.fill(neoled_colors['green'])

    LOCKED_STATE = 0
    UNLOCKED_STATE = 1
    joystick_state = UNLOCKED_STATE

    button_joystick_state = False
    button_joystick_last_state = False

    print_timer = time.monotonic()
    DELAY_PRINT = 0.1
    motor_throttle = 0
    global nom_airport

    while True:
        button_joystick_last_state = button_joystick_state
        button_joystick_state = button_joystick.value


        #print(joystick_state)
        if button_joystick_state == False and button_joystick_last_state == True:
            if joystick_state == LOCKED_STATE:
                joystick_state = UNLOCKED_STATE  
            else:
                joystick_state = LOCKED_STATE
    

        x = (x_axis_joystick.value / 32767) - 1
        y = (y_axis_joystick.value / 32767) - 1

        try:
            humid = humidity()
            temp = temperature()
        except RuntimeError as e:
            humid = 'Erreur'
            temp = 'Erreur'

        if joystick_state == UNLOCKED_STATE:
            angle_servo = joystick_servo()
            my_servo.angle = angle_servo
            led_ring(x, y)
            motor_throttle = motor()
            motor_percent = round(motor_throttle * 100)
            destination = nom_airport
            if print_timer >= DELAY_PRINT:
                print("Moteur: {0} \nServo: {1} \nDestination: {2}\nTemp: {3} \nHumid: {4}\n\n\n".format(motor_percent, int(my_servo.angle), destination, temp, humid))
                print_timer = time.monotonic()
        
        
        try:
            if sonar.distance < 10:
                motor_one.throttle = 0
                led_ring(0, 0)
                my_servo.angle = 90
                print('Distance moins de 10 cm')
                print('Going to etat 1')
                time.sleep(2)
                etat_1()
        except RuntimeError:
            pass
            #print("Retrying!")


        if tca.input_value[INPIN] == False:
            print('Going to etat 1')
            etat_1()


# Boucle principale
def boucle_principale():
    # Initialisation de la machine à états finis
        # Exécution de l'état courant
    print('Going to etat 1')
    etat_1()

# Programme principal
boucle_principale()
    


