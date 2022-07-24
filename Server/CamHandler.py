import cv2 as cv
import json
import requests
from io import BytesIO
import numpy as np

from Server.utils import append_parent_dir, loadJson, saveJson

append_parent_dir()
from privates import *


class CamHandler:

    def __init__(self):
        self.camDict = loadJson(CAM_DICT_PATH)

    def close(self):
        saveJson(self.camDict)

    def possibleCams(self):
        for name in self.camDict.keys():
            url = self.camDict[name]
            print(f"[{name}] ({url})")

    def newCam(self):
        text = input("name of new cam\n>> ")
        url = input("url of new cam\n>> ")
        self.camDict[text] = url
        saveJson(CAM_DICT_PATH,self.camDict)
        print("Sucessfully saved cam %s\n" % text)

    def chooseCam(self):
        self.possibleCams()
        text = input("which cam\n>> ")
        url = self.camDict[text]
        if url == None:
            print("keine cam mit der bezeichnung {opt} gefunden")
        self.showCam(text, url)

    def showCam(self, name, url):
        res = requests.get(url, stream=True)
        print(name + " starts streaming")
        for chunk in res.iter_content(chunk_size=120000):
            if len(chunk) > 100:
                try:
                    img_data = BytesIO(chunk)
                    img = cv.imdecode(np.frombuffer(
                        img_data.read(), np.uint8), 1)
                    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                    cv.imshow(name, img)
                except Exception as e:
                    print(str(e))
                    continue
            if cv.waitKey(1) == ord("q"):
                cv.destroyAllWindows()
                print(name + " stops streaming")
                break
