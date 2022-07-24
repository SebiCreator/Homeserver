import sys
import os
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    G_TEXT = '\33[90m'


def printError(category: str, msg: str):
    print(bcolors.FAIL + "[%s]\t" %
          category + bcolors.G_TEXT + msg + bcolors.ENDC)


def printWarning(category: str, msg: str):
    print(bcolors.WARNING + "[%s]\t" %
          category + bcolors.G_TEXT + msg + bcolors.ENDC)


def printSucess(category: str, msg: str):
    print(bcolors.OKGREEN+ "[%s]\t" %
          category + bcolors.G_TEXT + msg + bcolors.ENDC)

def loadJson(PATH):
    with open(PATH) as file:
        return json.load(file)

def saveJson(PATH,data):
    with open(PATH,"w") as outfile:
        json.dump(data,outfile)

def disablePrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__

    

def append_parent_dir():
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)