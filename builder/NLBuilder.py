import globals
import builder.defaultBuilder
from xmlBuilder import XmlElement

def buildPSPNL() -> XmlElement:
    pspNL = XmlElement.XmlElement("pspnl:PSPNL")
    pspNL.updateAttrib("xmlns:cm", "urn:eu:taxud:commontypes:v1")
    pspNL.updateAttrib("xmlns:cesop", "urn:ec.europa.eu:taxud:fiscalis:cesop:v1")
    pspNL.updateAttrib("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
    pspNL.updateAttrib("xmlns:idnl","http://xml.belastingdienst.nl/schemas/IDNL/1.0")
    pspNL.updateAttrib("xmlns:pspnl","http://xml.belastingdienst.nl/schemas/PSPNL/1.0")
    pspNL.updateAttrib("versionNL", "1.0")
    pspNL.updateAttrib("xsi:schemaLocation","http://xml.belastingdienst.nl/schemas/PSPNL/1.0 file:///Q:/IV/BCA-UIM_VIA/aanslag-werk/2300%20HL%20gegevensaanleveringen/HL-PSP%20(CESOP)/PSP_1.0/XSD/XSD_PSPNL_1.0_R20230210/PSPNL_1.0_V1.20230210.xsd")

    pspNLHeader = XmlElement.XmlElement("pspnl:PSPNL_Header")

    rsin = XmlElement.XmlElement("idnl:RSIN", globals.__RSIN__, True)
    kvk = XmlElement.XmlElement("idnl:KVK", globals.__KVK__,  True)

    pspNLHeader.addChildren([rsin, kvk])

    pspNL.addChild(pspNLHeader)

    return pspNL

def buildNLMsgSpec(MessageTypeIndic, countryMS, quarter, year):
    msgSpec = builder.defaultBuilder.build(MessageTypeIndic, countryMS, quarter, year)

    msgSpec.setTag("pspnl:" + msgSpec.getTag())

    for i in msgSpec.children:
        if isinstance(i, XmlElement.XmlElement):
            i.setTag("cesop:" + i.getTag())
        for j in i.children:
            if isinstance(j, XmlElement.XmlElement):
                j.setTag("cesop:" + j.getTag())

    return msgSpec

def build(MessageTypeIndic, countryMS, quarter, year, paymentDataBody):
    cesop = XmlElement.XmlElement("pspnl:CESOP")
    cesop.updateAttrib("version", globals.__cesopVersion__)
    
    pspNL = buildPSPNL()
    
    paymentDataBody.setTag("pspnl:" + paymentDataBody.getTag())

    for i in paymentDataBody.children:
        if isinstance(i, XmlElement.XmlElement):
            i.setTag("cesop:" + i.getTag())
        for j in i.children:
            if isinstance(j, XmlElement.XmlElement):
                if j.getTag() == "TAXIdentification":
                    # i.children.remove(j)
                    j.children.clear()
                    j.setInline(True)
                    continue
                j.setTag("cesop:" + j.getTag())

    cesop.addChildren([buildNLMsgSpec(MessageTypeIndic, countryMS, quarter, year),
                        paymentDataBody])
    pspNL.addChild(cesop)