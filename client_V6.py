
#WICHTIG:
#Server bereits gestartet?

import socket
from pymongo import MongoClient
from time import strftime, gmtime, localtime, sleep
from random import randrange

while True:

    #Einstellungen
    anzeige = 2 #0 für aus, 1 für wichtiges, 2 für zusätzliches.

    #IP = "localhost" “War für Tests
    IP = "192.168.2.10"
    PORT = 50005

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        # send only once
        sock.send(b"Kontaktaufnahme mit Wasserfarm")
        # wait for received data
        # Ab hier eigener Code
        data = ''
        data_part = ''
        while True:
            data_part = sock.recv(1024)
            if len(data_part) <= 0:
                sock.close()
                break
            data += data_part.decode("utf-8")
        print("Erhalten: "+data)
        if anzeige >= 1:
            print(type(data)) #ADG
            print(data) #ADG
    except Exception as error:
        print("Opps, something is wrong: ", error)

    #Zuerst Bytes in Str umwandeln.
    data_str = data
    if anzeige >= 2:
        print(data_str)
        print(type(data_str))

    #Jetzt Str in JSON (=dict) umwandeln
    import json
    data_json = json.loads(data_str)
    if anzeige >= 2:
        print(data_json)
        print(type(data_json))

    #Jetzt ein bisschen schlau ausgeben.

    if anzeige >= 2:
        print("Zeit: "+data_json['time_raspi'])
        print("Lichtsensor 1: "+str(data_json['lichtsensor_1']))
        print("Lichtsensor 2: "+str(data_json['lichtsensor_2']))

    #
    #Daten an MongoDB weitergeben!
    #


    # open MongoDB database and in there the collection
    try:
        client = MongoClient('localhost', 27017)
        db = client['wasserfarm']
        collection = db['wasserfarm_03']
        print("connected to", str(db))
    except:
        print("could not connect")

    # generate a couple entries

    for n in range(1):
        eintrag = {}
        timerasp = data_json['time_raspi']
        timetext = strftime("%a, %d %b %Y %H:%M:%S", localtime())
        # print(timetext)
        messung = {}

        # Verschiedene dicts mit Daten generieren

        messung['random'] = randrange(100000, 999999, 1)
        messung['lichtsensor1'] = data_json['lichtsensor_1']
        messung['lichtsensor2'] = data_json['lichtsensor_2']
        messung['widerstand1'] = data_json['widerstand_1']
        messung['widerstand2'] = data_json['widerstand_2']
        messung['temperatur'] = data_json['temperatur']
        messung['luftfeuchtigkeit'] = data_json['luftfeuchtigkeit']

        # Objekt mit Zeitstempel + Daten generieren
        eintrag['zeiten'] = timetext  # Zeitstempel -> 1 Wert!
        eintrag['messungen'] = messung  # Objekt mit 2 dicts (aus Werte generieren)
        if anzeige >= 2:
            print(eintrag)

        result = collection.insert_one(eintrag)
        if anzeige >= 1:
            print('One post: {0}'.format(result.inserted_id))
        sleep(randrange(1, 5, 1))

    #
    # Ab hier geht's um's Finden
    #

    for element in collection.find({"rvalue.val": 5}, {'_id': 0}):
        print("found the entry '5' @: ", element['timestamp'])

    sleep(5)



