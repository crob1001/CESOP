import sys
from pathlib import Path

from builder import NLBuilder, defaultBuilder
from xmlBuilder import XmlSchema

__author__ = "Christian Roberts"

def buildaccountIdentifiers() -> list:
    pass

def build(quarter, year, countryMS, pspId, partNumber, partTotal, MessageTypeIndic, pspIdType, name, nameType, fileList):
    schema = XmlSchema.XmlSchema()

    paymentDataBody = defaultBuilder.buildPaymentDataBody(pspId, pspIdType, name, nameType, fileList, countryMS)

    match(countryMS):
        case "NL" :
            schema.addElement(NLBuilder.build(MessageTypeIndic, countryMS, quarter, year, paymentDataBody))

        case _:
            schema.addElement(defaultBuilder.build(MessageTypeIndic, countryMS, quarter, year, paymentDataBody))

    #out
    fileName = f"PMT-{quarter}-{year}-{countryMS}-{pspId}-{partNumber}-{partTotal}.xml"
    filePath = Path(sys.argv[0]).parent.absolute().__str__()+"/out/"
    schema.toFile(fileName, filePath)