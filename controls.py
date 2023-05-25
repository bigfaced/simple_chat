from flask import session, request, redirect, url_for, abort, flash, g, jsonify
from models import db, Messages, Users
from datetime import datetime
from inspect import stack


MAX_NAME_SIZE = 12
DEBUG = True


def xprint(l, f, m):
    print(datetime.now(), l, f, m)


def dprint(m):
    xprint("DEBUG", stack()[1].function, m)


def eprint(m):
    if DEBUG:
        xprint("ERROR", stack()[1].function, m)


def get_user_object(_name=None):
    dprint("started")
    if not _name:   # Disgusting, but setting default value for argument 
                    # _name causes exception "Working outside of request context"!
        name = session.get("name")
    else:
        name = _name
    if not name:
        return None
    try:
        u = db.session.execute(db.select(Users).filter_by(name=name)).scalar_one_or_none()
        dprint(f"user object:{u}")
    except Exception as _exc:
        g.ROLLBACK = True
        abort(500, "Exception in get_user_object")
    return u


def is_logged_in():
    dprint("started")
    name = session.get("name")
    if not name:
        return False
    user = get_user_object()
    if not user:
        return False
    return True


def is_authorized(*args, **kwargs):
    dprint("started")
    # reserved for later development
    return True


def check_name(_name:str):
    dprint("started")
    if len(_name) > MAX_NAME_SIZE or len(_name)<1:
        flash("A név mérete nem megfelelő!")
        return False
    user = get_user_object(_name)
    if user:
        flash("Valaki már használja ezt a nevet!")
        return False
    return True



def do_login():
    dprint("started")
    if is_logged_in():
        abort(403)
    name = request.form.get("name")
    try:
        if check_name(name):
            user = Users()
            user.name = name
            user.reg_time = user.last_activity = datetime.utcnow()
            db.session.add(user)
            session["name"] = name
        else:
            flash("Hibás vagy még aktív nevet adtál meg!", "error")
    except Exception as _exc:
        g.ROLLBACK = True
        abort(500, "Exception in login")
    return


def do_logout():
    dprint("started")
    if not is_logged_in():
        abort(403)
    try:
        name = session.pop("name")
        user = get_user_object(name)
        db.session.delete(user)
    except Exception as _exc:
        g.ROLLBACK = True
        abort(500, "Exception in logout")
    return


def do_refresh():
    dprint("started")
    dprint(f"request: {request.url_rule}")
    if is_logged_in():
        user:Users = get_user_object()
        retval = False
        try:
            user.last_activity = datetime.utcnow()
            # commit @ teardown_request!
            retval = True
        except Exception as _exc:
            g.ROLLBACK = True
            abort(500, "Exception in do_refresh")
    return


def get_active_users(json=False):
    select_statement = db.select(Users)
    user_list = db.session.execute(
        select_statement.order_by(Users.last_activity)
    ).scalars()
    if json:
        return jsonify([
            {'id':i.id, 'name': i.name, 'reg_time': i.reg_time,
             'last_activity': i.last_activity} for i in user_list
        ])
    return user_list


# @app.route("/api/<cmd>", methods=["POST"])
def api(cmd):
    return redirect(url_for("index"))


# @app.route("/app/login", methods=["POST"])
def login():
    dprint("started")
    do_login()
    return redirect(url_for("index"))


# @app.route("/api/logout", methods=["GET", "POST"])
def logout():
    dprint("started")
    do_logout()
    return redirect(url_for("index"))


def keepalive():
    dprint("started")
    if not is_logged_in():
        g.ROLLBACK = True
        abort(403)
    # Simply do nothing. Every requests run do_refresh() which updates
    # the user's last_activity field.
    #user = get_user_object()
    return jsonify({"Status":"OK"})


def list_users():
    if is_logged_in() and is_authorized() or True:
        active_users = get_active_users(json=True)
    else:
        g.ROLLBACK=True
        abort(403)
    return active_users