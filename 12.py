import sys
import sqlite3
import pymongo
from bson.objectid import ObjectId
from pandas import DataFrame
import socket

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["smarthome"]
mycol = mydb["appliances"]
mycol.drop()
mycol = mydb["appliances"]
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
                           "parametroi":[None],
                "entoles":{"anapse":{"entolh_id":ObjectId("5fe24be4a42de2b58e748771"),
                                     "parametroi":None},
                           "sbhse":{"entolh_id":ObjectId("5fe24be4a42de2b58e748782"),
                                    "parametroi":None}}}
     
     
     


     ]
x=mycol.insert_many(my1)
