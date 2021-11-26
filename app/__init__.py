from flask import Flask
from flask_socketio import SocketIO
import config
from flask_mongoengine import MongoEngine


app=Flask(__name__)
app.config.from_object(config)
db=MongoEngine()
db.init_app(app)
socketio=SocketIO()
socketio.init_app(app)
from app import routes,events