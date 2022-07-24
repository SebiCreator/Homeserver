from .UDPServer import UDPServer
from .CamHandler import CamHandler
from WebInterface.utils import append_parent_dir
from .dbmanagement import *
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

    def options():
        print("q or quit -> quit programm")
        print("p or passiv -> run in passiv mode")
        print("c or cam -> choose cam")
        print("l or listen -> listen to packets")
        print("r or reload -> reload ALL connections")

    def mainloop(self):
        while 1:
            try :
                op = finput("\nWas möchtest du tun?")
                if op == "q" or op == "quit" :
                    exit(0)
                elif op == "passiv" or op == "p":
                    self.run_passiv()
                elif op == "cam" or op == "c":
                   self.handleCam()
                elif op == "reload" or op == "r":
                    self.reload()
                elif op == "listen" or op == "l":
                    self.listen_to()
                elif op == "database" or op == "d":
                    self.database_config()
                elif op == "h" or op == "help":
                    Server.options()
            except KeyboardInterrupt:
                print("\nAbbruch!")
                exit(1)
