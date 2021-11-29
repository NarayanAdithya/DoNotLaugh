from flask import render_template,request,redirect,url_for,jsonify
from app import app, client
from app.models import Game,User
import uuid
import requests
import json

def get_google_provider_cfg():
    return requests.get(app.config.get('GOOGLE_DISCOVERY_URL')).json()

@app.route('/login')
def google_login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri= 'http://127.0.0.1:8000/login' + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)  

@app.route("/login/callback")
def callback():
    code = request.args.get("code") 
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code
    )
    token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(app.config.get('GOOGLE_CLIENT_ID'), app.config.get('GOOGLE_CLIENT_SECRET')),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    print(userinfo_response)
    unique_id = userinfo_response.json()["sub"]
    users_email = userinfo_response.json()["email"]
    picture = userinfo_response.json()["picture"]
    users_name = userinfo_response.json()["given_name"]
    if not userinfo_response.json()['email_verified']:
        return redirect(url_for('home'))
    if len(User.objects(username=users_email.split('@')[0]))!=0:
        u = User.objects.get(username = users_email.split('@')[0])
        return redirect(url_for('game',userID=u.userID))
    print(users_email,picture,users_name)
    u=User()
    u.username = users_email.split('@')[0]
    u.userID = uuid.uuid4()
    u.status = "perm"
    u.save()
    return redirect(url_for('game',userID=u.userID))




@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        username=request.form['username']
        if(username==''):
            return render_template('signinnew.html',message="Please Enter a Valid Username")
        print(User.objects(username=username))
        if len(User.objects(username=username))!=0:
            return render_template('signinnew.html',message="Player Already Exists")
        u=User()
        u.userID=uuid.uuid4()
        u.username=username
        u.save()
        return redirect(url_for('game',userID=u.userID))
    return render_template('signinnew.html')


@app.route('/home/<userID>')
def game(userID):
    print("SERVER STARTED")
    links=["https://www.youtube.com/embed/o28RANhwb0s?controls=0&autoplay=1","https://www.youtube.com/embed/IxG3Cv5qK00","https://www.youtube.com/embed/EtH9Yllzjcc"]
    a=0
    u=User.objects.get(userID=userID)
    print(u)
    game=Game()
    game.userID=u.userID
    game.gameID=uuid.uuid4()
    u.games.append(game)
    u.save()
    return render_template('index.html',url=links[a],game=game,user=u)


@app.route('/save_details',methods=['POST'])
def save_details():
    body=request.get_json()
    print(body['points'])
    print(body['game'])
    print(body['user'])
    u=User.objects.get(userID=body['user'])
    last_game=u.games[-1]
    print(last_game)
    last_game.game_score=body['points']
    u.save()
    return jsonify({'message':'Success'})

@app.route('/end/<gameID>/<userID>')
def end(gameID,userID):
    u=User.objects.get(userID=userID)
    if u.status == 'temp':
        score = u.games[-1].game_score
        username = u.username
        u.delete()
    else:
        score = u.games[-1].game_score
        username = u.username
    return render_template('end_game.html',username=username,score=score)




