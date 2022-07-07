#! /opt/homebrew/bin/python3 



from socket import *
from threading import *
import requests
import time
import json
import cv2 as cv
import sys, os
import time
import numpy as np
from io import BytesIO
from datetime import datetime
from privates import *




############ STATIC SETTINGS ################


BUFFERSIZE = 1024
TIMEOUT = 10

cDict = {}
currentDict= {}
camDict = {}

############## HELPER FUNCTIONS ##############

def disablePrint():
    sys.stdout = open(os.devnull,'w')
def enablePrint():
    sys.stdout = sys.__stdout__

def saveCamDict():
    with open(DICT_PATH + "camDict.json", "w") as outfile:
        global camDict
        json.dump(camDict,outfile)


def loadCamDict():
    with open(DICT_PATH + "camDict.json") as file:
        global camDict
        camDict = json.load(file) 

def saveCDict():
    with open(DICT_PATH + "cDict.json" ,'w') as outfile:
        global cDict
        json.dump(cDict,outfile)

def loadCDict():
    with open(DICT_PATH+"cDict.json") as file:
        global cDict
        cDict = json.load(file)

def saveCurrentDict():
    with open(DICT_PATH + "currentDict.json", "w") as outfile:
        global currentDict
        json.dump(currentDict,outfile)

def loadCurrentDict():
    with open(DICT_PATH + "currentDict.json") as file:
        global currentDict
        currentDict = json.load(file)
def help():
    print("listen or l\t\t listen for new UDP events")
    print("quit or q\t\t for quitting clear with the server")
    print("timeout or t\t\t changes timeout value")
    print("passiv\t\t\t runs silent in background for updating")
    print("send or s\t\t for sending an UDP text message")
    print("new or n\t\t for register a new connection")




def inDict(addr):
    ip = addr[0]
    port = addr[1]
    for key in cDict:
        if ip == key:
            if cDict[key][0] == port:
                return cDict[key][1]
    return None

def killOld():
    pid = os.getpid()
    res = str(os.system("ps aux | awk '/Server.py/{print $2}'"))
    for r in res.split("\n"):
        r = r.strip()
        if r == pid:
            continue
        os.kill(int(r),9)


############## MAIN FUNCTIONS ###################

def logData(intervall):
    c = 0
    try:
        while 1:
            try:
                bytePair = s.recvfrom(BUFFERSIZE)
            except timeout:
                return

            if not c % intervall == 0:
                continue
            message = bytePair[0].decode()
            c += 1
            ip = bytePair[1][0]
            port= bytePair[1][1]
            trans = inDict((ip,port))
            extractMessage(trans,message)
            print("----------")
            if trans == None:
                print(f"Message: {message} von ip={ip} & port={port}")
            else:
                print(f"Message: {message} von {trans}")
            print("Logging on")
            logMessage(trans,message)

    except KeyboardInterrupt:
        return
        

def handleData():
    try:
        while 1:
            try:
                bytePair = s.recvfrom(BUFFERSIZE)
            except timeout:
                return
            message = bytePair[0].decode()
            addr = bytePair[1]
            trans = inDict(addr)
            extractMessage(trans,message)
            print("----------")
            if trans == None:
                print(f"Message: {message} von IP=({addr[0]}) & Port=({addr[1]}")
            else:
                print(f"Message: {message} von {trans}")
    except KeyboardInterrupt:
        print()
        return

def logMessage(trans,msg):
    logDict = {}
    if trans == None:
        print("Username is None")
        return
    path = DICT_PATH + trans + ".json"

    try:
        with open(path,'w') as file:
            logDict = json.load(file)
    except UnsupportedOperation:
        print("ups")
        pass

    now = datetime.now()
    timestamp = now.strftime("%m/%d/%y %H:%M:%S")
    print(timestamp)
    s = msg.split(",")
    n = len(s)
    for i in range(n):
        pairs.append(s[i].split("="))

    for e in pairs:
        name = e[0]
        num = float(e[1])
        logDict[timestamp] = msg

    with open(path,'w') as outfile:
        json.dump(logDict,outfile)

    


def extractMessage(trans,msg):
    s = msg.split(",")
    n = len(s)
    pairs = []
    for i in range(n):
        pairs.append(s[i].split("="))

    for e in pairs:
        name = e[0]
        num = float(e[1])
        currentDict[f"{trans}:{name}"] = num
    saveCurrentDict()

    #temp=32.40,hum=99.90



