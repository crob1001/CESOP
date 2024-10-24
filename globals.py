__author__ = "Christian Roberts"

global __VERSION__
__VERSION__ = "0.8.0"

global __XML_VERSION__
__XML_VERSION__ = "1.0"

global __CESOP_VERSION__
__CESOP_VERSION__ = "4.02"

global __COMMON_TYPES_V__
__COMMON_TYPES_V__ = 1

global __FISCALIS_CESOP_V__
__FISCALIS_CESOP_V__ = 1

global __PSP_ID__
__PSP_ID__ = ""

global __SENDING_PSP_NAME__
__SENDING_PSP_NAME__ = ""

global __RSIN__
__RSIN__ = ""

global __KVK__ 
__KVK__ = ""

global __OPTIONALS__
__OPTIONALS__ = {
    "VATID" : False,
    "TAXID" : True
}

global __QUARTERS__ 
__QUARTERS__ = {
    "Q1": {"01-01", "03-31"},
    "Q2": {"04-01", "06-31"},
    "Q3": {"07-01", "09-31"},
    "Q4": {"10-01", "12-31"}
}

global __COUNTRIES__ 
__COUNTRIES__ = {
    "LT": "Lithuania",
    "PL": "Poland",
    "NL": "Netherlands"
    
}

global __MSG_TYPE_INDIC__
__MSG_TYPE_INDIC__ = {
    "CESOP100": "The message contains new data.",
    "CESOP101": "The message contains corrections or deletions of previously sent data.",
    "CESOP102": "The message indicates there is no data to report."
}

global __PSP_ID_TYPE__
__PSP_ID_TYPE__ = {
    "BIC": "The PSP Identifier is a BIC code.",
	"Other": "Other PSP Identifier type."
}

global __NAME_TYPES__
__NAME_TYPES__ = {
    "LEGAL"   : "Legal name",
    "BUSINESS": "Business name", 
	"TRADE"   : "Trade name",
	"PERSON"  : "Person name",
	"OTHER"   : "Other name" 
}

global __PAYER_MS_SOURCE__
__PAYER_MS_SOURCE__ = {
    "IBAN",
    "OBAN",
    "Other"
}