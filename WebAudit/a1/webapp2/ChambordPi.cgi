#!flask/bin/python

from wsgrief.handlers import CGIHandler
from app import app

CGIHandler.run(app)
