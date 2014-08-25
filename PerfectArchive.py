from mekk.xmind import XMindDocument
import xml.etree.ElementTree as ET
import shutil
import zipfile
import os

markerArchive="markersSketchyXMP.xmp"
originalMarkerDir="markersSketchy/"
targetArchiveDir="markersSketchyXMP/"

def voidPath():
    for root, dirs, files in os.walk(targetArchiveDir):
        for fil in files:
            if (fil!="markerSheet.xml"):
                os.remove(targetArchiveDir+fil)


def processXmindFile(filename):
    voidPath()
    xmindDoc=XMindDocument.open(filename)
    s1=xmindDoc.get_first_sheet()
    r1=s1.get_root_topic()
    values=xmindWalk_getMarkers(r1,[])
    markers=ET.parse(targetArchiveDir+"markerSheet.xml").getroot().getchildren()[0]
    dico=buildDico(markers)
    createArchive(dico,values)
    attachXMP(filename,xmindDoc)

def attachXMP(filename,xmindDoc):
    xmindDoc.embed_markers(markerArchive)
    xmindDoc.save(filename)

def createArchive(dico,values):
    for val in values:
        print(dico[val])
        shutil.copyfile(originalMarkerDir+dico[val],targetArchiveDir+dico[val])
        zipf=zipfile.ZipFile(markerArchive, 'w')
        zipdir(targetArchiveDir, zipf)
        zipf.close()

def buildDico(markers):
    dico={}
    for marker in markers:
        i=marker.get("id")
        r=marker.get("resource")
        dico[i]=r
    return dico


def zipdir(path, zipfile):
    os.chdir(path)
    try:
        for root, dirs, files in os.walk("."):
            for fil in files:
                print(fil)
                zipfile.write(fil)
    finally:
        os.chdir("..")


def xmindWalk_getMarkers(topic,values=[]):
    topics=topic.get_subtopics()
    for subtopic in topics:
        markers=subtopic.get_markers()
        for marker in markers:
            values.append(marker)
        xmindWalk_getMarkers(subtopic,values)
    return values

if __name__ == "__main__":
    filename=raw_input("filename : ")
    processXmindFile(filename)


# In[ ]:



