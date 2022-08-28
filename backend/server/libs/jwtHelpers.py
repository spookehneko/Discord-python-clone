import jwt
import os

JWT_ALGORITHM = 'HS256'

def sign(data: dict) -> str:
 return jwt.encode(payload=data, key=os.environ['JWT_SECRET'],algorithm=JWT_ALGORITHM)


def verify(encoded: dict) -> str | bool: 
 try:
  return jwt.decode(encoded, key=os.environ['JWT_SECRET'], algorithms=JWT_ALGORITHM)
 except jwt.exceptions.InvalidSignatureError as e: return False

 