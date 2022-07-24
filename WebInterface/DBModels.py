from sqlalchemy import ForeignKey
from flask_login import UserMixin
from . import db


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

    def __repr__(self):
        d = {"id": self.id,
             "email": self.email,
             "password": self.password,
             "first_name": self.first_name}
        return ("[USER]\t" + str(d))


class Room(db.Model):
    name = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        return ("[ROOM]\t" +
                str({"name": self.name}))


class Device(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    room = db.Column(db.String(50), db.ForeignKey("room.name"))
    ip = db.Column(db.String(20))
    port = db.Column(db.String(10))

    def __repr__(self):
        return ("[DEVICE]\t" +
                str({"name": self.name, "room": self.room,
                     "ip": self.ip, "port": self.port}))


class Unit(db.Model):
    name = db.Column(db.String(30), primary_key=True)

    def __repr__(self):
        return ("[UNIT]\t" +
                str({"name": self.name}))


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(50))
    device = db.Column(db.String(50), db.ForeignKey("device.name"))
    unit = db.Column(db.String(30), db.ForeignKey("unit.name"))

    def __repr__(self):
        d = {"id": self.id, "typ": self.typ, "device": self.device,
             "unit": self.unit}
        return ("[SENSOR]\t" +
                str(d))


class Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.Integer, db.ForeignKey("sensor.id"))
    date = db.Column(db.String(40))
    value = db.Column(db.Float)

    def __repr__(self):
        d = {"id":self.id,"sensor":self.sensor,"date":self.date,
             "value": self.value}

        return ("[MEASURE]\t" + 
                str(d))
