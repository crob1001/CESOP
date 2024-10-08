# import sys
import sys
import pandas as pd
from uuid import uuid4
from pathlib import Path
import xmlBuilder.MtElement
import xmlBuilder.XmlSchema
import xmlBuilder.XmlElement
from datetime import datetime

import globals
import legend

__author__ = "Christian Roberts"

def buildLTMsgSpec(messageTypeIndic, transmittingCountry, quarter, year):
    msgSpec = xmlBuilder.XmlElement.XmlElement("MessageSpec")

    transmitingCountry = xmlBuilder.XmlElement.XmlElement("TransmittingCountry", transmittingCountry, True)
    msgType = xmlBuilder.XmlElement.XmlElement("MessageType", "PMT", True)
    messageTypeIndic = xmlBuilder.XmlElement.XmlElement("MessageTypeIndic", messageTypeIndic, True)
    MessageRefId = xmlBuilder.XmlElement.XmlElement("MessageRefId", uuid4(), True)
    ReportingPeriod = xmlBuilder.XmlElement.XmlElement("ReportingPeriod")
    ReportingPeriod.addChildren([xmlBuilder.XmlElement.XmlElement("Quarter", quarter, True),
                                 xmlBuilder.XmlElement.XmlElement("Year", year, True)])
    Timestamp = xmlBuilder.XmlElement.XmlElement("Timestamp", datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ'), True)

    msgSpec.addChildren([transmitingCountry, msgType, messageTypeIndic, MessageRefId, ReportingPeriod,
                         Timestamp])

    return msgSpec

def buildReportingPSP(pspId, pspIdType, name, nameType):
    reportingPSP = xmlBuilder.XmlElement.XmlElement("ReportingPSP")

    pspId = xmlBuilder.XmlElement.XmlElement("PSPId", pspId, True)
    pspId.updateAttrib("PSPIdType", pspIdType)

    name = xmlBuilder.XmlElement.XmlElement("Name", name, True)
    name.updateAttrib("NameType", nameType)

    reportingPSP.addChildren([pspId, name])

    return reportingPSP

def buildPaymentMethod(paymentMethodType):

    paymentMethodType = xmlBuilder.XmlElement.XmlElement("PaymentMethodType", paymentMethodType, True)

    paymentMethod = xmlBuilder.XmlElement.XmlElement("PaymentMethod", paymentMethodType, True)

    return paymentMethod

def buildReportedTransaction(transactionIdentifier, dateTime, isRefund, transactionDateType, amount, currency, paymentMethodType,
                             initiatedAtPhysicalPremisesOfMerchant, payerMS, payerMSSource, pspRole):
    reportedTransaction = xmlBuilder.XmlElement.XmlElement("ReportedTransaction", None, True)

    reportedTransaction.updateAttrib("IsRefund", isRefund)
    
    transactionIdentifier = xmlBuilder.XmlElement.XmlElement("TransactionIdentifier", transactionIdentifier, True)

    dateTime = xmlBuilder.XmlElement.XmlElement("DateTime", dateTime, True)
    dateTime.updateAttrib("TransactionDateType", transactionDateType)

    amount = xmlBuilder.XmlElement.XmlElement("Amount", amount, True)
    amount.updateAttrib("Currency", currency)

    paymentMethod = buildPaymentMethod(paymentMethodType)

    initiatedAtPhysicalPremisesOfMerchant = xmlBuilder.XmlElement.XmlElement("InitiatedAtPhysicalPremisesOfMerchant", initiatedAtPhysicalPremisesOfMerchant, True)

    payerMS = xmlBuilder.XmlElement.XmlElement("PayerMS", payerMS, True)
    payerMS.updateAttrib("PayerMSSource", payerMSSource)

    pspRoleType = xmlBuilder.XmlElement.XmlElement("PSPRoleType", pspRole, True)
    pspRole = xmlBuilder.XmlElement.XmlElement("PSPRole", pspRoleType, False)
    
    reportedTransaction.addChildren([transactionIdentifier, dateTime, amount, paymentMethod, initiatedAtPhysicalPremisesOfMerchant,
                                     payerMS, pspRole])

    return reportedTransaction

def buildRepresentative(representativeId, pspIdType, name, nameType):
    representative = xmlBuilder.XmlElement.XmlElement("Representative")

    representativeId = xmlBuilder.XmlElement.XmlElement("RepresentativeId", representativeId, True)
    representativeId.updateAttrib("PSPIdType", pspIdType)

    name = xmlBuilder.XmlElement.XmlElement("Name", name, True)
    name.updateAttrib("NameType", nameType)

    representative.addChildren([representativeId, name])

    return representative

def buildDocSpec(docTypeIndic):
    docSpec = xmlBuilder.XmlElement.XmlElement("DocSpec")
    docTypeIndic = xmlBuilder.XmlElement.XmlElement("DocTypeIndic", docTypeIndic, True)
    docRefID = xmlBuilder.XmlElement.XmlElement("DocRefID", uuid4(), True)
    docSpec.addChildren([docTypeIndic, docRefID])
    return docSpec

def buildaccountIdentifiers() -> list:
    pass

def buildReportedPayee(df, countryMS):
    reportedPayee = xmlBuilder.XmlElement.XmlElement("ReportedPayee")

    name = xmlBuilder.XmlElement.XmlElement("Name", df.iat[0,legend.FileLocations.index("PayeeName")], True)
    name.updateAttrib("NameType", df.iat[0,legend.FileLocations.index("PayeeNameType")])

    country = xmlBuilder.XmlElement.XmlElement("Country", df.iat[0,legend.FileLocations.index("CountryCode")], True)

    address = xmlBuilder.XmlElement.XmlElement("Address", None, True)

    match(countryMS):
        
        case "NL" :
            address.setInline(False)
            address.updateAttrib("LegalAddressType", df.iat[0,legend.FileLocations.index("legalAddressType")].replace(' ',''))

            countryCode = xmlBuilder.XmlElement.XmlElement("cm:CountryCode", countryMS, True)
            addressFix = xmlBuilder.XmlElement.XmlElement("cm:AddressFix", None, False)

            street = xmlBuilder.XmlElement.XmlElement("cm:Street", df.iat[0,legend.FileLocations.index("Street")], True)
            postCode = xmlBuilder.XmlElement.XmlElement("cm:PostCode", df.iat[0,legend.FileLocations.index("PostCode")], True)
            city = xmlBuilder.XmlElement.XmlElement("cm:City", df.iat[0,legend.FileLocations.index("City")], True)
            countrySubentity = xmlBuilder.XmlElement.XmlElement("cm:CountrySubentity", df.iat[0,legend.FileLocations.index("CountrySubentity")], True)

            addressFix.addChildren([street, postCode, city, countrySubentity])

            address.addChildren([countryCode, addressFix])
        
        case _ :
            address.updateAttrib("LegalAddressType", df.iat[0,legend.FileLocations.index("legalAddressType")].replace(' ',''))
            address.addChild(" ".join(f'{df.iat[0,legend.FileLocations.index("Street")]} {df.iat[0,legend.FileLocations.index("BuildingIdentifier")]} {df.iat[0,legend.FileLocations.index("SuiteIdentifier")]} {df.iat[0,legend.FileLocations.index("FloorIdentifier")]} {df.iat[0,legend.FileLocations.index("DistrictName")]} {df.iat[0,legend.FileLocations.index("POB")]} {df.iat[0,legend.FileLocations.index("PostCode")]} {df.iat[0,legend.FileLocations.index("City")]} {df.iat[0,legend.FileLocations.index("CountrySubentity")]}'.split()))
    
    # emailAddress = xmlBuilder.XmlElement.XmlElement("EmailAddress", df.iat[0,legend.FileLocations.index("EmailAddress")], True)

    # webPage = xmlBuilder.XmlElement.XmlElement("WebPage", df.iat[0,legend.FileLocations.index("WebPage")], True)

    taxIdentification = xmlBuilder.XmlElement.XmlElement("TAXIdentification", None, False)

    VATId = xmlBuilder.XmlElement.XmlElement("VATId", df.iat[0,legend.FileLocations.index("VATId")],True)
    VATId.updateAttrib("issuedBy", df.iat[0,19])

    TAXId = xmlBuilder.XmlElement.XmlElement("TAXId", df.iat[0,legend.FileLocations.index("TAXId")], True)
    TAXId.updateAttrib("issuedBy", df.iat[0,legend.FileLocations.index("issuedByTAX")])
    TAXId.updateAttrib("type", df.iat[0,legend.FileLocations.index("typeTAX")])

    # taxIdentification.addChildren([VATId, TAXId])

    reportedPayee.addChildren([name, country, address#, emailAddress, webPage
                               ,taxIdentification])

    i = 0

    accountIdentifiers = []
    
    while i < len(df.index):
        exists = False
        for j in accountIdentifiers:
            if j == df.iat[i,legend.FileLocations.index("AccountIdentifier")]:
                exists = True
        if exists == False:
            accountIdentifiers.append(df.iat[i,legend.FileLocations.index("AccountIdentifier")])
            accountIdentifier = xmlBuilder.XmlElement.XmlElement("AccountIdentifier", df.iat[i,legend.FileLocations.index("AccountIdentifier")], True)
            accountIdentifier.updateAttrib("CountryCode", df.iat[i,legend.FileLocations.index("CountryCode")])
            accountIdentifier.updateAttrib("Type", df.iat[i,legend.FileLocations.index("typeAccount")])
            reportedPayee.addChild(accountIdentifier)
        i+=1

    i = 0

    while i < len(df.index):
        reportedPayee.addChild(buildReportedTransaction(df.iat[i,legend.FileLocations.index("TransactionIdentifier")], df.iat[i,legend.FileLocations.index("DateTime")],
                                                        df.iat[i,legend.FileLocations.index("IsRefund")], df.iat[i,legend.FileLocations.index("transactionDateType")],
                                                        df.iat[i,legend.FileLocations.index("Amount")], df.iat[i,legend.FileLocations.index("currency")],
                                                        df.iat[i,legend.FileLocations.index("PaymentMethodType")], df.iat[i,legend.FileLocations.index("InitiatedAtPhysicalPremisesOfMerchant")],
                                                        df.iat[i,legend.FileLocations.index("PayerMS")], df.iat[i,legend.FileLocations.index("PayerMSSource")],
                                                        df.iat[i,legend.FileLocations.index("PSPRoleType")]))
        i+=1

    # reportedPayee.addChild(buildRepresentative(df.iat[0,legend.FileLocations.index("RepresentativeId")], df.iat[0,legend.FileLocations.index("PSPIdType")], df.iat[0,legend.FileLocations.index("Name")], df.iat[0,legend.FileLocations.index("NameType")]))

    reportedPayee.addChild(buildDocSpec(df.iat[0,legend.FileLocations.index("DocTypeIndic")]))

    reportedPayee.addChild(xmlBuilder.MtElement.MtElement())

    return reportedPayee

def buildPaymentDataBody(pspId, pspIdType, name, nameType, fileList, countryMS):
    paymentDataBody = xmlBuilder.XmlElement.XmlElement("PaymentDataBody")

    paymentDataBody.addChild(buildReportingPSP(pspId, pspIdType, name, nameType))

    for i in fileList:
        with open(i, 'rb') as f:
            file = pd.read_excel(f).fillna('')

        dfs = file.groupby(['PayeeName', 'CountryCode'])

        for countryCode, payeeName in dfs:
            group = dfs.get_group(countryCode)
            paymentDataBody.addChild(buildReportedPayee(group, countryMS))

    return paymentDataBody

def buildPSPNL() -> xmlBuilder.XmlElement:
    pspNL = xmlBuilder.XmlElement.XmlElement("pspnl:PSPNL")
    pspNL.updateAttrib("xmlns:cm", "urn:eu:taxud:commontypes:v1")
    pspNL.updateAttrib("xmlns:cesop", "urn:ec.europa.eu:taxud:fiscalis:cesop:v1")
    pspNL.updateAttrib("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
    pspNL.updateAttrib("xmlns:idnl","http://xml.belastingdienst.nl/schemas/IDNL/1.0")
    pspNL.updateAttrib("xmlns:pspnl","http://xml.belastingdienst.nl/schemas/PSPNL/1.0")
    pspNL.updateAttrib("versionNL", "1.0")
    pspNL.updateAttrib("xsi:schemaLocation","http://xml.belastingdienst.nl/schemas/PSPNL/1.0 file:///Q:/IV/BCA-UIM_VIA/aanslag-werk/2300%20HL%20gegevensaanleveringen/HL-PSP%20(CESOP)/PSP_1.0/XSD/XSD_PSPNL_1.0_R20230210/PSPNL_1.0_V1.20230210.xsd")

    pspNLHeader = xmlBuilder.XmlElement.XmlElement("pspnl:PSPNL_Header")

    rsin = xmlBuilder.XmlElement.XmlElement("idnl:RSIN", globals.__RSIN__, True)
    kvk = xmlBuilder.XmlElement.XmlElement("idnl:KVK", globals.__KVK__,  True)

    pspNLHeader.addChildren([rsin, kvk])

    pspNL.addChild(pspNLHeader)

    return pspNL

def buildNLMsgSpec(MessageTypeIndic, countryMS, quarter, year):
    msgSpec = buildLTMsgSpec(MessageTypeIndic, countryMS, quarter, year)

    msgSpec.setTag("pspnl:" + msgSpec.getTag())

    for i in msgSpec.children:
        if isinstance(i, xmlBuilder.XmlElement.XmlElement):
            i.setTag("cesop:" + i.getTag())
        for j in i.children:
            if isinstance(j, xmlBuilder.XmlElement.XmlElement):
                j.setTag("cesop:" + j.getTag())

    # msgSpec.insertChild(xmlBuilder.XmlElement.XmlElement("CorrMessageRefId", "", True), 4)

    # sendingPSP = xmlBuilder.XmlElement.XmlElement("SendingPSP")

    # pspID = xmlBuilder.XmlElement.XmlElement("PSPId", globals.__sendingPSPID__, True)
    # pspID.updateAttrib("PSPIdType", globals.__sendingPSPID__)

    # name = xmlBuilder.XmlElement.XmlElement("Name", globals.__sendingPSPName__, True)
    # name.updateAttrib("NameType", globals.__sendingPSPNameType__)

    # sendingPSP.addChildren([pspID, name])

    # msgSpec.insertChild(sendingPSP, 5)

    # sendingPSP.addChild

    return msgSpec

def build(quarter, year, countryMS, pspId, partNumber, partTotal, MessageTypeIndic, pspIdType, name, nameType, fileList):
    #schema
    schema = xmlBuilder.XmlSchema.XmlSchema()

    paymentDataBody = buildPaymentDataBody(pspId, pspIdType, name, nameType, fileList, countryMS)

    match(countryMS):
        case "NL" :
            #cesop Element
            cesop = xmlBuilder.XmlElement.XmlElement("pspnl:CESOP")
            cesop.updateAttrib("version", globals.__cesopVersion__)
            
            pspNL = buildPSPNL()
            
            
            paymentDataBody.setTag("pspnl:" + paymentDataBody.getTag())

            for i in paymentDataBody.children:
                # print(i.getTag())
                if isinstance(i, xmlBuilder.XmlElement.XmlElement):
                    i.setTag("cesop:" + i.getTag())
                for j in i.children:
                    if isinstance(j, xmlBuilder.XmlElement.XmlElement):
                        if j.getTag() == "TAXIdentification":
                            # i.children.remove(j)
                            j.children.clear()
                            j.setInline(True)
                            continue
                        j.setTag("cesop:" + j.getTag())

            cesop.addChildren([buildNLMsgSpec(MessageTypeIndic, countryMS, quarter, year),
                               paymentDataBody])
            pspNL.addChild(cesop)

            schema.addElement(pspNL)
            #  cesop.addChild()

        case _:
            #cesop Element
            cesop = xmlBuilder.XmlElement.XmlElement("CESOP")
            cesop.updateAttrib("version", globals.__cesopVersion__)

            cesop.updateAttrib("xmlns", f"urn:ec.europa.eu:taxud:fiscalis:cesop:v{globals.__xmlVersion__.split('.')[0]}")
            cesop.addChildren([buildLTMsgSpec(MessageTypeIndic, countryMS, quarter, year),
                               paymentDataBody])
            schema.addElement(cesop)

    #out
    fileName = f"PMT-{quarter}-{year}-{countryMS}-{pspId}-{partNumber}-{partTotal}.xml"
    filePath = Path(sys.argv[0]).parent.absolute().__str__()+"/out/"
    schema.toFile(fileName, filePath)