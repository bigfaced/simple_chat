from flask import render_template, session, request
from models import db, Messages, Users
from controls import is_logged_in, is_authorized
from datetime import datetime


# @app.route("/")
def index():
    print(datetime.now(), "DEBUG ", "index:",is_logged_in())
    if is_logged_in() and is_authorized():
        template = "index.jinja2"
    else:
        template = "login.jinja2"
    return render_template(template)


