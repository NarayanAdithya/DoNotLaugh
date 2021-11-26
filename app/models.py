from mongoengine.fields import EmbeddedDocumentField,ReferenceField
import datetime
import json

from app import db

class Game(db.EmbeddedDocument):
    gameID=db.UUIDField(required=True,binary=False)
    userID=db.UUIDField(required=True,binary=False)
    game_score=db.IntField(required=True,default=0)
    created=db.DateTimeField(required=False,default=datetime.datetime.utcnow)

class User(db.Document):
    userID=db.UUIDField(required=True,binary=False)
    username=db.StringField(required=True)
    games=db.ListField(db.EmbeddedDocumentField(Game),required=False,default=[])
    created=db.DateTimeField(required=False,default=datetime.datetime.utcnow)

