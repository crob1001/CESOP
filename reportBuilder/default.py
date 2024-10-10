import pandas as pd
from uuid import uuid4
from datetime import datetime

import legend
from xmlSchema import xmlElement

__author__ = "Christian Roberts"

def buildReportingPSP(pspId, pspIdType, name, nameType):
    reportingPSP = xmlElement.xmlElement("ReportingPSP")

    pspId = xmlElement.xmlElement("PSPId", pspId, True)
    pspId.updateAttrib("PSPIdType", pspIdType)

    name = xmlElement.xmlElement("Name", name, True)
    name.updateAttrib("NameType", nameType)

    reportingPSP.addChildren([pspId, name])

    return reportingPSP

def buildPaymentMethod(paymentMethodType):

    paymentMethodType = xmlElement.xmlElement("PaymentMethodType", paymentMethodType, True)

    paymentMethod = xmlElement.xmlElement("PaymentMethod", paymentMethodType, True)

    return paymentMethod

def buildReportedTransaction(transactionIdentifier, dateTime, isRefund, transactionDateType, amount, currency, paymentMethodType,
                             initiatedAtPhysicalPremisesOfMerchant, payerMS, payerMSSource, pspRole):
    reportedTransaction = xmlElement.xmlElement("ReportedTransaction", None, True)

    reportedTransaction.updateAttrib("IsRefund", isRefund)
    
    transactionIdentifier = xmlElement.xmlElement("TransactionIdentifier", transactionIdentifier, True)

    dateTime = xmlElement.xmlElement("DateTime", dateTime, True)
    dateTime.updateAttrib("TransactionDateType", transactionDateType)

    amount = xmlElement.xmlElement("Amount", amount, True)
    amount.updateAttrib("Currency", currency)

    paymentMethod = buildPaymentMethod(paymentMethodType)

    initiatedAtPhysicalPremisesOfMerchant = xmlElement.xmlElement("InitiatedAtPhysicalPremisesOfMerchant", initiatedAtPhysicalPremisesOfMerchant, True)

    payerMS = xmlElement.xmlElement("PayerMS", payerMS, True)
    payerMS.updateAttrib("PayerMSSource", payerMSSource)

    pspRoleType = xmlElement.xmlElement("PSPRoleType", pspRole, True)
    pspRole = xmlElement.xmlElement("PSPRole", pspRoleType, False)
    
    reportedTransaction.addChildren([transactionIdentifier, dateTime, amount, paymentMethod, initiatedAtPhysicalPremisesOfMerchant,
                                     payerMS, pspRole])

    return reportedTransaction

def buildRepresentative(representativeId, pspIdType, name, nameType):
    representative = xmlElement.xmlElement("Representative")

    representativeId = xmlElement.xmlElement("RepresentativeId", representativeId, True)
    representativeId.updateAttrib("PSPIdType", pspIdType)

    name = xmlElement.xmlElement("Name", name, True)
    name.updateAttrib("NameType", nameType)

    representative.addChildren([representativeId, name])

    return representative

def buildDocSpec(docTypeIndic):
    docSpec = xmlElement.xmlElement("DocSpec")
    docTypeIndic = xmlElement.xmlElement("DocTypeIndic", docTypeIndic, True)
    docRefID = xmlElement.xmlElement("DocRefID", uuid4(), True)
    docSpec.addChildren([docTypeIndic, docRefID])
    return docSpec

def buildPaymentDataBody(pspId, pspIdType, name, nameType, fileList, countryMS):
    paymentDataBody = xmlElement.xmlElement("PaymentDataBody")

    paymentDataBody.addChild(buildReportingPSP(pspId, pspIdType, name, nameType))

    for i in fileList:
        with open(i, 'rb') as f:
            file = pd.read_excel(f).fillna('')

        dfs = file.groupby(['PayeeName', 'CountryCode'])

        for countryCode, payeeName in dfs:
            paymentDataBody.addChild(buildReportedPayee(dfs.get_group(countryCode), countryMS))
            paymentDataBody.addChild('')

    return paymentDataBody

