from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.get(id)


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    value = db.Column(db.Text())

    def __repr__(self):
        return self.value


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class GlobalQueue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, index=True)
    TotalMessagesInbound = db.Column(db.Integer)
    TotalMessagesOutbound = db.Column(db.Integer)
    MeanTimeInQueueInbound = db.Column(db.Integer)
    MeanTimeInQueueOutbound = db.Column(db.Integer)
    LongestTimeInInbound = db.Column(db.Integer)
    LongestTimeInOutbound = db.Column(db.Integer)


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domainname = db.Column(db.Text, index=True, unique=True)
    stats = db.relationship("DomainQueue")

    def __repr__(self):
        return self.domainname


class DomainQueue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.Integer, db.ForeignKey('domain.id'))
    datetime = db.Column(db.DateTime, index=True)
    ReceiveQueueCountInbound = db.Column(db.Integer)
    ReceiveQueueCountOutbound = db.Column(db.Integer)
    DeliveryQueueCountInbound = db.Column(db.Integer)
    DeliveryQueueCountOutbound = db.Column(db.Integer)
    LongestTimeInReceiveQueueInbound = db.Column(db.Integer)
    LongestTimeInReceiveQueueOutbound = db.Column(db.Integer)
    LongestTimeInDeliveryQueueInbound = db.Column(db.Integer)
    LongestTimeInDeliveryQueueOutbound = db.Column(db.Integer)
    MeanTimeInReceiveQueueInbound = db.Column(db.Integer)
    MeanTimeInReceiveQueueOutbound = db.Column(db.Integer)
    MeanTimeInDeliveryQueueInbound = db.Column(db.Integer)
    MeanTimeInDeliveryQueueOutbound = db.Column(db.Integer)
