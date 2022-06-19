#! /opt/homebrew/bin/python3 



from socket import *
from threading import *
import time
import json
import cv2 as cv
import sys, os
import time


############ STATIC SETTINGS ################


IP = "192.168.0.209"
PORT = 5000
BUFFERSIZE = 1024
TIMEOUT = 10

DICT_PATH = "/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/"

cDict = {}
currentDict= {}

############## HELPER FUNCTIONS ##############

def disablePrint():
    sys.stdout = open(os.devnull,'w')
def enablePrint():
    sys.stdout = sys.__stdout__

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
    print("quit or q\t\tfor quitting clear with the server")
    print("timeout or t\t\t changes timeout value")
    print("passiv\t\t runs silent in background for updating")
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

############## MAIN FUNCTIONS ###################

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
        t = int(input("Wie lange soll der Timeout gehen?\n>>\t"))
        TIMEOUT = t
        s.settimeout(t)
        print("timeout=" + str(TIMEOUT))




def handleSend():
        ip = input("Bitte gib die Target-IP an\n>>\t")
        port = int(input("Bitte gib den Target-Port an\n>>\t"))
        msg = input("Bitte gib die Nachricht an\n>>\t").encode()
        s.sendto(msg,(ip,port))
        print("Nachricht erfolgreich gesendet")



def handleNewEntry():
        addr = input("Bitte gib IP und Port an (space als seperator)\n>>\t").split(" ")
        name = input("Bitte gib den zugehörigen Namen an\n>>\t")
        if len(addr) != 2:
            print("Zu viele Argumente..")
        ip = addr[0]
        port = int(addr[1])
        cDict[ip] = (port,name)
        save()

def passiveMode():
    c = 0
    try:
        disablePrint()
        while 1:
            c += 1
            handleData()
            time.sleep(1)
    except KeyboardInterrupt:
        print("End of passiv mode..")
        enablePrint()
    enablePrint()




################## SETUP ##############################


loadCDict()
loadCurrentDict()
s = socket(AF_INET, SOCK_DGRAM) 
s.bind((IP,PORT))
s.settimeout(TIMEOUT)
print(f"Server is listening on {IP}: {str(PORT)}..")
print(f"timeout={TIMEOUT}")


#################### MAIN LOOP #########################

while 1:
    try:
        op = input("\n++++++++++++++++++++++\nWas möchtest du tun?\n>>\t")

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
        else:
            print(f"Keine option mit der Bezeichung {op}")
            help()
    except EOFError:
        continue
    except KeyboardInterrupt:
        print("\nAbbruch..")
        exit(1)

    


