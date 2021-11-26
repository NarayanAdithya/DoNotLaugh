from flask import Flask
from flask_socketio import SocketIO
import config
from flask_mongoengine import MongoEngine


app=Flask(__name__)
app.config.from_object(config)
app.config["MONGODB_SETTINGS"] = {'DB': "donotlaugh", "host":'mongodb://adithya:narayan@db:27017/donotlaugh?authSource=admin'}
db=MongoEngine()
db.init_app(app)
socketio=SocketIO()
socketio.init_app(app)
from app import routes,events