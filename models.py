from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from datetime import datetime


db = SQLAlchemy()


class Messages(db.Model):
    id = sa.Column("id", sa.Integer, sa.Identity(start=1), primary_key=True, index=True)
    user = sa.Column("user", sa.String(256), index=True)
    message = sa.Column("message", sa.String(1024))
    timestamp = sa.Column("timestamp", sa.DateTime)

    def __init__(self, user, message="", timestamp=datetime.utcnow(), **kwargs):
        super().__init__(self, **kwargs)
        self.user = user
        self.message = message
        self.timestamp = timestamp


class User(db.Model):
    id = sa.Column("id", sa.Integer, sa.Identity(), primary_key=True, index=True)
    name = sa.Column("name", sa.String(256))
    reg_time = sa.Column("regtime", sa.DateTime)
    last_activity = sa.Column("last_activity", sa.DateTime)
