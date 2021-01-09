import sys
import sqlite3
import pymongo
from bson.objectid import ObjectId


conn = sqlite3.connect(r"smarthome.db") #connect to local sqlite database
cursor = conn.cursor() #initialize cursor, used to execute queries

client = pymongo.MongoClient('localhost', 27017) #connect to local mongodb server
db = client['smarthome'] #connect to smarthome database


mongo_appliances=[
    {"_id":ObjectId(),
          "parametroi":["Minutes"],
          "entoles":{"Turn on":{"entolh_id":ObjectId(),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Timer":{"entolh_id":ObjectId(),
                                  "parametroi":{"Minutes":[0,120]}}}},

    {"_id":ObjectId(),"parametroi":["Current consumption"],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None}}},
    
         {"_id":ObjectId(),
          "parametroi":["Brightness"],
          "entoles":{"Turn on":{"entolh_id":ObjectId(),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Brightness":{"entolh_id":ObjectId(),
                                   "parametroi":{"Brightness":[1,100]}}}},


     
       {"_id":ObjectId(),
          "parametroi":["Intruder detected","Number to call on emergency","On Hours"],
          "entoles":{"Turn on":{"entolh_id":ObjectId(),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Set ON Hours":{"entolh_id":ObjectId(),
                                   "parametroi":{"Start Hours":[1,24], "Start Minutes":[0,59], "End Hours":[1,24], "End Minutes":[0,59]}},
                     "Set emergency call":{"entolh_id":ObjectId(),
                                   "parametroi":{"Number1":[0,9], "Number2":[0,9], "Number3":[0,9], "Number4":[0,9], "Number5":[0,9], "Number6":[0,9], "Number7":[0,9], "Number8":[0,9], "Number9":[0,9], "Number10":[0,9]}} }},


         
         {"_id":ObjectId(),
          "parametroi":["Dry on", "Cool on", "Heat on", "Fan on", "Economy on", "Fan speed", "Swing on", "Swing range", "Desired Temperature", "Envirnoment Temperature"],
          "entoles":{"Turn on":{"entolh_id":ObjectId(),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Auto":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Cool":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Heat":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Dry":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Fan":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Economy":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Fan speed":{"entolh_id":ObjectId(),
                              "parametroi":{"entasi":[0,3]}},
                     "Swing":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Swing range":{"entolh_id":ObjectId(),
                              "parametroi":{"entasi":[0,4]}},
                     
                     "Temperature":{"entolh_id":ObjectId(),
                                   "parametroi":{"entasi":[15,30]}}}},
     

#lock
{"_id":ObjectId(),"parametroi":["Locked", "Violation attempt"],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Lock or Unlock":{"entolh_id":ObjectId(),
                             "parametroi":{"Set Lock":[0,1]}}}},

#router
{"_id":ObjectId(),"parametroi":["Network status", "Current users connected"],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Show connected devices":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Set max concurrent devices":{"entolh_id":ObjectId(),
                             "parametroi":{"Set max devices":[0,10]}}}},


#security camera
{"_id":ObjectId(),"parametroi":["Feed"],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Watch feed":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Screenshot":{"entolh_id":ObjectId(),
                             "parametroi":None}}},



#thermostat
{"_id":ObjectId(),"parametroi":["Comfort on", "Desired Temperature", "Environmental Temperature" ],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Comfort":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Economy":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Temperature":{"entolh_id":ObjectId(),
                             "parametroi":{"Temperature":[15,30]}}}},


#oven
{"_id":ObjectId(),"parametroi":["Mati 1 Temperature", "Mati 2 Temperature", "Mati 3 Temperature", "Mati 4 Temperature", "Oven Temperature", "Oven Timer"],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Mati 1":{"entolh_id":ObjectId(),
                              "parametroi":{"temp":[0,9]}},
                    "Mati 2":{"entolh_id":ObjectId(),
                              "parametroi":{"temp":[0,9]}},
                    "Mati 3":{"entolh_id":ObjectId(),
                              "parametroi":{"temp":[0,9]}},
                    "Mati 4":{"entolh_id":ObjectId(),
                              "parametroi":{"temp":[0,9]}},
                    "Oven temperature":{"entolh_id":ObjectId(),
                             "parametroi":{"temp":[0,250]}},
                    "Oven timer":{"entolh_id":ObjectId(),
                             "parametroi":{"Minutes":[1,180]}}}},

#vacuum
{"_id":ObjectId(),"parametroi":["Mode"],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Scan room":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Silent Mode":{"entolh_id":ObjectId(),
                             "parametroi":{"Silent mode On/Off":[0,1]}}}},

#sprinkler controller
{"_id":ObjectId(),"parametroi":[None],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None}}},


#hxeia2
{"_id":ObjectId(),
          "parametroi":["Speaker volume", "Device connected"],
          "entoles":{"Turn on":{"entolh_id":ObjectId(),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Connect with current device":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "Volume":{"entolh_id":ObjectId(),
                                   "parametroi":{"Volume":[0,100]}}}}

         

     ]

sql_appliances = [
'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Θερμοσίφωνας','Μπάνιο',false,0.33);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Μπρίζες','Κουζίνα',false,0.0001);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Λάμπα','Κουζίνα',false,0.05);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Συναργερμός','Είσοδος',false,0.02);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Αir-condition','Σαλόνι',false,2.0);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Κλειδαριά','Είσοδος',false,0.001);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Router','Χωλ',false,0.8);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Security cam','Είσοδος',false,0.8);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Θερμοστάτης','Χωλ',false,0.002);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Φούρνος','Κουζίνα',false,2.4);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Σκούπα','Σαλόνι',false,0.5);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Σύστημα ποτίσματος','Κήπος',false,0.5);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Ηχεία','Υπνοδωμάτιο',false,0.3);''']

appliance_names = ['θερμοσίφωνας', 'μπρίζες', 'λαμπα', 'συναργεμός', 'air-condition', 'κλειδαριά', 'router', 'security cam', 'thermostat', 'φούρνος', 'σκούπα', 'sprinkler system', 'ηχεία']

appliances = {appliance_names[i]:(mongo_appliances[i],sql_appliances[i]) for i in range(len(appliance_names))}

for i,j in enumerate(appliances.keys()):
    print(i,':',j)

print('appliances on sale, select appliances by typing the numbers of the appliances you want seperated by spaces, each appliance once')

selection = map(int, input().split())

appliances_selected = [(mongo_appliances[i],sql_appliances[i]) for i in selection]

for i in appliances_selected:
    db.appliances.insert_one(i[0])
    _id = str(db.appliances.find_one({},sort=[( '_id', pymongo.DESCENDING )])['_id'])
    cursor.execute(i[1],(_id,))
    conn.commit()

