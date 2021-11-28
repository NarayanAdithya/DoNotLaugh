from flask import render_template,request,redirect,url_for,jsonify
import random
import pickle
import sys
from app import app
from app.models import Game,User
import uuid
data=[]

@app.route('/',methods=['POST','GET'])
def sign_in():
    if request.method=='POST':
        username=request.form['username']
        if(username==''):
            return render_template('signinnew.html',message="Please Enter a Valid Username")
        u=User()
        u.userID=uuid.uuid4()
        u.username=username
        u.save()
        return redirect(url_for('end',userID=u.userID))
    return render_template('signinnew.html')


@app.route('/home/<userID>')
def end(userID):
    print("SERVER STARTED")
    links=["https://www.youtube.com/embed/o28RANhwb0s","https://www.youtube.com/embed/IxG3Cv5qK00","https://www.youtube.com/embed/EtH9Yllzjcc"]
    a=1
    u=User.objects.get(userID=userID)
    game=Game()
    game.userID=u.userID
    game.gameID=uuid.uuid4()
    u.games.append(game)
    u.save()
    return render_template('index.html',url=links[a],game=game.gameID)


@app.route('/save_details',methods=['POST'])
def save_details():
    body=request.get_json()
    print(body['points'])
    return jsonify({'message':'Success'})


@app.route('/end')
def home_():
    print("SERVER END SAVING DATA")
    return "Saved Successfully"





