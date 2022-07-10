#! /opt/homebrew/bin/python3 


INCLUDE_PATH = "/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/Server"



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
import sys

sys.path.insert(0,INCLUDE_PATH)



from privates import *
from CamHandler import CamHandler
from UDPServer import UDPServer



################## SETUP ##############################


camHandler = CamHandler()
udpServer = UDPServer()


#################### MAIN LOOP #########################



def mainloop():
    while 1:
        try:
            op = input("\n++++++++++++++++++++++\nWas möchtest du tun?\n>>\t")
            if op == "udp":
                udpServer.serve()
            if op == "passiv":
                udpServer.passivMode()
            if op == "udpconfig":
                udpServer.config()
            if op == "cam":
                camHanlder.chooseCam()
            if op == "listen":
                udpServer.handleData()
            else:
                print("Keine option mit der Bezeichung %s" % op)
        except EOFError:
            continue
        except KeyboardInterrupt:
            print("\nAbbruch..")
            exit(1)


################## ARGV PARSING ##############
    
if len(sys.argv) == 2:
    op = sys.argv[1]
    if op == "normal" or op == "" or op == None:
        mainloop()
    elif op == "passiv":
        udpServer.passivMode()
    elif op == "cam":
        camHandler.chooseCam()
    else:
        print("no such option!")
        exit(1)
else:
    mainloop()

