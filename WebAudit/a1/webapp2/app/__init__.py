from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config')

from flask_login import LoginManager

lm = LoginManager()
lm.session_protection = 'strong'
lm.login_view = 'login'
lm.init_app(app)

def create_app(config_name):
    lm.init_app(app)

from app import views
