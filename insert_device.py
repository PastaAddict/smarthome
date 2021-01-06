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
         "entoles":{"anapse":{"entolh_id":ObjectId("5fe24be4a42de2b58e74877e"),
                              "parametroi":None},
                    "sbhse":{"entolh_id":ObjectId("5fe24be4a42de2b58e748782"),
                             "parametroi":None}}},
         {"_id":ObjectId("5fd688ab0cc1ed38ec8a7006"),
          "parametroi":["lepta"],
          "entoles":{"anapse":{"entolh_id":ObjectId("5fe24dc2a42de2b58e74877f"),
                               "parametroi":None},
                     "sbhse":{"entolh_id":ObjectId("5fe24e06a42de2b58e748780"),
                              "parametroi":None},
                     "xronometro":{"entolh_id":ObjectId("5fe24e36a42de2b58e748781"),
                                   "parametroi":{"lepta":[0,120]}}}},






         {"_id":ObjectId("5fd688720cc1ed38ec8a7007"),
          "parametroi":["entasi"],
          "entoles":{"anapse":{"entolh_id":ObjectId("5fe24dc2a42de2b58e748773"),
                               "parametroi":None},
                     "sbhse":{"entolh_id":ObjectId("5fe24e06a42de2b58e748786"),
                              "parametroi":None},
                     "fwteinothta":{"entolh_id":ObjectId("5fe24e36a42de2b58e748787"),
                                   "parametroi":{"entasi":[1,100]}}}},



         {"_id":ObjectId("5fd688720cc1ed38ec8a7008"),"parametroi":[None],
         "entoles":{"anapse":{"entolh_id":ObjectId("5fe24be4a42de2b58e748771"),
                              "parametroi":None},
                    "sbhse":{"entolh_id":ObjectId("5fe24be4a42de2b58e748782"),
                             "parametroi":None}}},

          {"_id":ObjectId("5fd688ab0cc1ed38ec8a7009"),
          "parametroi":["aisthitiras"],
          "entoles":{"anapse":{"entolh_id":ObjectId("5fe24dc2a42de2b58e74877e"),
                               "parametroi":None},
                     "sbhse":{"entolh_id":ObjectId("5fe24e06a42de2b58e748783"),
                              "parametroi":None},
                     "synargemos":{"entolh_id":ObjectId("5fe24e36a42de2b58e748784"),
                                   "parametroi":{"aisthitiras":[0,1]}}}},
##
        {"_id":ObjectId("5fd688720cc1ed38ec8a7010"),"parametroi":["entasi"],
         "entoles":{"anapse":{"entolh_id":ObjectId("5fe24be4a42de2b58e748773"),
                             "parametroi":None},
                    "sbhse":{"entolh_id":ObjectId("5fe24be4a42de2b58e748784"),
                            "parametroi":None},
                   "aspro":{"entolh_id":ObjectId("5fe24be4a42de2b58e748785"),
                           "parametroi":None},
                   "mple":{"entolh_id":ObjectId("5fe24be4a42de2b58e748786"),
                            "parametroi":None},"kokkino":{"entolh_id":ObjectId("5fe24be4a42de2b58e748787"),
                            "parametroi":None},"prasino":{"entolh_id":ObjectId("5fe24be4a42de2b58e748788"),
                            "parametroi":None},"kitrino":{"entolh_id":ObjectId("5fe24be4a42de2b58e748789"),
                             "parametroi":None},"mov":{"entolh_id":ObjectId("5fe24be4a42de2b58e748791"),
                            "parametroi":None},
                    "ntisko":{"entolh_id":ObjectId("5fe24be4a42de2b58e748792"),
                            "parametroi":{"entasi":[1,100]}},
                   "fwteinothta":{"entolh_id":ObjectId("5fe24e36a42de2b58e748719"),
                                   "parametroi":{"entasi":[1,100]}}}},
         {"_id":ObjectId("5fd688ab0cc1ed38ec8a7011"),
          "parametroi":["entasi"],
          "entoles":{"anapse":{"entolh_id":ObjectId("5fe24dc2a42de2b58e74871e"),
                               "parametroi":None},
                     "sbhse":{"entolh_id":ObjectId("5fe24e06a42de2b58e741783"),
                              "parametroi":None},
                     "fwteinotita":{"entolh_id":ObjectId("5fe24e36a12de2b58e748784"),
                                   "parametroi":{"entasi":[0,100]}}}}

     ]
    #inserting them to mongo db
x=mycol.insert_many(my1)

    ##creating devices in sql db if they dont exist
conn = sqlite3.connect(r"C:\Users\Zisis\Desktop\check\Smart11.db") #connect to local sqlite database
cursor = conn.cursor()
    #my1={},{"_id":1}
a=mycol1.find({},{ "_id": 1})


    #initialize devices to sql database
    #if they already exists then nothing happens to the sql
cursor.execute("""INSERT OR IGNORE INTO syskeyi(device_id,eidos,dwmatio,energi,kwh)
              VALUES('5fd688ab0cc1ed38ec8a7006','thermosifwnas','mpanio',false,0.33);""")
conn.commit()
cursor.execute("""INSERT OR IGNORE INTO syskeyi(device_id,eidos,dwmatio,energi,kwh)
              VALUES('5fd688720cc1ed38ec8a7005','mprizes','kouzina',false,0.0001);""")
conn.commit()

cursor.execute("""INSERT OR IGNORE INTO syskeyi(device_id,eidos,dwmatio,energi,kwh)
              VALUES('5fd688720cc1ed38ec8a7007','lampa1','kouzina',false,0.05);""")
conn.commit()

cursor.execute("""INSERT OR IGNORE INTO syskeyi(device_id,eidos,dwmatio,energi,kwh)
              VALUES
             ('5fd688720cc1ed38ec8a7008','mprizes1','saloni',false,0.0001);""")
conn.commit()

cursor.execute("""INSERT OR IGNORE INTO syskeyi(device_id,eidos,dwmatio,energi,kwh)
              VALUES('5fd688ab0cc1ed38ec8a7009','synargemos','eisodo',false,0.0001);""")
conn.commit()

cursor.execute("""INSERT OR IGNORE INTO syskeyi(device_id,eidos,dwmatio,energi,kwh)
              VALUES('5fd688720cc1ed38ec8a7010','lampa2','dwmatio1',false,0.005);""")
conn.commit()

    #in case there is a device in mongo and not in sql database
    #we insert the device from mongo to sql in a default device
for i in mycol1.find({},{ "_id": 1}):
    print(i)
    b=i.get('_id')
    c=str(b)
    b=(str(b),)

    cursor.execute("""INSERT OR IGNORE INTO syskeyi(device_id,eidos,dwmatio,energi,kwh)
              VALUES(?,'lampa2','kouzina',false,0.002);""",b)
    conn.commit()
