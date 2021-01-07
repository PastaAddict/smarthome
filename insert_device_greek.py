import sys
import sqlite3
import pymongo
from bson.objectid import ObjectId
from pandas import DataFrame
import socket



  ###---connecting python to mongo db
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["smarthome"]
mycol1 = mydb["appliances"]
mycol1.drop()
mycol = mydb["appliances"]
#initialize devices to mongodb
my1=[{"_id":ObjectId("5fd688720cc1ed38ec8a7005"),"parametroi":[None],
         "entoles":{"Turn on":{"entolh_id":ObjectId("5fe24be4a42de2b58e74877e"),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId("5fe24be4a42de2b58e748782"),
                             "parametroi":None}}},
         {"_id":ObjectId("5fd688ab0cc1ed38ec8a7006"),
          "parametroi":["lepta"],
          "entoles":{"Turn on":{"entolh_id":ObjectId("5fe24dc2a42de2b58e74877f"),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId("5fe24e06a42de2b58e748780"),
                              "parametroi":None},
                     "xronometro":{"entolh_id":ObjectId("5fe24e36a42de2b58e748781"),
                                  "parametroi":{"lepta":[0,120]}}}}





,
         {"_id":ObjectId("5fd688720cc1ed38ec8a7007"),
          "parametroi":["entasi"],
          "entoles":{"Turn on":{"entolh_id":ObjectId("5fe24dc2a42de2b58e748773"),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId("5fe24e06a42de2b58e748786"),
                              "parametroi":None},
                     "fwteinothta":{"entolh_id":ObjectId("5fe24e36a42de2b58e748787"),
                                   "parametroi":{"entasi":[1,100]}}}},



         {"_id":ObjectId("5fd688720cc1ed38ec8a7008"),"parametroi":[None],
         "entoles":{"Turn on":{"entolh_id":ObjectId("5fe24be4a42de2b58e748771"),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId("5fe24be4a42de2b58e748782"),
                             "parametroi":None}}},
     
       {"_id":ObjectId("5fd688ab0cc1ed38ec8a7009"),
          "parametroi":["detect"],
          "entoles":{"Turn on":{"entolh_id":ObjectId("5fe24dc2a42de2b58e748773"),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId("5fe24e06a42de2b58e748786"),
                              "parametroi":None},
                     "alarm":{"entolh_id":ObjectId("5fe24e36a42de2b58e748787"),
                                   "parametroi":{"detect":[0,1]}}}},



        {"_id":ObjectId("5fd688720cc1ed38ec8a7010"),"parametroi":["entasi"],
         "entoles":{"Turn on":{"entolh_id":ObjectId("5fe24be4a42de2b58e748773"),
                              "parametroi":None},
                    "Turn off":{"entolh_id":ObjectId("5fe24be4a42de2b58e748784"),
                             "parametroi":None},
                   "aspro":{"entolh_id":ObjectId("5fe24be4a42de2b58e748785"),
                            "parametroi":{"entasi":[1,100]}},
                   "mple":{"entolh_id":ObjectId("5fe24be4a42de2b58e748786"),
                            "parametroi":{"entasi":[1,100]}},
                    "kokkino":{"entolh_id":ObjectId("5fe24be4a42de2b58e748787"),
                            "parametroi":{"entasi":[1,100]}},
                    "prasino":{"entolh_id":ObjectId("5fe24be4a42de2b58e748788"),
                             "parametroi":{"entasi":[1,100]}}},
                    "kitrino":{"entolh_id":ObjectId("5fe24be4a42de2b58e748789"),
                              "parametroi":{"entasi":[1,100]}},
                    "mov":{"entolh_id":ObjectId("5fe24be4a42de2b58e748791"),
                            "parametroi":{"entasi":[1,100]}},
                    "ntisko":{"entolh_id":ObjectId("5fe24be4a42de2b58e748792"),
                            "parametroi":{"entasi":[1,100]}},
                   "fwteinothta":{"entolh_id":ObjectId("5fe24e36a42de2b58e748719"),
                                   "parametroi":{"entasi":[1,100]}}},
     
         {"_id":ObjectId("5fd688ab0cc1ed38ec8a7011"),
          "parametroi":["entasi"],
          "entoles":{"Turn on":{"entolh_id":ObjectId("5fe24dc2a42de2b58e74871e"),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId("5fe24e06a42de2b58e741783"),
                              "parametroi":None},
                     "fwteinotita":{"entolh_id":ObjectId("5fe24e36a12de2b58e748784"),
                                   "parametroi":{"entasi":[0,100]}}}},
         
         {"_id":ObjectId("5fd688ab0cc1ed38ec8a7012"),
          "parametroi":["entasi"],
          "entoles":{"Turn on":{"entolh_id":ObjectId("5fe24dc2a42de2b58e74871e"),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId("5fe24e06a42de2b58e741783"),
                              "parametroi":None},
                     "auto":{"entolh_id":ObjectId("5fe24e04a42de2b58e741783"),
                              "parametroi":None},
                     "cool":{"entolh_id":ObjectId("5fe24e02a42de2b58e741783"),
                              "parametroi":None},
                     "heat":{"entolh_id":ObjectId("5fe21e06a42de2b58e741783"),
                              "parametroi":None},
                     "dry":{"entolh_id":ObjectId("1fe24e06a42de2b58e741783"),
                              "parametroi":None},
                     "fan":{"entolh_id":ObjectId("5fe24e06a42de2b18e741783"),
                              "parametroi":None},
                     "economy":{"entolh_id":ObjectId("5fe24e06a41de2b58e741783"),
                              "parametroi":None},
                     "fan speed":{"entolh_id":ObjectId("5fe24e06a12de2b58e741783"),
                              "parametroi":{"entasi":[0,3]}},
                     "swing":{"entolh_id":ObjectId("5fe24e06a42de1b58e741783"),
                              "parametroi":None},
                     "swing range":{"entolh_id":ObjectId("5fe14e06a42de2b58e741783"),
                              "parametroi":{"entasi":[0,4]}},
                     
                     "thermokrasia":{"entolh_id":ObjectId("1fe24e36a11de2b58e748784"),
                                   "parametroi":{"entasi":[15,30]}}}},
     {"_id":ObjectId("5fd688ab0cc1ed38ec8a7013"),
          "parametroi":["entasi"],
          "entoles":{"Turn on":{"entolh_id":ObjectId("1fe24dc2a12de2b58e74871e"),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId("1fe24e06a41de2b58e741783"),
                              "parametroi":None},
                     "fwteinotita":{"entolh_id":ObjectId("1fe24e16a12de2b58e748784"),
                                   "parametroi":{"entasi":[0,100]}}}},
     {"_id":ObjectId("5fd688ab0cc1ed38ec8a7014"),
          "parametroi":["entasi"],
          "entoles":{"Turn on":{"entolh_id":ObjectId("1fe21dc2a12de2b18e74871e"),
                               "parametroi":None},
                     "Turn off":{"entolh_id":ObjectId("1fe22e06a41de2b28e741783"),
                              "parametroi":None},
                     "fwteinotita":{"entolh_id":ObjectId("1ae22e26a12de2b58e748784"),
                                   "parametroi":{"entasi":[0,100]}}}}
         

     ]
    #inserting them to mongo db
