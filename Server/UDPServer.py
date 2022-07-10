import json
import os
import sys
import time


from socket import *
from privates import *

BUFFERSIZE = 1024
TIMEOUT = 10

def disablePrint():
     sys.stdout = open(os.devnull,'w')
def enablePrint():
     sys.stdout = sys.__stdout__


class UDPServer:

    def conig(self):
        pass

    def loadSensors(self):
        with open(DICT_PATH + "sensors.json") as file:
            self.sensors = json.load(file)

    def loadcurrentValues(self):
        with open(DICT_PATH + "currentDict.json") as file:
            self.current = json.load(file)

    def saveSensors(self):
        with open(DICT_PATH + "sensors.json", "w") as outfile:
            json.dump(self.sensors, outfile)

    def savecurrentValues(self):
        with open(DICT_PATH + "currentDict.json", "w") as outfile:
            json.dump(self.current, outfile)

    def __init__(self):
        self.loadSensors()
        self.loadcurrentValues()
        self.socket = socket(AF_INET, SOCK_DGRAM)
        try:
            self.socket.bind((IP, PORT))
            print("[SUCESSFULLY CONNECTED] IP=%s, PORT=%s" % (IP , PORT))
        except OSError as e:
            print(e)
        self.socket.settimeout(TIMEOUT)

    def inDict(self, addr):
        ip = addr[0]
        port = addr[1]
        for key in self.sensors:
            if ip == key:
                if self.sensors[key][0] == port:
                    return self.sensors[key][1]
        return None

    def extractMessage(self, trans, msg):
        s = msg.split(",")
        n = len(s)
        pairs = []
        for i in range(n):
            pairs.append(s[i].split("="))

        for e in pairs:
            name = e[0]
            num = float(e[1])
            self.current[f"{trans}:{name}"] = num
            self.savecurrentValues()

        #temp=32.40,hum=99.90

    def handleData(self):
        try:
            while 1:
                try:
                    bytePair = self.socket.recvfrom(BUFFERSIZE)
                except timeout:
                    return
                message = bytePair[0].decode()
                addr = bytePair[1]
                trans = self.inDict(addr)
                self.extractMessage(trans, message)
                print("----------")
                if trans == None:
                    print(
                        f"Message: {message} von IP=({addr[0]}) & Port=({addr[1]}"
                    )
                else:
                    print(f"Message: {message} von {trans}")
        except KeyboardInterrupt:
            print()
            return

    def handleTimeoutChange(self):
        try:
            t = int(input("Wie lange soll der Timeout gehen?\n>>\t"))
            TIMEOUT = t
            self.socket.settimeout(t)
            print("timeout=" + str(TIMEOUT))
        except KeyboardInterrupt:
            return

    def handleSend(self):
        try:
            ip = input("Bitte gib die Target-IP an\n>>\t")
            port = int(input("Bitte gib den Target-Port an\n>>\t"))
            msg = input("Bitte gib die Nachricht an\n>>\t").encode()
            self.socket.sendto(msg, (ip, port))
            print("Nachricht erfolgreich gesendet")
        except KeyboardInterrupt:
            return

    def handleNewEntry(self):
        try:
            addr = input("Bitte gib IP und Port an (space als seperator)\n>>\t"
                         ).split(" ")
            name = input("Bitte gib den zugehörigen Namen an\n>>\t")
            if len(addr) != 2:
                print("Zu viele Argumente..")
            ip = addr[0]
            port = int(addr[1])
            self.sensors[ip] = (port, name)
            self.saveSensors()
        except KeyboardInterrupt:
            return

    def passivMode(self):
        c = 0
        try:
            print("Passiv Mode -stdout is inactive")
            disablePrint()
            while 1:
                c += 1
                self.handleData()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        enablePrint()
        print("End of passiv mode..")
