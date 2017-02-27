#!flask/bin/python
from pymongo import MongoClient

client = MongoClient()
db = client.ChambordPi

drinks = db.Drinks
alchohol = db.Alchohol
users = db.Users
orders = db.Orders
mixers = db.Mixers
beer = db.Beer
past_orders = db.PastOrders

backup_file = open("backups/db_backup", "w")

backup_file.write("Drinks\n")
backups = drinks.find()
for index in backups:
    backup_file.write(str(index))

backup_file.write("\nAlchohol\n")
backups = alchohol.find()
for index in backups:
    backup_file.write(str(index))

backup_file.write("\nUsers\n")
backups = users.find()
for index in backups:
    backup_file.write(str(index))

backup_file.write("\nPastOrders\n")
backups = past_orders.find()
for index in backups:
    backup_file.write(str(index))
