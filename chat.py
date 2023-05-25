from flask import Flask, g
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
app.config["SQLALCHEMY_ECHO"] = False
#app.config["SESSION_COOKIE_SAMESITE"] = "None"
#app.config["SESSION_COOKIE_SECURE"] = "True"

with app.app_context():
    db.init_app(app)
    db.create_all()

app.add_url_rule("/", view_func=views.index)
app.add_url_rule("/api/<cmd>", view_func=controls.api)
app.add_url_rule("/api/login", view_func=controls.login, methods=["POST"])
app.add_url_rule("/api/logout", view_func=controls.logout, methods=["GET", "POST"])
app.add_url_rule("/api/keepalive", view_func=controls.keepalive, 
                 methods=["GET", "POST"])
app.add_url_rule("/api/list_users", view_func=controls.list_users, methods=["GET", "POST"])


@app.before_request
def before_req():
    print("----------------- request started ---------------------")
    db.session.begin()  # The whole request runs in a single DB transaction
    controls.do_refresh()


@app.teardown_request
def after_req(exc):
    print(datetime.now(), "DEBUG: ", "teardown request", repr(exc))
    if g.get("ROLLBACK"):
        print(datetime.now(), "DEBUG: ", "Transaction rolled back")
        db.session.rollback()
    else:
        print(datetime.now(), "DEBUG ", "comitted")
        db.session.commit()
    print("------------------- request ended -------------------------")


if __name__ == "__main__":
    app.run(debug=True)