from werkzeug.security import check_password_hash
from .db import db

class User():

    def __init__(self, user_json):
        self.username = user_json['username']
        self.credits = user_json['credits']
        self.roles = user_json['roles']

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymouse(self):
        return False

    def get_id(self):
        return self.username

    def is_role(self, role):
        return(role in self.roles)

    def purchase(self, credits):
        #look up how to lock the database
        self.credits -= credits
        db.Users.update({
            'username': self.username
        },{
            '$set': {'credits': existing - credits }
        }, upsert=False)


    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)
