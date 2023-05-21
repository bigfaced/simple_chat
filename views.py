from flask import render_template, session, request
from models import db, Messages, Users


# @app.route("/")
def index():
    if session.get("name"):
        template = "index.jinja2"
    else:
        template = "login.jinja2"
    return render_template(template)


