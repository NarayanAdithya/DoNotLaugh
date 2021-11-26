from app.routes import data
from app import socketio


#Events
@socketio.on('connect')
def test_connect():
    print("SOCKET CONNECTED")

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print("GAME ID {}".format(json['game']))
    data.append(json)