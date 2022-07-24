import json
import os
import sys
import time
from Server.utils import printError, printSucess
from .utils import *
from socket import *

append_parent_dir()

from privates import *


BUFFERSIZE = 1024
TIMEOUT = 10


class UDPServer:

    def __init__(self):
        self.sensors = loadJson(SENSOR_DICT_PATH)
        self.current = loadJson(CURRENT_DICT_PATH)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        try:
            self.socket.bind((IP, PORT))
            print("[SUCESSFULLY CONNECTED] IP=%s, PORT=%s" % (IP, PORT))
        except OSError as e:
            print(e)
        self.socket.settimeout(TIMEOUT)

    # Checkt ob ob Adresse bekannt ist oder nicht
    # Returnt Übersetzung oder None falls nicht vorhanden
    def inDict(self, addr):
        ip, port = addr
        for key in self.sensors:
            if ip == key and self.sensors[key][0] == port:
                return self.sensors[key][1]
        return None

    # Extrahiert Paket von Sensor printet und speichert es
    def extractMessage(self, translation, msg):
        if translation == None:
            translation = "Unknown Device"
        out = {}
        s = msg.split(",")
        n = len(s)
        pairs = []
        for i in range(n):
            pairs.append(s[i].split("="))

        for e in pairs:
            name = e[0]
            if e[1] in ["nan", None, "None", "Nan", "NULL", "null"]:
                printError("BAD_DATA", "Device: %s Sensor: %s" %
                           (translation, name))
                continue
            num = float(e[1])
            self.current[f"{translation}:{name}"] = num
            out[f"{translation}:{name}"] = num
            saveJson(CURRENT_DICT_PATH,self.current)

        return out

    # Wartet auf UDP Datenpakete
    def handleData(self):
        try:
            while 1:
                try:
                    bytePair = self.socket.recvfrom(BUFFERSIZE)
                except timeout:
                    return

                message = bytePair[0].decode()
                addr = bytePair[1]
                translation = self.inDict(addr)
                out = self.extractMessage(translation, message)
                printSucess("NEW_PACKET", str(out)) if out != {} else ""
        except KeyboardInterrupt:
            print()
            return

    # Ändert den Timeout Wert
    def handleTimeoutChange(self):
        try:
            t = int(input("Wie lange soll der Timeout gehen?\n>>\t"))
            TIMEOUT = t
            self.socket.settimeout(t)
            print("timeout=" + str(TIMEOUT))
        except KeyboardInterrupt:
            return

    # Sendet UDP Paket (args über input)
    def handleSend(self):
        try:
            ip = input("Bitte gib die Target-IP an\n>>\t")
            port = int(input("Bitte gib den Target-Port an\n>>\t"))
            msg = input("Bitte gib die Nachricht an\n>>\t").encode()
            self.socket.sendto(msg, (ip, port))
            print("Nachricht erfolgreich gesendet")
        except KeyboardInterrupt:
            return

    # Speichert neues Device mit Namen (args über input)
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
            saveJson(SENSOR_DICT_PATH,self.sensors)
        except KeyboardInterrupt:
            return

    # verarbeitet UDP Pakete im Hintergrund

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
