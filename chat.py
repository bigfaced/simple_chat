from flask import Flask
from dotenv import load_dotenv
import os
from models import db


app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
with app.app_context():
    db.init_app(app)
    db.create_all()
    

