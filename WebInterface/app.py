#! /opt/homebrew/bin/python3

from flask import Flask, render_template, url_for
import json


currentDict = {}

with open("../JsonData/currentDict.json") as file:
    currentDict = json.load(file)

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    k = list(currentDict.keys())
    s = [e.split(":")[0] for e in k]
    t = [e.split(":")[1] for e in k]
    v = list(currentDict.values())
    return render_template("index.html",sensors=s,types=t,values=v,l=len(k))
    

if __name__ == "__main__":
    app.run(debug=True)
