import pandas as pd
from uuid import uuid4
from datetime import datetime

import legend
import globals
from xmlBuilder import XmlElement

__author__ = "Christian Roberts"

def buildReportingPSP(pspId, pspIdType, name, nameType):
    reportingPSP = XmlElement.XmlElement("ReportingPSP")

    pspId = XmlElement.XmlElement("PSPId", pspId, True)
    pspId.updateAttrib("PSPIdType", pspIdType)

    name = XmlElement.XmlElement("Name", name, True)
    name.updateAttrib("NameType", nameType)

    reportingPSP.addChildren([pspId, name])

    return reportingPSP

def buildPaymentMethod(paymentMethodType):

    paymentMethodType = XmlElement.XmlElement("PaymentMethodType", paymentMethodType, True)

    paymentMethod = XmlElement.XmlElement("PaymentMethod", paymentMethodType, True)

    return paymentMethod

def buildReportedTransaction(transactionIdentifier, dateTime, isRefund, transactionDateType, amount, currency, paymentMethodType,
                             initiatedAtPhysicalPremisesOfMerchant, payerMS, payerMSSource, pspRole):
    reportedTransaction = XmlElement.XmlElement("ReportedTransaction", None, True)

    reportedTransaction.updateAttrib("IsRefund", isRefund)
    
    transactionIdentifier = XmlElement.XmlElement("TransactionIdentifier", transactionIdentifier, True)

    dateTime = XmlElement.XmlElement("DateTime", dateTime, True)
    dateTime.updateAttrib("TransactionDateType", transactionDateType)

    amount = XmlElement.XmlElement("Amount", amount, True)
    amount.updateAttrib("Currency", currency)

    paymentMethod = buildPaymentMethod(paymentMethodType)

    initiatedAtPhysicalPremisesOfMerchant = XmlElement.XmlElement("InitiatedAtPhysicalPremisesOfMerchant", initiatedAtPhysicalPremisesOfMerchant, True)

    payerMS = XmlElement.XmlElement("PayerMS", payerMS, True)
    payerMS.updateAttrib("PayerMSSource", payerMSSource)

    pspRoleType = XmlElement.XmlElement("PSPRoleType", pspRole, True)
    pspRole = XmlElement.XmlElement("PSPRole", pspRoleType, False)
    
    reportedTransaction.addChildren([transactionIdentifier, dateTime, amount, paymentMethod, initiatedAtPhysicalPremisesOfMerchant,
                                     payerMS, pspRole])

    return reportedTransaction

def buildRepresentative(representativeId, pspIdType, name, nameType):
    representative = XmlElement.XmlElement("Representative")

    representativeId = XmlElement.XmlElement("RepresentativeId", representativeId, True)
    representativeId.updateAttrib("PSPIdType", pspIdType)

    name = XmlElement.XmlElement("Name", name, True)
    name.updateAttrib("NameType", nameType)

    representative.addChildren([representativeId, name])

    return representative

def buildDocSpec(docTypeIndic):
    docSpec = XmlElement.XmlElement("DocSpec")
    docTypeIndic = XmlElement.XmlElement("DocTypeIndic", docTypeIndic, True)
    docRefID = XmlElement.XmlElement("DocRefID", uuid4(), True)
    docSpec.addChildren([docTypeIndic, docRefID])
    return docSpec

def buildPaymentDataBody(pspId, pspIdType, name, nameType, fileList, countryMS):
    paymentDataBody = XmlElement.XmlElement("PaymentDataBody")

    paymentDataBody.addChild(buildReportingPSP(pspId, pspIdType, name, nameType))

    for i in fileList:
        with open(i, 'rb') as f:
            file = pd.read_excel(f).fillna('')

        dfs = file.groupby(['PayeeName', 'CountryCode'])

        for countryCode, payeeName in dfs:
            group = dfs.get_group(countryCode)
            paymentDataBody.addChild(buildReportedPayee(group, countryMS))

    return paymentDataBody

