


INCLUDE_PATH = "/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/Server"



import sys
# Proper Imports
sys.path.insert(0, INCLUDE_PATH)

import os
from UDPServer import UDPServer
from CamHandler import CamHandler
from privates import *
from WebInterface.utils import *
from Server.dbmanagement import *
import json
import time
from threading import *
from socket import *






def createServer():
        s = Server()
        return s

class Server:
    def __init__(self):
        self.camHandler = CamHandler()
        self.udpServer = UDPServer()

    def reload(self):
        self.camHandler = CamHandler()
        self.udpServer = UDPServer()


    def run_passiv(self):
       self.udpServer.passivMode() 

    def database_config(self):
        databaseConfigLoop()

    def listen_to(self):
        self.udpServer.handleData()

    def handleCam(self):
        self.camHandler.chooseCam()

    def mainloop(self):
        while 1:
            try :
                op = finput("Was möchtest du tun?")
                if op == "q" or op == "quit" :
                    exit(0)
                if op == "passiv" or op == "p":
                    self.run_passiv()
                if op == "cam" or op == "c":
                   self.handleCam()
                if op == "reload" or op == "r":
                    self.reload()
                if op == "listen" or op == "l":
                    self.listen_to()
                if op == "database" or op == "d":
                    self.database_config()
            except KeyboardInterrupt:
                print("\nAbbruch!")
                exit(1)