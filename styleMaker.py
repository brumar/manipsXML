from mekk.xmind import XMindDocument
import xml.etree.ElementTree as ET
import shutil
import zipfile
import os
import myCanevasReader

# Definition of all the canevas available
canevas_dictionary={"ex":[ET.Element("style"), "exemple"],"code2":ET.Element("style2")}


ET.register_namespace("fo","http://www.w3.org/1999/XSL/Format" )
ET.register_namespace("svg","http://www.w3.org/2000/svg" )
ET.register_namespace("xhtml","http://www.w3.org/1999/xhtml" )
ET.register_namespace("xlink","http://www.w3.org/1999/xlink")
prefixStyle="{urn:xmind:xmap:xmlns:style:2.0}"
prefixContent="{urn:xmind:xmap:xmlns:content:2.0}"

pathXmind="./styleMaker"

def proceed(source_filename,output_filename):
    canevas=myCanevasReader.CanevasDic()
    canevas.read("canev.xml")
    unzip(source_filename,pathXmind)

    contentxmlRoot=ET.parse(pathXmind+"/"+"content.xml").getroot()
    styleIdList,contentxmlRoot=updateTopics(contentxmlRoot,canevas)
    writeXML(contentxmlRoot,"content.xml")

    stylexmlRoot=ET.parse(pathXmind+"/"+"styles.xml").getroot()
    stylexmlRoot=addStyles(stylexmlRoot,styleIdList,canevas)
    writeXML(stylexmlRoot,"styles.xml")
    saveAndOpen(output_filename)

def saveAndOpen(output_filename):
    zipf=zipfile.ZipFile(output_filename, 'w')
    zipdir(pathXmind+"/", zipf)
    zipf.close()
    #if sys.platform == "win32":
    #    os.startfile(output_filename)
    os.open(output_filename, 1)
def updateTopics(contentxmlRoot,canevas):
    listOfStyleIds=[]
    topics=contentxmlRoot.findall(".//"+prefixContent+"topic")
    for t in topics:
        text=t.find(prefixContent+"title").text
        if(text!=None):
            code = extractCode(text)
            print(code)
            print( canevas.matchingTextDic.keys())
            if (code in canevas.matchingTextDic.keys()):
                styleID=canevas.matchingTextDic[code][1]
                listOfStyleIds.append(styleID)
                text2=text.replace(","+code+" ","")
                t.find(prefixContent+"title").text=text2
                t.set("style-id",styleID)
    return listOfStyleIds,contentxmlRoot


def extractCode(text):
    # If the text of the topic starts by ",", return the code in this topic
    if(text[0] == ","):
        i = 1
        code = ""
        while(i < len(text)):
            if text[i] == " ":
                if i > 1:
                    return text[1:i]
                else: #i == 1, no code !
                    return None
            i+=1
        # If we get here, we never found a "space"
        return None
    else: #Not a code
        return None

def writeXML(xmlRoot,xmlFile):
    xmlString=ET.tostring(xmlRoot,encoding="UTF-8",method="xml")
    xmlString=xmlString.replace("ns0:","")
    with open(pathXmind+"/"+xmlFile,"w")as f:
        f.write(xmlString)

def updateFile(filename):
    unzip(filename,pathXmind)

def voidPath():
    for root, dirs, files in os.walk(pathXmind):
        for fil in files:
            os.remove(fil)

def unzip(source_filename, dest_dir):
    zf=zipfile.ZipFile(source_filename)
    zf.extractall(dest_dir)
    zf.close()

def zipdir(path, zipfile):
    os.chdir(path)
    try:
        for root, dirs, files in os.walk("."):
            for fil in files:
                print(dirs)
                print(fil)
                print(root)
                print(os.path.join(root, fil))
                zipfile.write(os.path.join(root, fil))
    finally:
        os.chdir("..")

def addStyles(xmlRoot,styleIdList,canevas):
    styles=xmlRoot.findall(prefixStyle+"styles")
    if(styles==[]):
        styles=ET.SubElement(xmlRoot,"styles")
    else:
        styles=styles[0]
    for styleId in styleIdList:
        element=canevas.idstyle[styleId]
        styles.extend(element)
    return xmlRoot

if __name__=="__main__":
    source_filename=raw_input("input : ")
    output_filename=raw_input("output : ")
    proceed(source_filename,output_filename)

