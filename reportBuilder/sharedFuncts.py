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

def docSpec(docTypeIndic):
    docTypeIndic = xmlElement.xmlElement("DocTypeIndic", "cm", docTypeIndic, True)
    docRefID = xmlElement.xmlElement("DocRefId", "cm", uuid4(), True)

    docSpec = xmlElement.xmlElement("DocSpec", "cesop")
    docSpec.addChildren([docTypeIndic, docRefID])
    return docSpec

def paymentMethod(paymentMethodType):
    paymentMethodType = xmlElement.xmlElement("PaymentMethodType", "cm", paymentMethodType, True)

    paymentMethod = xmlElement.xmlElement("PaymentMethod", "cesop", paymentMethodType)

    return paymentMethod

def reportedTransaction(transactionIdentifier, dateTime, isRefund, transactionDateType, amount, currency, paymentMethodType,
                             initiatedAtPhysicalPremisesOfMerchant, payerMS, payerMSSource, pspRole):
    
    transactionIdentifier = xmlElement.xmlElement("TransactionIdentifier", "cesop", transactionIdentifier, True)

    if ('z' == dateTime[-1]):
        dateTime = xmlElement.xmlElement("DateTime", "cesop", dateTime, True)
    else:
        dateTime = xmlElement.xmlElement("DateTime", "cesop", dateTime+'Z', True)
    
    dateTime.updateAttrib("transactionDateType", transactionDateType)

    amount = xmlElement.xmlElement("Amount", "cesop", amount, True)
    amount.updateAttrib("currency", currency)

    initiatedAtPhysicalPremisesOfMerchant = xmlElement.xmlElement("InitiatedAtPhysicalPremisesOfMerchant", "cesop", initiatedAtPhysicalPremisesOfMerchant.lower(), True)

    payerMS = xmlElement.xmlElement("PayerMS", "cesop", payerMS, True)
    if (payerMSSource not in globals.__PAYER_MS_SOURCE__): payerMSSource = "Other" 
    payerMS.updateAttrib("PayerMSSource", payerMSSource)

    # pspRoleType = xmlElement.xmlElement("PSPRoleType", pspRole, True)
    # pspRole = xmlElement.xmlElement("PSPRole", pspRoleType, False)
    
    reportedTransaction = xmlElement.xmlElement("ReportedTransaction", "cesop")
    reportedTransaction.updateAttrib("IsRefund", str(isRefund).lower())
    reportedTransaction.addChildren([transactionIdentifier, dateTime, amount, paymentMethod(paymentMethodType), initiatedAtPhysicalPremisesOfMerchant, payerMS, 
                                     #pspRole
                                     ])

    return reportedTransaction

