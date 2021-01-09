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
          "parametroi":["lepta"],
          "entoles":{"Turn on":{"entolh_id":ObjectId(),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "xronometro":{"entolh_id":ObjectId(),
                                  "parametroi":{"lepta":[0,120]}}}},

    {"_id":ObjectId(),"parametroi":[None],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None}}},
    
         {"_id":ObjectId(),
          "parametroi":["entasi"],
          "entoles":{"Turn on":{"entolh_id":ObjectId(),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "fwteinothta":{"entolh_id":ObjectId(),
                                   "parametroi":{"entasi":[1,100]}}}},


     
       {"_id":ObjectId(),
          "parametroi":["detect"],
          "entoles":{"Turn on":{"entolh_id":ObjectId(),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "alarm":{"entolh_id":ObjectId(),
                                   "parametroi":{"detect":[0,1]}}}},


         
         {"_id":ObjectId(),
          "parametroi":["entasi"],
          "entoles":{"Turn on":{"entolh_id":ObjectId(),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "auto":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "cool":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "heat":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "dry":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "fan":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "economy":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "fan speed":{"entolh_id":ObjectId(),
                              "parametroi":{"entasi":[0,3]}},
                     "swing":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "swing range":{"entolh_id":ObjectId(),
                              "parametroi":{"entasi":[0,4]}},
                     
                     "thermokrasia":{"entolh_id":ObjectId(),
                                   "parametroi":{"entasi":[15,30]}}}},
     

#kleidaria
{"_id":ObjectId(),"parametroi":[None],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None}}},

#router
{"_id":ObjectId(),"parametroi":[None],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None}}},


#security camera
{"_id":ObjectId(),"parametroi":[None],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "watch feed":{"entolh_id":ObjectId(),
                             "parametroi":None}}},



#thermostat
{"_id":ObjectId(),"parametroi":["temp"],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Comfort":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Economy":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Temperature":{"entolh_id":ObjectId(),
                             "parametroi":{"temp":[15,50]}}}},


#oven
{"_id":ObjectId(),"parametroi":["temp"],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "mati1":{"entolh_id":ObjectId(),
                              "parametroi":{"temp":[0,9]}},
                    "mati2":{"entolh_id":ObjectId(),
                              "parametroi":{"temp":[0,9]}},
                    "mati3":{"entolh_id":ObjectId(),
                              "parametroi":{"temp":[0,9]}},
                    "mati4":{"entolh_id":ObjectId(),
                              "parametroi":{"temp":[0,9]}},
                    "temp fournoi":{"entolh_id":ObjectId(),
                             "parametroi":{"temp":[0,9]}}}},

#vacuum
{"_id":ObjectId(),"parametroi":[None],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None},
                    "Scan room":{"entolh_id":ObjectId(),
                             "parametroi":None}}},

#sprinkler controller
{"_id":ObjectId(),"parametroi":[None],
         "entoles":{"Turn on":{"entolh_id":ObjectId(),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId(),
                             "parametroi":None}}},


#hxeia2
{"_id":ObjectId(),
          "parametroi":["entasi"],
          "entoles":{"Turn on":{"entolh_id":ObjectId(),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId(),
                              "parametroi":None},
                     "volume":{"entolh_id":ObjectId(),
                                   "parametroi":{"entasi":[0,100]}}}}

         

     ]

sql_appliances = [
'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'θερμοσίφωνας','Μπάνιο',false,0.33);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'μπρίζες','Κουζίνα',false,0.0001);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'λάμπα','Κουζίνα',false,0.05);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'συναργερμός','Είσοδος',false,0.02);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'air-condition','Σαλόνι',false,2.0);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'κλειδαριά','Είσοδος',false,0.001);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'router','Χωλ',false,0.8);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'security cam','Είσοδος',false,0.8);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'θερμοστάτης','Χωλ',false,0.002);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'φούρνος','Κουζίνα',false,2.4);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'σκούπα','Σαλόνι',false,0.5);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'Σύστημα ποτίσματος','Κήπος',false,0.5);''',

'''INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh) VALUES(?,'ηχεία','Υπνοδωμάτιο',false,0.3);''']

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