def buildReportedPayee(df, countryMS):
    reportedPayee = XmlElement.XmlElement("ReportedPayee")

    name = XmlElement.XmlElement("Name", df.iat[0,legend.__fieldOrder__.index("PayeeName")], True)
    name.updateAttrib("NameType", df.iat[0,legend.__fieldOrder__.index("PayeeNameType")])

    country = XmlElement.XmlElement("Country", df.iat[0,legend.__fieldOrder__.index("CountryCode")], True)

    address = XmlElement.XmlElement("Address", None, True)

    match(countryMS):
        
        case "NL" :
            address.setInline(False)
            address.updateAttrib("LegalAddressType", df.iat[0,legend.__fieldOrder__.index("legalAddressType")].replace(' ',''))

            countryCode = XmlElement.XmlElement("cm:CountryCode", countryMS, True)
            addressFix = XmlElement.XmlElement("cm:AddressFix", None, False)

            street = XmlElement.XmlElement("cm:Street", df.iat[0,legend.__fieldOrder__.index("Street")], True)
            postCode = XmlElement.XmlElement("cm:PostCode", df.iat[0,legend.__fieldOrder__.index("PostCode")], True)
            city = XmlElement.XmlElement("cm:City", df.iat[0,legend.__fieldOrder__.index("City")], True)
            countrySubentity = XmlElement.XmlElement("cm:CountrySubentity", df.iat[0,legend.__fieldOrder__.index("CountrySubentity")], True)

            addressFix.addChildren([street, postCode, city, countrySubentity])

            address.addChildren([countryCode, addressFix])
        
        case _ :
            address.updateAttrib("LegalAddressType", df.iat[0,legend.__fieldOrder__.index("legalAddressType")].replace(' ',''))
            address.addChild(" ".join(f'{df.iat[0,legend.__fieldOrder__.index("Street")]} {df.iat[0,legend.__fieldOrder__.index("BuildingIdentifier")]} {df.iat[0,legend.__fieldOrder__.index("SuiteIdentifier")]} {df.iat[0,legend.__fieldOrder__.index("FloorIdentifier")]} {df.iat[0,legend.__fieldOrder__.index("DistrictName")]} {df.iat[0,legend.__fieldOrder__.index("POB")]} {df.iat[0,legend.__fieldOrder__.index("PostCode")]} {df.iat[0,legend.__fieldOrder__.index("City")]} {df.iat[0,legend.__fieldOrder__.index("CountrySubentity")]}'.split()))
    

    taxIdentification = XmlElement.XmlElement("TAXIdentification", None, False)

    VATId = XmlElement.XmlElement("VATId", df.iat[0,legend.__fieldOrder__.index("VATId")],True)
    VATId.updateAttrib("issuedBy", df.iat[0,19])

    TAXId = XmlElement.XmlElement("TAXId", df.iat[0,legend.__fieldOrder__.index("TAXId")], True)
    TAXId.updateAttrib("issuedBy", df.iat[0,legend.__fieldOrder__.index("issuedByTAX")])
    TAXId.updateAttrib("type", df.iat[0,legend.__fieldOrder__.index("typeTAX")])

    reportedPayee.addChildren([name, country, address#, emailAddress, webPage
                               ,taxIdentification])

    i = 0

    accountIdentifiers = []
    
    while i < len(df.index):
        exists = False
        for j in accountIdentifiers:
            if j == df.iat[i,legend.__fieldOrder__.index("AccountIdentifier")]:
                exists = True
        if exists == False:
            accountIdentifiers.append(df.iat[i,legend.__fieldOrder__.index("AccountIdentifier")])
            accountIdentifier = XmlElement.XmlElement("AccountIdentifier", df.iat[i,legend.__fieldOrder__.index("AccountIdentifier")], True)
            accountIdentifier.updateAttrib("CountryCode", df.iat[i,legend.__fieldOrder__.index("CountryCode")])
            accountIdentifier.updateAttrib("Type", df.iat[i,legend.__fieldOrder__.index("typeAccount")])
            reportedPayee.addChild(accountIdentifier)
        i+=1

    i = 0

    while i < len(df.index):
        reportedPayee.addChild(buildReportedTransaction(df.iat[i,legend.__fieldOrder__.index("TransactionIdentifier")], df.iat[i,legend.__fieldOrder__.index("DateTime")],
                                                        df.iat[i,legend.__fieldOrder__.index("IsRefund")], df.iat[i,legend.__fieldOrder__.index("transactionDateType")],
                                                        df.iat[i,legend.__fieldOrder__.index("Amount")], df.iat[i,legend.__fieldOrder__.index("currency")],
                                                        df.iat[i,legend.__fieldOrder__.index("PaymentMethodType")], df.iat[i,legend.__fieldOrder__.index("InitiatedAtPhysicalPremisesOfMerchant")],
                                                        df.iat[i,legend.__fieldOrder__.index("PayerMS")], df.iat[i,legend.__fieldOrder__.index("PayerMSSource")],
                                                        df.iat[i,legend.__fieldOrder__.index("PSPRoleType")]))
        i+=1


    reportedPayee.addChild(buildDocSpec(df.iat[0,legend.__fieldOrder__.index("DocTypeIndic")]))

    reportedPayee.addChild('')

    return reportedPayee

def buildMsgSpec(messageTypeIndic, transmittingCountry, quarter, year):
    msgSpec = XmlElement.XmlElement("MessageSpec")

    transmitingCountry = XmlElement.XmlElement("TransmittingCountry", transmittingCountry, True)
    msgType = XmlElement.XmlElement("MessageType", "PMT", True)
    messageTypeIndic = XmlElement.XmlElement("MessageTypeIndic", messageTypeIndic, True)
    MessageRefId = XmlElement.XmlElement("MessageRefId", uuid4(), True)
    ReportingPeriod = XmlElement.XmlElement("ReportingPeriod")
    ReportingPeriod.addChildren([XmlElement.XmlElement("Quarter", quarter, True),
                                 XmlElement.XmlElement("Year", year, True)])
    Timestamp = XmlElement.XmlElement("Timestamp", datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ'), True)

    msgSpec.addChildren([transmitingCountry, msgType, messageTypeIndic, MessageRefId, ReportingPeriod,
                         Timestamp])

    return msgSpec

def build(MessageTypeIndic, countryMS, quarter, year, paymentDataBody):
    cesop = XmlElement.XmlElement("CESOP")
    cesop.updateAttrib("version", globals.__cesopVersion__)

    cesop.updateAttrib("xmlns", f"urn:ec.europa.eu:taxud:fiscalis:cesop:v{globals.__xmlVersion__.split('.')[0]}")
    cesop.addChildren([buildMsgSpec(MessageTypeIndic, countryMS, quarter, year),
                        paymentDataBody])
    
    return cesop
