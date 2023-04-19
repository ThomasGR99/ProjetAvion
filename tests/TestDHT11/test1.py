import board
import adafruit_dht
import time

dht_pin = board.D5
dht_device = adafruit_dht.DHT11(dht_pin)

last_temp_values = []
last_humidity_values = []

while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        last_temp_values.append(temperature)
        last_humidity_values.append(humidity)

        if len(last_temp_values) > 10:
            last_temp_values.pop(0)
        if len(last_humidity_values) > 10:
            last_humidity_values.pop(0)

        avg_temp = sum(last_temp_values) / len(last_temp_values)
        avg_humidity = sum(last_humidity_values) / len(last_humidity_values)
        
        print("Temp: {:.1f} °C \t Humidity: {}% \t Avg Temp: {:.1f} °C \t Avg Humidity: {}%".format(temperature, humidity, avg_temp, avg_humidity))
    except RuntimeError as e:
        print("Lecture impossible.", e.args)
    time.sleep(1)