import sys
from pathlib import Path

from reportBuilder import netherlands, default, sharedFuncts
from xmlSchema import xmlSchema

__author__ = "Christian Roberts"

def main(quarter, year, countryMS, pspId, partNumber, partTotal, messageTypeIndic, pspIdType, name, nameType, fileList):

    schema = xmlSchema.xmlSchema()
    
    paymentDataBody = sharedFuncts.paymentDataBody(pspId, pspIdType, name, nameType, fileList, countryMS)

    match(countryMS):
        case "NL" :
            schema.addElement(netherlands.build(messageTypeIndic, countryMS, quarter, year, paymentDataBody))

        case _:
            schema.addElement(default.build(messageTypeIndic, countryMS, quarter, year, paymentDataBody))

    #out
    fileName = f"PMT-{quarter}-{year}-{countryMS}-{pspId}-{partNumber}-{partTotal}.xml"
    filePath = Path(sys.argv[0]).parent.absolute().__str__()+"/out/"
    schema.toFile(fileName, filePath)