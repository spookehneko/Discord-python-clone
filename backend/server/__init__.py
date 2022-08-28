from .database import init, User
init()

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

from .libs import jwtHelpers

app = Flask(__name__)
CORS(app)

@app.get('/')
def root():
    return "Yo Yo bantai!"

@app.post('/register_user')
def registerUser():
    req_data = request.get_json()
    email = req_data['email']
    password = req_data['password']

    uid = User.addUser(email, password)

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



