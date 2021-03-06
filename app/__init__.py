from flask import Flask
from flask_mongoengine import MongoEngine
from oauthlib.oauth2 import WebApplicationClient
import config
import os

app = Flask(__name__)
app.config.from_object(config.Config)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
db = MongoEngine()
db.init_app(app)
client = WebApplicationClient(app.config.get('GOOGLE_CLIENT_ID'))
from app import routes
