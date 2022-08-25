# from dotenv import load_dotenv
# load_dotenv()


from flask import Flask
import sqlalchemy

app = Flask(__name__)

print(sqlalchemy.__version__)

@app.get('/')
def root():
    return sqlalchemy.__version__