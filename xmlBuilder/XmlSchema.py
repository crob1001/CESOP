from pathlib import Path
import sys

#xml version 1.0
#UTF-8 encoding

__author__ = "Christian Roberts"

class XmlSchema:

    def __init__(self):
        # self.fileName = ""
        self.prolog = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        self.content = {}

    def addElement(self, element):
        self.content[element.getTag()] = element

    def toFile(self, quarter, year, countryMS, pspId, partNumber, partTotal):
        filePath = Path(sys.argv[0]).parent.absolute().__str__()+"/out/"
        fileName = f"PMT-{quarter}-{year}-{countryMS}-{pspId}-{partNumber}-{partTotal}.xml"

        file = open(filePath+fileName, "w", encoding="utf-8")

        file.write(self.__str__())

        file.close()
        
    def __str__(self) -> str:
        out = f"{self.prolog}"
        for i in self.content:
            out = f"{out}{self.content[i].__str__()}"
        return out