import globals
import legend
from xmlSchema import xmlElement
from reportBuilder import sharedFuncts

__author__ = "Christian Roberts"

def NLMsgSpec(messageTypeIndic, countryMS, quarter, year):
    msgSpec = sharedFuncts.msgSpec(messageTypeIndic, countryMS, quarter, year)

    msgSpec.setNameSpace("pspnl")

    return msgSpec

def PSPNL():
    pspNL = xmlElement.xmlElement("pspnl:PSPNL")
    pspNL.updateAttrib("xmlns:cm", f"urn:eu:taxud:commontypes:v{globals.__COMMON_TYPES_V__}")
    pspNL.updateAttrib("xmlns:cesop", f"urn:ec.europa.eu:taxud:fiscalis:cesop:v{globals.__FISCALIS_CESOP_V__}")
    pspNL.updateAttrib("xmlns:xsi","http://www.w3.org/2001/xmlSchema-instance")
    pspNL.updateAttrib("xmlns:idnl","http://xml.belastingdienst.nl/schemas/IDNL/1.0")
    pspNL.updateAttrib("xmlns:pspnl","http://xml.belastingdienst.nl/schemas/PSPNL/1.0")
    pspNL.updateAttrib("versionNL", globals.__NL_VERSION__)
    pspNL.updateAttrib("xsi:schemaLocation","http://xml.belastingdienst.nl/schemas/PSPNL/1.0 file:///Q:/IV/BCA-UIM_VIA/aanslag-werk/2300%20HL%20gegevensaanleveringen/HL-PSP%20(CESOP)/PSP_1.0/XSD/XSD_PSPNL_1.0_R20230210/PSPNL_1.0_V1.20230210.xsd")

    pspNLHeader = xmlElement.xmlElement("PSPNL_Header", "pspnl")

    rsin = xmlElement.xmlElement("RSIN", "idnl", globals.__RSIN__, True)
    kvk = xmlElement.xmlElement("KVK", "idnl", globals.__KVK__,  True)

    pspNLHeader.addChildren([rsin, kvk])

    pspNL.addChild(pspNLHeader)

    return pspNL

def build(messageTypeIndic, countryMS, quarter, year, paymentDataBody):
    cesop = xmlElement.xmlElement("pspnl:CESOP")
    cesop.updateAttrib("version", globals.__CESOP_VERSION__)

    pspNL = PSPNL()

    paymentDataBody.setTag("pspnl:" + paymentDataBody.getTag())

    cesop.addChildren([NLMsgSpec(messageTypeIndic, countryMS, quarter, year),
                        paymentDataBody])
    
    pspNL.addChild(cesop)

    return pspNL