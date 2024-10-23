import legend
import globals
from xmlSchema import xmlElement
from reportBuilder import sharedFuncts

__author__ = "Christian Roberts"

def address(df, countryMS):

    addresslist = ["Street", 
                   "BuildingIdentifier", 
                   "SuiteIdentifier", 
                   "FloorIdentifier",
                   "DistrictName", 
                   "POB", 
                   "PostCode", 
                   "City", 
                   "CountrySubentity"]

    countryCode = xmlElement.xmlElement("CountryCode", "cm", countryMS, True)

    addressFree = xmlElement.xmlElement("AddressFree", "cm", None, True)

    child = ""
    for i in addresslist:
        cell = df.iat[-1,legend.__fieldOrder__.index(i)]
        child = f"{child} {str(cell)}"

    addressFree.addChild(" ".join(child.split()))

    address = xmlElement.xmlElement("Address", "cesop")
    address.updateAttrib("legalAddressType", df.iat[-1,legend.__fieldOrder__.index("legalAddressType")].replace(' ',''))
    address.addChildren([countryCode, addressFree])

    return address
    
def build(messageTypeIndic, countryMS, quarter, year, paymentDataBody):
    cesop = xmlElement.xmlElement("CESOP", "cesop")

    cesop.addChildren([sharedFuncts.msgSpec(messageTypeIndic, countryMS, quarter, year), paymentDataBody])

    cesop.updateAttrib("xmlns:cm", f"urn:eu:taxud:commontypes:v{globals.__COMMON_TYPES_V__}")
    cesop.updateAttrib("xmlns:cesop", f"urn:ec.europa.eu:taxud:fiscalis:cesop:v{globals.__FISCALIS_CESOP_V__}")
    cesop.updateAttrib("version", globals.__CESOP_VERSION__)

    return cesop