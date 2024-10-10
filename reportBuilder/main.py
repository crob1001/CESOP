import sys
from pathlib import Path

from reportBuilder import netherlands, default, lithuania
from xmlSchema import xmlSchema

__author__ = "Christian Roberts"

def buildaccountIdentifiers() -> list:
    pass

def build(quarter, year, countryMS, pspId, partNumber, partTotal, messageTypeIndic, pspIdType, name, nameType, fileList):
    schema = xmlSchema.xmlSchema()
    
    paymentDataBody = default.buildPaymentDataBody(pspId, pspIdType, name, nameType, fileList, countryMS)

    match(countryMS):
        case "LT" :
            schema.addElement(lithuania.build(messageTypeIndic, countryMS, quarter, year, paymentDataBody))

        case "NL" :
            schema.addElement(netherlands.build(messageTypeIndic, countryMS, quarter, year, paymentDataBody))

        case _:
            schema.addElement(lithuania.build(messageTypeIndic, countryMS, quarter, year, paymentDataBody))

    #out
    fileName = f"PMT-{quarter}-{year}-{countryMS}-{pspId}-{partNumber}-{partTotal}.xml"
    filePath = Path(sys.argv[0]).parent.absolute().__str__()+"/out/"
    schema.toFile(fileName, filePath)