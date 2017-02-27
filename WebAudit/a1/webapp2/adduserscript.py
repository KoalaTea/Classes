#!flask/bin/python
from pymongo import MongoClient, ASCENDING
from werkzeug.security import generate_password_hash
import getpass

username = input("Username: ")
password = getpass.getpass()

client = MongoClient()
db = client.ChambordPi

users = db.Users
users.insert_one(
        {
            "username" : username,
            "password" : generate_password_hash(password),
            "credits" : 500,
            "roles" : [ "user" ],
            "drinksOrdered" : 0
        }
)