def reportedPayee(df, countryMS):
    reportedPayee = xmlElement.xmlElement("ReportedPayee" ,"cesop")

    name = xmlElement.xmlElement("Name", "cesop", df.iat[-1,legend.__fieldOrder__.index("PayeeName")], True)
    name.updateAttrib("nameType", df.iat[-1,legend.__fieldOrder__.index("PayeeNameType")].upper())

    country = xmlElement.xmlElement("Country", "cesop", df.iat[-1,legend.__fieldOrder__.index("CountryCode")], True)

    taxIdentification = xmlElement.xmlElement("TAXIdentification", "cesop")

    match(countryMS):
        
        case "NL" :
            address = netherlands.NLAddress(df)
        
        case _ :
            address = default.address(df, countryMS)  

    if globals.__OPTIONALS__["VATID"]:
        VATId = xmlElement.xmlElement("VATId", "cesop", df.iat[0,legend.__fieldOrder__.index("VATId")],True)
        VATId.updateAttrib("issuedBy", df.iat[0,legend.__fieldOrder__.index("issuedByVAT")])
        VATId.addChild(df.iat[-1,legend.__fieldOrder__.index("VATId")])
        taxIdentification.addChild(VATId)

    if globals.__OPTIONALS__["TAXID"]:
        TAXId = xmlElement.xmlElement("TAXId", None, df.iat[-1,legend.__fieldOrder__.index("TAXId")], True)
        TAXId.updateAttrib("issuedBy", df.iat[-1,legend.__fieldOrder__.index("issuedByTAX")])
        TAXId.updateAttrib("type", df.iat[-1,legend.__fieldOrder__.index("typeTAX")])
        taxIdentification.addChild(TAXId)

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
            accountIdentifier = xmlElement.xmlElement("AccountIdentifier", "cesop", df.iat[i,legend.__fieldOrder__.index("AccountIdentifier")], True)
            accountIdentifier.updateAttrib("CountryCode", df.iat[i,legend.__fieldOrder__.index("CountryCode")])
            accountIdentifier.updateAttrib("type", df.iat[i,legend.__fieldOrder__.index("typeAccount")])
            reportedPayee.addChild(accountIdentifier)

        i += 1

    i = 0

    while i < len(df.index):
        reportedPayee.addChild(reportedTransaction(df.iat[i,legend.__fieldOrder__.index("TransactionIdentifier")], df.iat[i,legend.__fieldOrder__.index("DateTime")],
                                                        df.iat[i,legend.__fieldOrder__.index("IsRefund")], df.iat[i,legend.__fieldOrder__.index("transactionDateType")],
                                                        '{:.2f}'.format(df.iat[i,legend.__fieldOrder__.index("Amount")]), df.iat[i,legend.__fieldOrder__.index("currency")],
                                                        df.iat[i,legend.__fieldOrder__.index("PaymentMethodType")], str(df.iat[i,legend.__fieldOrder__.index("InitiatedAtPhysicalPremisesOfMerchant")]).lower(),
                                                        df.iat[i,legend.__fieldOrder__.index("PayerMS")], df.iat[i,legend.__fieldOrder__.index("PayerMSSource")],
                                                        df.iat[i,legend.__fieldOrder__.index("PSPRoleType")]))
        i += 1

    reportedPayee.addChild(docSpec(df.iat[-1,legend.__fieldOrder__.index("DocTypeIndic")]))

    return reportedPayee

def reportingPSP(pspId, pspIdType, name, nameType):
    reportingPSP = xmlElement.xmlElement("ReportingPSP", "cesop")

    pspId = xmlElement.xmlElement("PSPId", "cesop", pspId, True)
    pspId.updateAttrib("PSPIdType", pspIdType)

    name = xmlElement.xmlElement("Name", "cesop", name, True)
    name.updateAttrib("nameType", nameType)

    reportingPSP.addChildren([pspId, name])

    return reportingPSP

def paymentDataBody(pspId, pspIdType, name, nameType, fileList, countryMS):
    paymentDataBody = xmlElement.xmlElement("PaymentDataBody", "cesop")

    paymentDataBody.addChild(reportingPSP(pspId, pspIdType, name, nameType))

    for i in fileList:
        with open(i, 'rb') as f:
            file = pd.read_excel(f).fillna('')

        dfs = file.groupby(['PayeeName', 'CountryCode'])

        for countryCode, payeeName in dfs:
            paymentDataBody.addChild(reportedPayee(dfs.get_group(countryCode), countryMS))
            # paymentDataBody.addChild('')

    return paymentDataBody

def msgSpec(messageTypeIndic, transmittingCountry, quarter, year):
    transmitingCountry = xmlElement.xmlElement("TransmittingCountry", "cesop", transmittingCountry, True)

    msgType = xmlElement.xmlElement("MessageType", "cesop", "PMT", True)

    messageTypeIndic = xmlElement.xmlElement("MessageTypeIndic", "cesop", messageTypeIndic, True)

    MessageRefId = xmlElement.xmlElement("MessageRefId", "cesop", uuid4(), True)

    ReportingPeriod = xmlElement.xmlElement("ReportingPeriod", "cesop")
    ReportingPeriod.addChildren([xmlElement.xmlElement("Quarter", "cesop", list(globals.__QUARTERS__.keys()).index(quarter) + 1, True),
                                 xmlElement.xmlElement("Year", "cesop", year, True)])
    
    Timestamp = xmlElement.xmlElement("Timestamp", "cesop", datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ'), True)

    msgSpec = xmlElement.xmlElement("MessageSpec", "cesop")
    msgSpec.addChildren([transmitingCountry, msgType, messageTypeIndic, MessageRefId, ReportingPeriod,
                         Timestamp])

    return msgSpec