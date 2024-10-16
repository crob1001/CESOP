import globals
import legend
from xmlSchema import xmlElement
from reportBuilder import sharedFuncts

__author__ = "Christian Roberts"

def NLAddress(address, countryMS, df):
    address.setInline(False)
    address.updateAttrib("legalAddressType", df.iat[-1,legend.__fieldOrder__.index("legalAddressType")].replace(' ', ))

    countryCode = xmlElement.xmlElement("cm:CountryCode", countryMS, True)
    addressFix = xmlElement.xmlElement("cm:AddressFix", None, False)

    street = xmlElement.xmlElement("cm:Street", df.iat[-1,legend.__fieldOrder__.index("Street")], True)
    postCode = xmlElement.xmlElement("cm:PostCode", df.iat[-1,legend.__fieldOrder__.index("PostCode")], True)
    city = xmlElement.xmlElement("cm:City", df.iat[-1,legend.__fieldOrder__.index("City")], True)
    countrySubentity = xmlElement.xmlElement("cm:CountrySubentity", df.iat[-1,legend.__fieldOrder__.index("CountrySubentity")], True)

    addressFix.addChildren([street, postCode, city, countrySubentity])

    address.addChildren([countryCode, addressFix])

def NLMsgSpec(messageTypeIndic, countryMS, quarter, year):
    msgSpec = sharedFuncts.msgSpec(messageTypeIndic, countryMS, quarter, year)

    msgSpec.setTag("pspnl:" + msgSpec.getTag())

    for i in msgSpec.children:
        if isinstance(i, xmlElement.xmlElement):
            i.setTag("cesop:" + i.getTag())
        for j in i.children:
            if isinstance(j, xmlElement.xmlElement):
                j.setTag("cesop:" + j.getTag())

    return msgSpec

def PSPNL():
    pspNL = xmlElement.xmlElement("pspnl:PSPNL")
    pspNL.updateAttrib("xmlns:cm", "urn:eu:taxud:commontypes:v1")
    pspNL.updateAttrib("xmlns:cesop", "urn:ec.europa.eu:taxud:fiscalis:cesop:v1")
    pspNL.updateAttrib("xmlns:xsi","http://www.w3.org/2001/xmlSchema-instance")
    pspNL.updateAttrib("xmlns:idnl","http://xml.belastingdienst.nl/schemas/IDNL/1.0")
    pspNL.updateAttrib("xmlns:pspnl","http://xml.belastingdienst.nl/schemas/PSPNL/1.0")
    pspNL.updateAttrib("versionNL", "1.0")
    pspNL.updateAttrib("xsi:schemaLocation","http://xml.belastingdienst.nl/schemas/PSPNL/1.0 file:///Q:/IV/BCA-UIM_VIA/aanslag-werk/2300%20HL%20gegevensaanleveringen/HL-PSP%20(CESOP)/PSP_1.0/XSD/XSD_PSPNL_1.0_R20230210/PSPNL_1.0_V1.20230210.xsd")

    pspNLHeader = xmlElement.xmlElement("pspnl:PSPNL_Header")

    rsin = xmlElement.xmlElement("idnl:RSIN", globals.__RSIN__, True)
    kvk = xmlElement.xmlElement("idnl:KVK", globals.__KVK__,  True)

    pspNLHeader.addChildren([rsin, kvk])

    pspNL.addChild(pspNLHeader)

    return pspNL

def addCesopToTag(element):
    if isinstance(element, xmlElement.xmlElement):
        for i in element.children:
            addCesopToTag(i)
        if "type" in element.getTag().lower():
            element.setTag("cm:" + element.getTag())
        else:
            element.setTag("cesop:" + element.getTag())

def build(messageTypeIndic, countryMS, quarter, year, paymentDataBody):
    cesop = xmlElement.xmlElement("pspnl:CESOP")
    cesop.updateAttrib("version", globals.__cesopVersion__)

    pspNL = PSPNL()

    paymentDataBody.setTag("pspnl:" + paymentDataBody.getTag())

    for i in paymentDataBody.children:
        addCesopToTag(i)

    cesop.addChildren([NLMsgSpec(messageTypeIndic, countryMS, quarter, year),
                        paymentDataBody])
    
    pspNL.addChild(cesop)

    return pspNL