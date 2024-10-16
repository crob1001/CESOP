import legend
import globals
from xmlSchema import xmlElement
from reportBuilder import sharedFuncts

__author__ = "Christian Roberts"

def address(df):

    addresslist = ["Street", 
                   "BuildingIdentifier", 
                   "SuiteIdentifier", 
                   "FloorIdentifier",
                   "DistrictName", 
                   "POB", 
                   "PostCode", 
                   "City", 
                   "CountrySubentity"]
    
    address = xmlElement.xmlElement("Address")
    address.updateAttrib("legalAddressType", df.iat[-1,legend.__fieldOrder__.index("legalAddressType")].replace(' ',''))

    addressFix = xmlElement.xmlElement("AddressFix")

    for i in addresslist:
        cell = df.iat[-1,legend.__fieldOrder__.index(i)]
        addressFix.addChild(xmlElement.xmlElement(i, str(cell), True))

    address.addChild(addressFix)

    return address
    
    
def build(messageTypeIndic, countryMS, quarter, year, paymentDataBody):
    cesop = xmlElement.xmlElement("CESOP")
    cesop.updateAttrib("version", globals.__cesopVersion__)

    cesop.addChildren([sharedFuncts.msgSpec(messageTypeIndic, countryMS, quarter, year),
                        paymentDataBody])
    
    cesop.updateAttrib("xmlns", f"urn:ec.europa.eu:taxud:fiscalis:cesop:v{globals.__xmlVersion__.split('.')[0]}")

    return cesop