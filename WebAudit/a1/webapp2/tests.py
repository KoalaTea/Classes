from pymongo import MongoClient
import requests

client = MongoClient
db = client.ChambordPi

drinks = db.Drinks

#TODO test alchohol changes
