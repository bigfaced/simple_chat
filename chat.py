from flask import Flask
from dotenv import load_dotenv
import os
from models import db
import views
import controls
from datetime import datetime


app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_ECHO"] = True
#app.config["SESSION_COOKIE_SAMESITE"] = "None"
#app.config["SESSION_COOKIE_SECURE"] = "True"
with app.app_context():
    db.init_app(app)
    db.create_all()

app.add_url_rule("/", view_func=views.index)
app.add_url_rule("/api/<cmd>", view_func=controls.api)
app.add_url_rule("/api/login", view_func=controls.login, methods=["POST"])
app.add_url_rule("/api/logout", view_func=controls.logout, methods=["GET", "POST"])


@app.before_request
def before_req():
    controls.do_refresh()


if __name__ == "__main__":
    app.run(debug=True)