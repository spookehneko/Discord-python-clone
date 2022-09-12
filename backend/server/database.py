from asyncio import create_task
from operator import ge
import os
from flask import current_app as app
from mysql import connector
import bcrypt
from mysql.connector import cursor_cext
from .libs import utils

global db

def init():
 global db
 
 print("INITIALIZING DB")

 db = connector.connect(
  host=os.environ["DB_HOST"],
  user=os.environ["DB_USER"],
  password=os.environ["DB_PASSWORD"],
  port=os.environ["DB_PORT"],
  database=os.environ["DB_NAME"]
 )

 User.create_table()
 Message.create_table()
 ServerInfo.create_table()
 ServerMember.create_table()
 ServerTextChannel.create_table()
 PersonalMessage.create_table()

 print("Connected to Database!")

def getDB() -> connector.CMySQLConnection:
 global db

 if(isinstance(db,connector.CMySQLConnection) and not db.is_connected()): 
  db.reconnect()

 return db


def getConn():
 db = getDB()
 cursor : cursor_cext.CMySQLCursor = db.cursor()

 def close():
  db.commit()
  cursor.close()
 
 return db, cursor, close


class User:
 table_name = "users"

 def create_table():
  db = getDB()
  cursor = db.cursor()

  cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS users 
  (id INT AUTO_INCREMENT, 
  email VARCHAR(30) UNIQUE NOT NULL, 
  pass VARCHAR(60) NOT NULL, 
  username VARCHAR(30) UNIQUE NOT NULL, 
  PRIMARY KEY(id),
  profile_photo TEXT 
  );
  ''')

  db.commit()
  cursor.close()

 def addUser(email:str, password: str, username: str) -> int: 
  hashpwd = bcrypt.hashpw(password.encode('utf8'),  bcrypt.gensalt()).decode('utf8')
  
  db = getDB()
  cursor = db.cursor()
  res = cursor.execute(f'''INSERT INTO users(email, pass, username) VALUES(%(email)s, %(hashedPwd)s, %(username)s);''', {
   "email": email, 
   "hashedPwd": hashpwd,
   "username" : username
  })
  
  uid = cursor.lastrowid
  print(f"User added -> id : {uid} | email : {email}")
  
  db.commit()
  cursor.close()

  return uid

 def checkPassword(email: str, password: str):
  db = getDB()
  cursor = db.cursor()

  cursor.execute(f'''SELECT pass from users where email = %(email)s;''', {
   "email": email 
  })
  res = cursor.fetchall()
  
  if(len(res) == 0): raise Exception("User not found")

  hashedPwd: str = res[0][0]
  isPasswordCorrect = bcrypt.checkpw(password.encode('utf8'), hashedPwd.encode('utf8'))
  cursor.close()

  return isPasswordCorrect
 
 def getUID(email: str):
  cursor = getDB().cursor()

  cursor.execute(f'''SELECT id from users where email = %(email)s;''', {
   "email" : email
  })

  rows = cursor.fetchall()

  if(not len(rows)): raise Exception("User not found")

  uid = rows[0][0]
  cursor.close()

  return int(uid)

  
  

class Message: 
 table_name = "message"

 def create_table():
  db = getDB()
  cursor = db.cursor()
  
  cursor.execute('''CREATE TABLE IF NOT EXISTS message
  (id INT AUTO_INCREMENT, 
  data TEXT NOT NULL, 
  uid INT NOT NULL, 
  created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(id),
  FOREIGN KEY(uid) REFERENCES users(id))''')
  
  db.commit()
  cursor.close()

 def createMessage(data: str, uid: int):
  _, cursor, close = getConn()
  
  cursor.execute('''INSERT INTO message (data, uid) VALUES(%(data)s, %(uid)s)''', {
   "data" : data,
   "uid" : uid
  })
  mid = cursor.lastrowid
  print(f"Message Created | mid -> {mid} | uid -> {uid}")

  close()
  return mid



class ServerInfo: 
 table_name = "server_info"

 def create_table(): 
  _, cursor, close = getConn()

  cursor.execute('''
  CREATE TABLE IF NOT EXISTS server_info 
  (id INT AUTO_INCREMENT,
  name VARCHAR(30) NOT NULL UNIQUE,
  public_invite_code VARCHAR(8) NOT NULL UNIQUE,
  public_profile_photo TEXT,
  PRIMARY KEY(id)
  )
  ''')

  close()

 def createServer(name):
  _, cursor, close = getConn()
  
  cursor.execute('''INSERT INTO server_info (name,public_invite_code) 
  VALUES (%(serverName)s, %(publicInviteCode)s)''',{
    "serverName" : name, 
    "publicInviteCode" : utils.getRandomString(8)
  })

  sid = cursor.lastrowid
  print(f"Server Created | sid -> {sid} | name -> {name}")
  
  ServerTextChannel.createTextChannel("General", sid)

  close()
  return sid


class ServerMember:
 table_name = "server_member"

 def create_table():
  _, cursor, close = getConn()

  cursor.execute('''
  CREATE TABLE IF NOT EXISTS server_member
  (uid INT NOT NULL,
  sid INT NOT NULL,
  role ENUM('OWNER', 'ADMIN', 'MEMBER') DEFAULT 'MEMBER',
  FOREIGN KEY(uid) REFERENCES users(id),
  FOREIGN KEY(sid) REFERENCES server_info(id),
  PRIMARY KEY(uid, sid))
  ''')

  close()

 def addMember(uid: int, sid: int, role: int = "MEMBER"): 
  _, cursor, close = getConn()

  cursor.execute('''INSERT INTO server_member (uid, sid, role) VALUES (%(uid)s, %(sid)s, %(role)s)''',{
   "uid": uid,
   "sid": sid,
   "role" : role
  })

  print(f"Server Member added | sid ->{sid} | uid -> {uid}")

  close()



class ServerTextChannel:
 table_name = "sText_channel"
 
 def create_table():

  _, cursor, close = getConn()

  cursor.execute('''CREATE TABLE IF NOT EXISTS sText_channel
  (
   id INT AUTO_INCREMENT,
   name VARCHAR(60) NOT NULL,
   sid INT NOT NULL,
   FOREIGN KEY(sid) REFERENCES server_info(id),
   UNIQUE(name, sid),
   PRIMARY KEY(id) 
  )''')

  close()

 def createTextChannel(name: str, sid: int): 
  _, cursor, close = getConn()
  
  cursor.execute('''INSERT INTO sText_channel
  (name, sid)
  VALUES (%(channelName)s, %(sid)s)
  ''',
  {
   "channelName": name, 
   "sid": sid
  })

  tcid = cursor.lastrowid

  print(f"Server Text Channel Created | tcid -> {tcid} | sid -> {sid}")

  close()


class PersonalMessage: 
 table_name = "personal_message"

 def create_table():
  _, cursor, close = getConn()

  cursor.execute('''CREATE table IF NOT EXISTS personal_message
  (to_uid INT NOT NULL,
  from_uid INT NOT NULL,
  mid INT NOT NULL,
  FOREIGN KEY(to_uid) REFERENCES users(id),
  FOREIGN KEY(from_uid) REFERENCES users(id),
  FOREIGN KEY(mid) REFERENCES message(id))
  ''')

  close()


 def sendDM(senderUID: int, receiverUID: int, mid: int):
  _, cursor, close = getConn()
  
  cursor.execute('''INSERT INTO personal_message 
  (to_uid, from_uid, mid)
  VALUES (%(receiver)s, %(sender)s, %(messageID)s)''',{
   "receiver": senderUID,
   "sender": receiverUID, 
   "messageID" : mid
  })

  print(f"Personal Message sent | sender_uid -> {senderUID} | receiver_uid -> {receiverUID}")

  close()