import json
import os
from datetime import datetime
import sys



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



def append_parent_dir():
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)




