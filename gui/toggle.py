import globals

__author__ = "Christian Roberts"

def toggleVat():
        globals.__OPTIONAL__["VATID"] = not globals.__OPTIONAL__["VATID"]

def toggleTax():
        globals.__OPTIONAL__["TAXID"] = not globals.__OPTIONAL__["TAXID"]

def toggleAddressFix():
        globals.__OPTIONAL__["ADDRESS_FIX"] = not globals.__OPTIONAL__["ADDRESS_FIX"]

def toggleAddressFree():
        globals.__OPTIONAL__["ADDRESS_FREE"] = not globals.__OPTIONAL__["ADDRESS_FREE"]