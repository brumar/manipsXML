import os
from mekk.xmind import XMindDocument

def updateMarkers(filename):
    xmindfile = XMindDocument.open(filename)
    xmindfile.embed_markers("livemappingMarkers.xmp")
    xmindfile.save(filename)

class DirectoryWalker:

    def __init__(self, directory):
        self.stack = [directory]
        self.files = []
        self.index = 0

    def __getitem__(self, index):
        while 1:
            try:
                f = self.files[self.index]
                self.index = self.index + 1
            except IndexError:
                # pop next directory from stack
                self.directory = self.stack.pop()
                self.files = os.listdir(self.directory)
                self.index = 0
            else:
                # got a filename
                fullname = os.path.join(self.directory, f)
                if os.path.isdir(fullname) and not os.path.islink(fullname):
                    self.stack.append(fullname)
                return fullname

files=["./EHS.xmind"]
#files=DirectoryWalker(".") # the directory targeted (all the subdirectories are recursively included in the search)
for f in files:
    if(f[-6:]==".xmind"):
        try :
            updateMarkers(f)
        except :
            print("error with file "+f)
