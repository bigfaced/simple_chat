from flask import session, request, redirect, url_for, abort, flash
from models import db, Messages, Users
from datetime import datetime
from time import sleep


MAX_NAME_SIZE = 12


def is_logged_in():
    '''
    Don't call it from inside an SQL transaction!
    '''
    name = session.get("name")
    if not name:
        return False
    print(datetime.now(), "DEBUG: check if user exists")
    db.session.begin()
    user = Users.query.filter_by(name=name).first()
    db.session.rollback()   # after a read only query commit is unnecessary
    if not user:
        return False
    return True


def is_authorized(*args, **kwargs):
    # reserved for later development
    return True


def check_name(_name:str):
    '''
    Don't call it from inside an SQL transaction!
    '''
    if len(_name) > MAX_NAME_SIZE or len(_name)<1:
        flash("A név mérete nem megfelelő!")
        return False
    db.session.begin()
    user = Users.query.filter_by(name=_name).first()
    db.session.rollback()
    if user:
        flash("Valaki már használja ezt a nevet!")
        return False
    return True


def do_login():
    if is_logged_in():
        abort(403)
    name = request.form.get("name")
    try:
        if check_name(name):
            db.session.begin()
            user = Users()
            user.name = name
            user.reg_time = user.last_activity = datetime.utcnow()
            db.session.add(user)
            db.session.commit()
            session["name"] = name
        else:
            flash("Hibás vagy még aktív nevet adtál meg!", "error")
    except Exception as ex:
        print(datetime.now(), "do_login Exception:", repr(ex))
        db.session.rollback()
        abort(500, "Exception in login")
    return


def do_logout():
    if not is_logged_in():
        abort(403)
    try:
        db.session.begin()
        name = session.pop("name")
        user = Users.query.filter_by(name=name).first()
        db.session.delete(user)
        db.session.commit()
    except Exception as ex:
        print("do_logout Exception", repr(ex))
        db.session.rollback()
        abort(500, "Exception in logout")
    return


def do_refresh():
    print(datetime.now(), "Debug: ", "do_refresh started")
    name = session.get("name")
    retval = False
    if name:
        try:
            db.session.begin()
            user:Users = Users.query.filter_by(name=name).first()
            user.last_activity = datetime.utcnow()
            db.session.commit() # ????
            retval = True
        except Exception as ex:
            print(datetime.now(),"do_refresh exception", repr(ex))
            db.session.rollback()
    print(datetime.now(), "Debug: ","do_refresh finished")
    return None


# @app.route("/api/<cmd>", methods=["POST"])
def api(cmd):
    print("Debug api():", cmd)
    return redirect(url_for("index"))


# @app.route("/app/login", methods=["POST"])
def login():
    do_login()
    return redirect(url_for("index"))


# @app.route("/api/logout", methods=["POST"])
def logout():
    do_logout()
    return redirect(url_for("index"))