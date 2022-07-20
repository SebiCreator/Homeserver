from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
#from .models import SensorData
from . import db
import json
import os
from .utils import *



PATH = "/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/JsonData/currentDict.json"

views = Blueprint('views',__name__)

@views.route("/")
def root():
    if current_user.is_authenticated:
        return redirect(url_for("views.dashboard"))
    else:
        return redirect(url_for("auth.login"))


@views.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
    currentDict = loadJSONDict(PATH)
    s, t, v, l = splitSensorData(currentDict)
    return render_template("index.html",sensors=s,types=t,values=v,l=l)


@views.route("/project",methods=['POST','GET'])
def project():
    return "<h1>In Work..</h1>"

@views.route("/search",methods=['POST','GET'])
def search():
    data = request.form['searchinput']
    return "<h1> %s You want to search lol</h1>"  % data





