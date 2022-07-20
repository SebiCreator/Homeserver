from sqlalchemy import ForeignKey
from . import db
from flask_login import UserMixin

class Id_Generator():
    def __init__(self):
        self.num = 0

    def get(self):
        old = self.num
        self.num += 1
        return old

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Room(db.Model):
    name = db.Column(db.String(50), primary_key=True)


class Device(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    room = db.Column(db.String(50), db.ForeignKey("room.name"))


class Unit(db.Model):
    name = db.Column(db.String(30),primary_key=True)


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(50))
    device = db.Column(db.String(50), db.ForeignKey("device.name"))
    unit = db.Column(db.String(30), db.ForeignKey("unit.name"))


class Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.Integer, db.ForeignKey("sensor.id"))
    date = db.Column(db.String(20))
    value = db.Column(db.Float)
