#! /opt/homebrew/bin/python3

from flask import Flask, render_template, url_for
import json
import os


PATH = "/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/JsonData/currentDict.json"



currentDict = {}

def loadCurrentDict():
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



app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    loadCurrentDict()
    s, t, v, l = splitSensorData(currentDict)
    return render_template("index.html",sensors=s,types=t,values=v,l=l)
    

if __name__ == "__main__":
    app.run(debug=True)
