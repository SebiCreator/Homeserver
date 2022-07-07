#! /opt/homebrew/bin/python3

from flask import Flask, render_template, url_for
import json


currentDict = {}

with open("../JsonData/currentDict.json") as file:
    currentDict = json.load(file)

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    ids = list(currentDict.keys())
    values = list(currentDict.values())
    out = ""
    for i in range(len(values)):
        out += "<p>"
        out += str(ids[i]) + " : "
        out += str(values[i]) 
        out += "</p>"
        out += "\n<br>"
    return out
    
    

if __name__ == "__main__":
    app.run(debug=True)
