import pandas as pd
from uuid import uuid4
from datetime import datetime

import legend
import globals
from xmlSchema import xmlElement
from reportBuilder import default, netherlands

__author__ = "Christian Roberts"

def representative(representativeId, pspIdType, name, nameType):
    representative = xmlElement.xmlElement("Representative")

    representativeId = xmlElement.xmlElement("RepresentativeId", representativeId, True)
    representativeId.updateAttrib("PSPIdType", pspIdType)

    name = xmlElement.xmlElement("Name", name, True)
    name.updateAttrib("nameType", nameType)

    representative.addChildren([representativeId, name])

    return representative

def msgSpec(messageTypeIndic, transmittingCountry, quarter, year):
    msgSpec = xmlElement.xmlElement("MessageSpec")

    transmitingCountry = xmlElement.xmlElement("TransmittingCountry", transmittingCountry, True)
    msgType = xmlElement.xmlElement("MessageType", "PMT", True)
    messageTypeIndic = xmlElement.xmlElement("MessageTypeIndic", messageTypeIndic, True)
    MessageRefId = xmlElement.xmlElement("MessageRefId", uuid4(), True)
    ReportingPeriod = xmlElement.xmlElement("ReportingPeriod")

    ReportingPeriod.addChildren([xmlElement.xmlElement("Quarter", list(globals.__quarters__.keys()).index(quarter) + 1, True),
                                 xmlElement.xmlElement("Year", year, True)])
    
    Timestamp = xmlElement.xmlElement("Timestamp", datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ'), True)

    msgSpec.addChildren([transmitingCountry, msgType, messageTypeIndic, MessageRefId, ReportingPeriod,
                         Timestamp])

    return msgSpec

def docSpec(docTypeIndic):
    docSpec = xmlElement.xmlElement("DocSpec")
    docTypeIndic = xmlElement.xmlElement("DocTypeIndic", docTypeIndic, True)
    docRefID = xmlElement.xmlElement("DocRefID", uuid4(), True)
    docSpec.addChildren([docTypeIndic, docRefID])
    return docSpec

def paymentMethod(paymentMethodType):
    paymentMethodType = xmlElement.xmlElement("PaymentMethodType", paymentMethodType, True)

    paymentMethod = xmlElement.xmlElement("PaymentMethod", paymentMethodType, True)

    return paymentMethod

def reportedTransaction(transactionIdentifier, dateTime, isRefund, transactionDateType, amount, currency, paymentMethodType,
                             initiatedAtPhysicalPremisesOfMerchant, payerMS, payerMSSource, pspRole):
    reportedTransaction = xmlElement.xmlElement("ReportedTransaction", None, True)

    reportedTransaction.updateAttrib("IsRefund", isRefund)
    
    transactionIdentifier = xmlElement.xmlElement("TransactionIdentifier", transactionIdentifier, True)

    dateTime = xmlElement.xmlElement("DateTime", dateTime, True)
    dateTime.updateAttrib("TransactionDateType", transactionDateType)

    amount = xmlElement.xmlElement("Amount", amount, True)
    amount.updateAttrib("Currency", currency)

    initiatedAtPhysicalPremisesOfMerchant = xmlElement.xmlElement("InitiatedAtPhysicalPremisesOfMerchant", initiatedAtPhysicalPremisesOfMerchant, True)

    payerMS = xmlElement.xmlElement("PayerMS", payerMS, True)
    payerMS.updateAttrib("PayerMSSource", payerMSSource)

    pspRoleType = xmlElement.xmlElement("PSPRoleType", pspRole, True)
    pspRole = xmlElement.xmlElement("PSPRole", pspRoleType, False)
    
    reportedTransaction.addChildren([transactionIdentifier, dateTime, amount, paymentMethod(paymentMethodType), initiatedAtPhysicalPremisesOfMerchant,
                                     payerMS, pspRole])

    return reportedTransaction

def reportedPayee(df, countryMS):
    reportedPayee = xmlElement.xmlElement("ReportedPayee")

    name = xmlElement.xmlElement("Name", df.iat[-1,legend.__fieldOrder__.index("PayeeName")], True)
    name.updateAttrib("nameType", df.iat[-1,legend.__fieldOrder__.index("PayeeNameType")].upper())

    country = xmlElement.xmlElement("Country", df.iat[-1,legend.__fieldOrder__.index("CountryCode")], True)

    match(countryMS):
        
        case "NL" :
            address = netherlands.NLAddress(df)
        
        case _ :
            address = default.address(df)  

    taxIdentification = xmlElement.xmlElement("TAXIdentification", None, False)

    VATId = xmlElement.xmlElement("VATId", df.iat[-1,legend.__fieldOrder__.index("VATId")],True)
    VATId.updateAttrib("issuedBy", df.iat[-1,19])

    TAXId = xmlElement.xmlElement("TAXId", df.iat[-1,legend.__fieldOrder__.index("TAXId")], True)
    TAXId.updateAttrib("issuedBy", df.iat[-1,legend.__fieldOrder__.index("issuedByTAX")])
    TAXId.updateAttrib("type", df.iat[-1,legend.__fieldOrder__.index("typeTAX")])

    reportedPayee.addChildren([name, country, address#, emailAddress, webPage
                               ,taxIdentification])

    i = -1

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

        i += 1

    i = 0

    while i < len(df.index):
        reportedPayee.addChild(reportedTransaction(df.iat[i,legend.__fieldOrder__.index("TransactionIdentifier")], df.iat[i,legend.__fieldOrder__.index("DateTime")],
                                                        df.iat[i,legend.__fieldOrder__.index("IsRefund")], df.iat[i,legend.__fieldOrder__.index("transactionDateType")],
                                                        df.iat[i,legend.__fieldOrder__.index("Amount")], df.iat[i,legend.__fieldOrder__.index("currency")],
                                                        df.iat[i,legend.__fieldOrder__.index("PaymentMethodType")], df.iat[i,legend.__fieldOrder__.index("InitiatedAtPhysicalPremisesOfMerchant")],
                                                        df.iat[i,legend.__fieldOrder__.index("PayerMS")], df.iat[i,legend.__fieldOrder__.index("PayerMSSource")],
                                                        df.iat[i,legend.__fieldOrder__.index("PSPRoleType")]))
        i += 1

    reportedPayee.addChild(docSpec(df.iat[-1,legend.__fieldOrder__.index("DocTypeIndic")]))

    return reportedPayee

def reportingPSP(pspId, pspIdType, name, nameType):
    reportingPSP = xmlElement.xmlElement("ReportingPSP")

    pspId = xmlElement.xmlElement("PSPId", pspId, True)
    pspId.updateAttrib("PSPIdType", pspIdType)

    name = xmlElement.xmlElement("Name", name, True)
    name.updateAttrib("nameType", nameType)

    reportingPSP.addChildren([pspId, name])

    return reportingPSP

def paymentDataBody(pspId, pspIdType, name, nameType, fileList, countryMS):
    paymentDataBody = xmlElement.xmlElement("PaymentDataBody")

    paymentDataBody.addChild(reportingPSP(pspId, pspIdType, name, nameType))

    for i in fileList:
        with open(i, 'rb') as f:
            file = pd.read_excel(f).fillna('')

        dfs = file.groupby(['PayeeName', 'CountryCode'])

        for countryCode, payeeName in dfs:
            paymentDataBody.addChild(reportedPayee(dfs.get_group(countryCode), countryMS))
            paymentDataBody.addChild('')

    return paymentDataBody