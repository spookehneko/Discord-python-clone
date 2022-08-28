from asyncio import create_task
import os
from flask import current_app as app
from mysql import connector
import bcrypt


global db

def init():
 global db

 db = connector.connect(
  host=os.environ["DB_HOST"],
  user=os.environ["DB_USER"],
  password=os.environ["DB_PASSWORD"],
  port=os.environ["DB_PORT"],
  database=os.environ["DB_NAME"]
 )

 User.create_table()
 print("Connected to Database!")

def getDB() -> connector.CMySQLConnection:
 global db
 return db

class User:
 table_name = "users"

 def __init__(self) -> None:
  self.create_table()

 def create_table():
  cursor = getDB().cursor()

  cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT, email VARCHAR(30) UNIQUE NOT NULL, pass VARCHAR(60) NOT NULL, PRIMARY KEY(id));
  ''')

 def addUser(email:str, password: str) -> int: 
  hashpwd = bcrypt.hashpw(password.encode('utf8'),  bcrypt.gensalt()).decode('utf8')
  
  db = getDB()
  cursor = db.cursor()
  res = cursor.execute(f'''INSERT INTO users(email, pass) VALUES(%(email)s, %(hashedPwd)s);''', {
   "email": email, 
   "hashedPwd": hashpwd
  })
  
  uid = cursor.lastrowid
  print(f"User added -> id : {type(uid)} | email : {email}")
  
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

  
  

