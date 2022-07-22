import json
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