def buildReportedPayee(df, countryMS):
    reportedPayee = xmlElement.xmlElement("ReportedPayee")

    name = xmlElement.xmlElement("Name", df.iat[0,legend.__fieldOrder__.index("PayeeName")], True)
    name.updateAttrib("NameType", df.iat[0,legend.__fieldOrder__.index("PayeeNameType")])

    country = xmlElement.xmlElement("Country", df.iat[0,legend.__fieldOrder__.index("CountryCode")], True)

    address = xmlElement.xmlElement("Address", None, True)

    match(countryMS):
        
        case "NL" :
            address.setInline(False)
            address.updateAttrib("LegalAddressType", df.iat[0,legend.__fieldOrder__.index("legalAddressType")].replace(' ',''))

            countryCode = xmlElement.xmlElement("cm:CountryCode", countryMS, True)
            addressFix = xmlElement.xmlElement("cm:AddressFix", None, False)

            street = xmlElement.xmlElement("cm:Street", df.iat[0,legend.__fieldOrder__.index("Street")], True)
            postCode = xmlElement.xmlElement("cm:PostCode", df.iat[0,legend.__fieldOrder__.index("PostCode")], True)
            city = xmlElement.xmlElement("cm:City", df.iat[0,legend.__fieldOrder__.index("City")], True)
            countrySubentity = xmlElement.xmlElement("cm:CountrySubentity", df.iat[0,legend.__fieldOrder__.index("CountrySubentity")], True)

            addressFix.addChildren([street, postCode, city, countrySubentity])

            address.addChildren([countryCode, addressFix])
        
        case _ :
            address.updateAttrib("LegalAddressType", df.iat[0,legend.__fieldOrder__.index("legalAddressType")].replace(' ',''))
            address.addChild(" ".join(f'{df.iat[0,legend.__fieldOrder__.index("Street")]} {df.iat[0,legend.__fieldOrder__.index("BuildingIdentifier")]} {df.iat[0,legend.__fieldOrder__.index("SuiteIdentifier")]} {df.iat[0,legend.__fieldOrder__.index("FloorIdentifier")]} {df.iat[0,legend.__fieldOrder__.index("DistrictName")]} {df.iat[0,legend.__fieldOrder__.index("POB")]} {df.iat[0,legend.__fieldOrder__.index("PostCode")]} {df.iat[0,legend.__fieldOrder__.index("City")]} {df.iat[0,legend.__fieldOrder__.index("CountrySubentity")]}'.split()))
    

    taxIdentification = xmlElement.xmlElement("TAXIdentification", None, False)

    VATId = xmlElement.xmlElement("VATId", df.iat[0,legend.__fieldOrder__.index("VATId")],True)
    VATId.updateAttrib("issuedBy", df.iat[0,19])

    TAXId = xmlElement.xmlElement("TAXId", df.iat[0,legend.__fieldOrder__.index("TAXId")], True)
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
            accountIdentifier = xmlElement.xmlElement("AccountIdentifier", df.iat[i,legend.__fieldOrder__.index("AccountIdentifier")], True)
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

    return reportedPayee

def buildMsgSpec(messageTypeIndic, transmittingCountry, quarter, year):
    msgSpec = xmlElement.xmlElement("MessageSpec")

    transmitingCountry = xmlElement.xmlElement("TransmittingCountry", transmittingCountry, True)
    msgType = xmlElement.xmlElement("MessageType", "PMT", True)
    messageTypeIndic = xmlElement.xmlElement("messageTypeIndic", messageTypeIndic, True)
    MessageRefId = xmlElement.xmlElement("MessageRefId", uuid4(), True)
    ReportingPeriod = xmlElement.xmlElement("ReportingPeriod")
    ReportingPeriod.addChildren([xmlElement.xmlElement("Quarter", quarter, True),
                                 xmlElement.xmlElement("Year", year, True)])
    Timestamp = xmlElement.xmlElement("Timestamp", datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ'), True)

    msgSpec.addChildren([transmitingCountry, msgType, messageTypeIndic, MessageRefId, ReportingPeriod,
                         Timestamp])

    return msgSpec

def build(cesop, messageTypeIndic, countryMS, quarter, year, paymentDataBody):

    cesop.addChildren([buildMsgSpec(messageTypeIndic, countryMS, quarter, year),
                        paymentDataBody])
    
    return cesop
