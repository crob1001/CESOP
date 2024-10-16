import legend
import globals
from xmlSchema import xmlElement
from reportBuilder import sharedFuncts

__author__ = "Christian Roberts"

def address(address, countryMS, df):
    address.updateAttrib("legalAddressType", df.iat[-1,legend.__fieldOrder__.index("legalAddressType")].replace(' ',''))
    address.addChild(xmlElement.xmlElement(
        "AddressFree",
        (" ".join(f'{df.iat[-1,legend.__fieldOrder__.index("Street")]} {df.iat[0,legend.__fieldOrder__.index("BuildingIdentifier")]} {df.iat[0,legend.__fieldOrder__.index("SuiteIdentifier")]} {df.iat[0,legend.__fieldOrder__.index("FloorIdentifier")]} {df.iat[0,legend.__fieldOrder__.index("DistrictName")]} {df.iat[0,legend.__fieldOrder__.index("POB")]} {df.iat[0,legend.__fieldOrder__.index("PostCode")]} {df.iat[0,legend.__fieldOrder__.index("City")]} {df.iat[0,legend.__fieldOrder__.index("CountrySubentity")]}'.split()))
        ))
    
def build(messageTypeIndic, countryMS, quarter, year, paymentDataBody):
    cesop = xmlElement.xmlElement("CESOP")
    cesop.updateAttrib("version", globals.__cesopVersion__)

    cesop.addChildren([sharedFuncts.msgSpec(messageTypeIndic, countryMS, quarter, year),
                        paymentDataBody])
    
    cesop.updateAttrib("xmlns", f"urn:ec.europa.eu:taxud:fiscalis:cesop:v{globals.__xmlVersion__.split('.')[0]}")

    return cesop