from flask import Flask
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine
from oauthlib.oauth2 import WebApplicationClient
import config
import os

app=Flask(__name__)
app.config.from_object(config.Config)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
db=MongoEngine()
db.init_app(app)
socketio=SocketIO()
socketio.init_app(app,cors_allowed_origins="*")
client = WebApplicationClient(app.config.get('GOOGLE_CLIENT_ID'))
from app import routes