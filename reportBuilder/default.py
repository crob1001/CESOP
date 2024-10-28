import legend
import globals
from xmlSchema import xmlElement
from reportBuilder import sharedFuncts

__author__ = "Christian Roberts"
    
def build(messageTypeIndic, countryMS, quarter, year, paymentDataBody):
    cesop = xmlElement.xmlElement("CESOP", "cesop")

    cesop.addChildren([sharedFuncts.msgSpec(messageTypeIndic, countryMS, quarter, year), paymentDataBody])

    cesop.updateAttrib("xmlns:cm", f"urn:eu:taxud:commontypes:v{globals.__COMMON_TYPES_V__}")
    cesop.updateAttrib("xmlns:cesop", f"urn:ec.europa.eu:taxud:fiscalis:cesop:v{globals.__FISCALIS_CESOP_V__}")
    cesop.updateAttrib("version", globals.__CESOP_VERSION__)

    return cesop