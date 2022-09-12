import secrets
import string

def getRandomString(N: int) -> str: 
 res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(N))
 return res