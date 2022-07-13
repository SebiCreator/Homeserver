from flask import Blueprint, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
#from .models import SensorData
from . import db
import json
import os



PATH = "/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/JsonData/currentDict.json"

currentDict = {}




def loadCurrentValues():
     global currentDict
     with open(PATH) as file:
         currentDict = json.load(file)

def splitSensorData(d):
    k = list(d.keys())
    s = [e.split(":")[0] for e in k]
    t = [e.split(":")[1] for e in k]
    v = list(d.values())
    l = len(k)
    return s, t, v, l



views = Blueprint('views',__name__)




@views.route("/",methods=["GET","POST"])
def index():
    loadCurrentValues()
    s, t, v, l = splitSensorData(currentDict)
    return render_template("index.html",sensors=s,types=t,values=v,l=l)


@views.route("/project",methods=['POST','GET'])
def project():
    return "<h1>In Work..</h1>"

@views.route("/search",methods=['POST','GET'])
def search():
    data = request.form['searchinput']
    return "<h1> %s You want to search lol</h1>"  % data





