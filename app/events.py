from app.routes import data
from app import socketio


#Events
@socketio.on('connect')
def test_connect():
    print("SOCKET CONNECTED")

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print("GAME Emote {}".format(json['data']))
    data.append(json)