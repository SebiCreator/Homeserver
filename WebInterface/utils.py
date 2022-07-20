import json
from venv import create
from . import create_app, db
from .DBModels import *
from datetime import datetime

# Lädt JSON-File und gibt es als Dict aus
def loadJSONDict(path):
     with open(path) as file:
         return json.load(file)

         
         
# Konvertiert einzelnes Sensor Dict in einzele Variablen
# s = Device Name
# t = Sensor Typ
# v = Wert des Sensors
# l = Anzahl der Sensor Typen
def splitSensorData(d):
    k = list(d.keys())
    s = [e.split(":")[0] for e in k]
    t = [e.split(":")[1] for e in k]
    v = list(d.values())
    l = len(k)
    return s, t, v, l

    
    
def new_device():
    app = create_app()
    name = input("Name:\t>> ")
    room = input("Room:\t>> ")
    with app.app_context():
        d = Device(name=name,room=room)
        db.session.add(d)
        db.session.commit()
        print(d)
    
    
def new_unit():
    app = create_app()
    name = input("Name:\t>> ")
    with app.app_context():
        u = Unit()
        u.name = name
        db.session.add(u)
        db.session.commit()
        print(u)
    
def new_sensor():
   app = create_app()
   typ = input("Typ:\t>> ")
   device = input("Device:\t>> ")
   unit= input("Unit:\t>> ")
   with app.app_context():
        s = Sensor(typ,device,unit) 
        db.session.add(s)
        db.session.commit()
        print(s)

def new_room():
    app = create_app()
    name = input("Name:\t>> ")
    with app.app_context():
        r = Room()
        r.name = name
        db.session.add(r)
        db.session.commit()
        print(r)
        
def new_Measure(sensor,value):
    app = create_app()
    with app.app_context():
        date = str(datetime.now())
        m = Measure(sensor,date,value)
        db.session.add(m)
        db.session.commit()
        print(m)