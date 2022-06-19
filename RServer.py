#! /opt/homebrew/bin/python3 



from socket import *
from threading import *
import time
import json


############ STATIC SETTINGS ################


IP = "192.168.0.209"
PORT = 5000
BUFFERSIZE = 1024
TIMEOUT = 10

cDict = {}

############## HELPER FUNCTIONS ##############

def save():
    with open('cDict.json','w') as outfile:
        json.dump(cDict,outfile)

def load():
    with open('cDict.json') as file:
        global cDict
        cDict = json.load(file)


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
            print("-------")
            print(f"Message: {message}");
            if trans == None:
                print(f"IP: {addr[0]}, Port: {addr[1]}")
            else:
                print(f"Name: {trans}")
    except KeyboardInterrupt:
        print()
        return



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



################## SETUP ##############################


load()
s = socket(AF_INET, SOCK_DGRAM) 
s.bind((IP,PORT))
s.settimeout(TIMEOUT)
print(f"Server is listening on {IP}: {str(PORT)}..")
print(f"timeout={TIMEOUT}")


#################### MAIN LOOP #########################

while 1:
    try:
        op = input("##########\nWas möchtest du tun?\n>>\t")

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
        else:
            print(f"Keine option mit der Bezeichung {op}")
            print("Bitte nochmal probieren oder mit q beenden\n")
    except EOFError:
        continue
    except KeyboardInterrupt:
        print("\nAbbruch..")
        exit(1)

    



