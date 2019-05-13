
#Code von:
#https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/

import json
from random import randrange
from time import strftime, gmtime, localtime, sleep
import socket
import grovepi
from grovepi import *
import datetime


#Wird auf dem Raspberry Pi ausgefuehrt
#Muss die ganze Zeit laufen...


#IP = "localhost"
IP = "192.168.2.10"
PORT = 50005

while True:
    try:
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.bind((IP, PORT))
        serv.listen(0)
        print("server lauscht...")
        sock, addr = serv.accept()
        print("Connection from: ", addr)
        while True:
            try:
                # Connect the LED to digital port D4
                # SIG,NC,VCC,GND
                led = 2
                sensor = 4  # The Temp/Humidity-Sensor goes on digital port 4.
                blue = 0  # The Blue colored sensor.
                white = 1  # The White colored sensor.
                # Turn on LED once sensor exceeds threshold resistance
                kontrollwert = 10
                light_sensor = 0

                grovepi.pinMode(light_sensor, "INPUT")
                grovepi.pinMode(led, "OUTPUT")

                light_sensor_value1 = 0
                light_sensor_value0 = grovepi.analogRead(0)  # Get sensor value
                resistance0 = (float)(1023 - light_sensor_value0) * 10 / (
                            light_sensor_value0 + 0.0001)  # Calculate resistance of sensor in K
                light_sensor_value1 = 0
                light_sensor_value1 = grovepi.analogRead(1)
                resistance1 = (float)(1023 - light_sensor_value1) * 10 / (light_sensor_value1 + 0.0001)

                [temp, humidity] = grovepi.dht(sensor, white)
                # if math.isnan(temp) == False and math.isnan(humidity) == False:
                # print("temp = %.02f C humidity =%.02f%%" % (temp, humidity))

                if resistance0 > kontrollwert or resistance1 > kontrollwert:
                    # Send HIGH to switch on LED
                    grovepi.digitalWrite(led, 1)
                else:
                    # Send LOW to switch off LED
                    grovepi.digitalWrite(led, 0)

                camera = 0 #0 = nichts, 1 = Bild erstellen und speichern, 2 = Bild in Dictionary einfuegen
                #Kamera funktioniert noch nicht -> Wohl zu grosse Dateien...
                if camera >= 1:
                    from picamera import PiCamera
                    camera = PiCamera()
                    t = strftime("%Y%m%d_%H%M%S", localtime())
                    q = str("image_"+t+".jpg")
                    camera.capture(q)

                data_sensoren = {}  # Dict wird erstellt
                data_sensoren['lichtsensor_1'] = light_sensor_value0
                data_sensoren['widerstand_1'] = resistance0
                if camera >= 2:
                    with open("image.jpg", "rb") as image:
                        f = image.read()
                        b = bytearray(f)
                    data_sensoren['bild'] = f
                data_sensoren['lichtsensor_2'] = light_sensor_value1
                data_sensoren['widerstand_2'] = resistance1
                data_sensoren['temperatur'] = temp
                data_sensoren['luftfeuchtigkeit'] = humidity
                data_sensoren['time_raspi'] = strftime("%a, %d %b %Y %H:%M:%S", localtime())
                data_sensoren_json = json.dumps(data_sensoren)

                data = data_sensoren_json.encode()
                print("sende folgende daten: " + data)
                sock.send(data)              # Echo received data
                print("daten gesendet")
                break
            except IOError:
                print ("Error")

        sock.close()
        serv.close()
    except Exception as error:
        print("Opps, something is wrong: ", error)


