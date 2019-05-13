from pymongo import MongoClient

'''
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

'''

# open MongoDB database and in there the collection
try:
    client = MongoClient('localhost', 27017)
    db = client['wasserfarm']
    collection = db['wasserfarm_03']
    print("connected to", str(db))
except:
    print("could not connect")


mydoc = collection.find().sort('zeiten')


l1 = [] #Zeit
l2 = [] #Lichtsensor 3
l3 = [] #Lichtsensor 2

l4 = [] #Temperatur
l5 = [] #Feuchtigkeit

for x in mydoc:
    print(x)
    l1.append(x['zeiten'])
    l2_wert = x['messungen']['lichtsensor1']
    if l2_wert > -1 and l2_wert < 1200:
        l2.append(l2_wert)
    l3_wert = x['messungen']['lichtsensor2']
    if l3_wert > -1 and l3_wert < 1200:
        l3.append(l3_wert)
    l4.append(x['messungen']['temperatur'])
    l5.append(x['messungen']['luftfeuchtigkeit'])


print(l1)
print(l2)

import matplotlib.pyplot as plt

#Lichtsensoren ausgeben
plt.plot(l1, l2, l3)
plt.grid(True)
plt.xlabel('Datum')
plt.ylabel('Werte der Lichtensoren')
titel_erzeugung = 'Auswertung der Sensoren'
plt.title(titel_erzeugung)
plt.show()

#Lichtsensoren ausgeben
plt.plot(l1, l4, l5)
plt.grid(True)
plt.xlabel('Datum')
plt.ylabel('Werte')
titel_erzeugung = 'Auswertung Temperatur und Luftfeuchtigkeit'
plt.title(titel_erzeugung)
plt.show()




'''
for element in collection.find({"rvalue.val": 5}, {'_id': 0}):
    print("found the entry '5' @: ", element['timestamp'])

'''
