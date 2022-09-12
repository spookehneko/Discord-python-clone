from .database import init, User, Message, ServerInfo, ServerMember, ServerTextChannel, PersonalMessage
init()

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

from .libs import jwtHelpers

app = Flask(__name__)
CORS(app)


# uid = User.addUser("E@gmail.com","123", "hot boy")
# sid = ServerInfo.createServer('naruto server')
# ServerMember.addMember(1, 1)
# ServerTextChannel.createTextChannel("general chat", 1)
mid = Message.createMessage("Hi", 1)
PersonalMessage.sendDM(1,3,mid)

@app.get('/')
def root():
    return "Yo Yo bantai!"

@app.post('/register_user')
def registerUser():
    req_data = request.get_json()
    username = req_data['username']
    email = req_data['email']
    password = req_data['password']

    uid = User.addUser(email, password, username)

    token = jwtHelpers.sign({
        "uid" : uid
    })

    resp = jsonify({
        "message" : "User has been created",
    })
    resp.set_cookie("token", token)
    
    return resp, 200

@app.post('/login_user')
def loginUser():
    req_data = request.get_json()
    email = req_data['email']
    password = req_data['password']

    isValid = User.checkPassword(email, password)
    if(not isValid): raise Exception("Password is not correct")
    
    uid = User.getUID(email)
    token = jwtHelpers.sign({
        "uid" : uid
    })

    resp = jsonify({
        "message" : "Login Successfull"
    })
    
    resp.set_cookie("token", token)

    return resp, 200



