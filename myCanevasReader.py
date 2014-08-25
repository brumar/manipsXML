import xml.etree.ElementTree as ET
import string


xmlFile="canev.xml"

class CanevasDic():
    def __init__(self):
        self.markerDic={}
        self.matchingTextDic={}
        self.idstyle={}

    def addmarker(self,marker,element,idStyle):
        self.markerDic[marker]=[element,idStyle]

    def addcode(self,code,element,idStyle):
        self.matchingTextDic[code]=[element,idStyle]

    def addId(self,code, element,idStyle):
        self.idstyle[idStyle]=element

    def read(self,xmlFile):
        root=ET.parse(xmlFile).getroot()
        for canev in root:
            code=canev.find("text").get("code")
            marker=canev.find("marker").get("markerId")
            element=canev.find("style")
            idStyle=canev.find("style").get("id")
            self.addcode(code, element,idStyle)
            self.addmarker(marker, element,idStyle)
            self.addId(code, element, idStyle)

c=CanevasDic()
c.read(xmlFile)
print(c.markerDic)
print(c.matchingTextDic)
print(c.idstyle)