x=mycol.insert_many(my1)

    ##creating devices in sql db if they dont exist
conn = sqlite3.connect(r"C:\Users\Zisis\Downloads\smarthome-greek (2)\smarthome-greek\smarthome.db") #connect to local sqlite database
cursor = conn.cursor()
    #my1={},{"_id":1}
a=mycol1.find({},{ "_id": 1})


    #initialize devices to sql database
    #if they already exists then nothing happens to the sql
cursor.execute("""INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh)
              VALUES('5fd688ab0cc1ed38ec8a7006','θερμοσίφωνας','μπάνιο',false,0.33);""")
conn.commit()
cursor.execute("""INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh)
              VALUES('5fd688720cc1ed38ec8a7005','μπρίζες','κουζίνα',false,0.0001);""")
conn.commit()

cursor.execute("""INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh)
              VALUES('5fd688720cc1ed38ec8a7007','λαμπα1','κουζίνα',false,0.05);""")
conn.commit()

cursor.execute("""INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh)
              VALUES
             ('5fd688720cc1ed38ec8a7008','μπρίζες1','σαλόνι',false,0.0001);""")
conn.commit()

cursor.execute("""INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh)
              VALUES('5fd688ab0cc1ed38ec8a7009','συναργεμός','είσοδο',false,0.02);""")
conn.commit()

cursor.execute("""INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh)
              VALUES('5fd688720cc1ed38ec8a7010','λάμπα12','δωμάτιο1',false,0.005);""")
conn.commit()

cursor.execute("""INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh)
              VALUES('5fd688ab0cc1ed38ec8a7012','air-condition1','σαλόνι',false,2.0);""")
conn.commit()
#INSERT INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh)


    #in case there is a device in mongo and not in sql database
    #we insert the device from mongo to sql in a default device
for i in mycol1.find({},{ "_id": 1}):
    print(i)
    b=i.get('_id')
    c=str(b)
    b=(str(b),)
    cursor.execute("""SELECT (count(device_id)+1)
        FROM Συσκευή
            WHERE είδος like '%λάμπα%'""")
    a=cursor.fetchone()
    name='λάμπα'+str(a[0])
    cursor.execute("""INSERT OR IGNORE INTO Συσκευή(device_id,είδος,δωμάτιο,ενεργή,KWh)
              VALUES(?,"""+"'"+name+"'"+""",'κουζίνα',false,0.002);""",b)
    conn.commit()
