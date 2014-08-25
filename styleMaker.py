from mekk.xmind import XMindDocument
import xml.etree.ElementTree as ET
import shutil
import zipfile
import os

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

    unzip(source_filename,pathXmind)
    stylexmlRoot=ET.parse(pathXmind+"/"+"styles.xml").getroot()
    addStyles(stylexmlRoot)
    writeXML(stylexmlRoot,"styles.xml")

    contentxmlRoot=ET.parse(pathXmind+"/"+"content.xml").getroot()
    updateTopics(contentxmlRoot)
    writeXML(contentxmlRoot,"content.xml")

    saveAndOpen(output_filename)

def saveAndOpen(output_filename):
    zipf=zipfile.ZipFile(output_filename, 'w')
    zipdir(pathXmind+"/", zipf)
    zipf.close()
    os.startfile(output_filename)

def updateTopics(contentxmlRoot):
    topics=contentxmlRoot.findall(".//"+prefixContent+"topic")


    for t in topics:
        text=t.find(prefixContent+"title").text
        if(text!=None):
            code = extractCode(text)
            if not(code in canevas_dictionary.keys()):
                #error : the code isn't recognized doesn't do anything, we skip to the next topic
                continue


            #1) modification of content.xml
            #2) modification of styles.xml
            #3) we must now suppress the code from the text of the topic 
            # + Other modifications of the text depending on the canvas
            


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

def addStyles(xmlRoot):
    styles=xmlRoot.findall(prefixStyle+"styles")
    if(styles==[]):
        styles=ET.SubElement(xmlRoot,"styles")
    else:
        styles=styles[0]
    s=ET.SubElement(styles,"style")
    s.set("id","connector")
    s.set("type","topic")
    prop=ET.SubElement(s,"topic-properties")
    prop.set("fo:color","#808080")
    prop.set("shape-class","org.xmind.topicShape.noBorder")
    return styles

if __name__=="__main__":
    source_filename=raw_input("input : ")
    output_filename=raw_input("output : ")
    proceed(source_filename,output_filename)

