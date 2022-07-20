#! /opt/homebrew/bin/python3


import os
import sys
from UDPServer import UDPServer
from CamHandler import CamHandler
from privates import *
from WebInterface import create_app
from WebInterface.utils import *
import json
import time
from threading import *
from socket import *
INCLUDE_PATH = "/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/Server"


app = create_app()

# Proper Imports
sys.path.insert(0, INCLUDE_PATH)


camHandler = CamHandler()
udpServer = UDPServer()


def mainloop():
    while 1:
        try:
            op = input("\n++++++++++++++++++++++\nWas möchtest du tun?\n>>\t")
            if op == "udp":
                udpServer.serve()
            elif op == "passiv":
                udpServer.passivMode()
            elif op == "udpconfig":
                udpServer.config()
            elif op == "cam":
                camHanlder.chooseCam()
            elif op == "listen":
                udpServer.handleData()
            elif op == "add-room":
                new_room()
            elif op == "add-unit":
                new_unit()
            elif op == "add-device":
                new_device()
            elif op == "add-sensor":
                new_sensor()
            else:
                print("Keine option mit der Bezeichung %s" % op)
        except EOFError:
            continue
        except KeyboardInterrupt:
            print("\nAbbruch..")
            exit(1)


if len(sys.argv) == 2:
    op = sys.argv[1]
    if op == "normal" or op == "" or op == None:
        mainloop()
    elif op == "passiv":
        udpServer.passivMode()
    elif op == "cam":
        camHandler.chooseCam()
    elif op == "listen":
        udpServer.handleData()
    else:
        print("no such option!")
        exit(1)
else:
    mainloop()
