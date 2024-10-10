#xml version 1.0
#UTF-8 encoding

from xmlSchema import xmlElement

__author__ = "Christian Roberts"

class xmlSchema:

    def __init__(self):
        self.prolog = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        self.content = {}

    def addElement(self, element):
        self.content[element.getTag()] = element

    def toFile(self, fileName, filePath):
        file = open(filePath+fileName, "w", encoding="utf-8")

        file.write(self.__str__())

        file.close()
        
    def __str__(self) -> str:
        out = f"{self.prolog}"

        for i in self.content:
            out = out + self.content[i].__str__()
            
        return out
