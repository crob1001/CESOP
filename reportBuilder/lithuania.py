import globals
from xmlSchema import xmlElement
from reportBuilder import default

def build(messageTypeIndic, countryMS, quarter, year, paymentDataBody):

    cesop = xmlElement.xmlElement("pspnl:CESOP")
    cesop.updateAttrib("version", globals.__cesopVersion__)

    cesop = default.build(cesop, messageTypeIndic, countryMS, quarter, year, paymentDataBody)
    cesop.updateAttrib("xmlns", f"urn:ec.europa.eu:taxud:fiscalis:cesop:v{globals.__xmlVersion__.split('.')[0]}")

    return cesop