def handleTimeoutChange():
    try:
        t = int(input("Wie lange soll der Timeout gehen?\n>>\t"))
        TIMEOUT = t
        s.settimeout(t)
        print("timeout=" + str(TIMEOUT))
    except KeyboardInterrupt:
        return




def handleSend():
    try:
        ip = input("Bitte gib die Target-IP an\n>>\t")
        port = int(input("Bitte gib den Target-Port an\n>>\t"))
        msg = input("Bitte gib die Nachricht an\n>>\t").encode()
        s.sendto(msg,(ip,port))
        print("Nachricht erfolgreich gesendet")
    except KeyboardInterrupt:
        return



def handleNewEntry():
    try:
        addr = input("Bitte gib IP und Port an (space als seperator)\n>>\t").split(" ")
        name = input("Bitte gib den zugehörigen Namen an\n>>\t")
        if len(addr) != 2:
            print("Zu viele Argumente..")
        ip = addr[0]
        port = int(addr[1])
        cDict[ip] = (port,name)
        save()
    except KeyboardInterrupt:
        return

def passiveMode():
    c = 0
    try:
        print("Passiv Mode -stdout is inactive")
        disablePrint()
        while 1:
            c += 1
            handleData()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    enablePrint()
    print("End of passiv mode..")

def backgroundMode():
    os.system('./Server.py &')
    print("server runs in background")
    print("if you want to kill please check the pid")


def showCam(name,url):
    res = requests.get(url,stream=True)

    print(name + " starts streaming")
    for chunk in res.iter_content(chunk_size=120000):
        if len(chunk) > 100:
            try:
                img_data = BytesIO(chunk)
                img = cv.imdecode(np.frombuffer(img_data.read(),np.uint8),1)
                gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
                cv.imshow(name,img)
            except Exception as e:
                print(str(e))
                continue
        if cv.waitKey(1) == ord("q"):
            cv.destroyAllWindows()
            print(name + " stops streaming")
            break

def chooseCam():
    print(camDict)
    opt = input("choose cam with name or type new for new cam\n>>\t")
    if opt == "new":
        n = input('Cam Name?\n>>\t')
        u = input("Url?^n>>\t")
        camDict[n] = u
        saveCamDict()
        return
    url = camDict[opt] 
    if url == None:
        print("keine cam mit der bezeichnung {opt} gefunden")
    showCam(opt,url)
    
    






################## SETUP ##############################


s = socket(AF_INET, SOCK_DGRAM) 
def setup():
    global s
    loadCDict()
    loadCurrentDict()
    loadCamDict()
    try:
        s.bind((IP,PORT))
    except OSError as e:
        print(e)
        print((IP,PORT))
        exit(1)
    s.settimeout(TIMEOUT)
    print(f"Server is listening on {IP}: {str(PORT)}..")
    print(f"timeout={TIMEOUT}")


#################### MAIN LOOP #########################

def mainloop():
    while 1:
        try:
            op = input("\n++++++++++++++++++++++\nWas möchtest du tun?\n>>\t")
            saveCamDict()
            if op == "listen" or op == "l":
                handleData()
            elif op == "quit" or op == "q":
                exit(0)
            elif op == "timeout" or op == "t":
                handleTimeoutChange()
            elif op == "send" or op == "s":
                handleSend()
            elif op == "new" or op == "n":
                handleNewEntry()
            elif op == "passiv":
                passiveMode()
            elif op == "help" or op == "h":
                help()
            elif op == "background":
                backgroundMode()
            elif op == "cams":
                chooseCam()
            elif op == "logging":
                logData(1)

            else:
                print(f"Keine option mit der Bezeichung {op}")
                help()
        except EOFError:
            continue
        except KeyboardInterrupt:
            print("\nAbbruch..")
            exit(1)


################## STARTSECTION ##############
    
if len(sys.argv) == 2:
    op = sys.argv[1]
    if op == "normal" or op == "" or op == None:
        setup()
        mainloop()
    elif op == "passiv":
        setup()
        passiveMode()
    elif op == "killold":
        killOld()
        print("old proc killed")
    elif op == "cams":
        setup()
        chooseCam()
    elif op == "listen":
        setup()
        setup()
        handleData()
    else:
        print("no such option!")
        exit(1)
else:
    setup()
    mainloop()

