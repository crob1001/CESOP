__author__ = "Christian Roberts"

global __version__
__version__ = "0.6.5"

global __xmlVersion__
__xmlVersion__ = "1.0"

global __cesopVersion__
__cesopVersion__ = "4.02"

global __COMMON_TYPES_V__
__COMMON_TYPES_V__ = 1

global __FISCALIS_CESOP_V__
__FISCALIS_CESOP_V__ = 1

global __pspID__
__pspID__ = ""

global __sendingPSPName__
__sendingPSPName__ = ""

global __RSIN__
__RSIN__ = ""

global __KVK__ 
__KVK__ = ""

global __quarters__ 
__quarters__ = {
    "Q1": {"01-01", "03-31"},
    "Q2": {"04-01", "06-31"},
    "Q3": {"07-01", "09-31"},
    "Q4": {"10-01", "12-31"}
}

global __countries__ 
__countries__ = {
    "LT": "Lithuania",
    "PL": "Poland",
    "NL": "Netherlands"
    
}

global __msgTypeIndic__
__msgTypeIndic__ = {
    "CESOP100": "The message contains new data.",
    "CESOP101": "The message contains corrections or deletions of previously sent data.",
    "CESOP102": "The message indicates there is no data to report."
}

global __pspIDType__
__pspIDType__ = {
    "BIC": "The PSP Identifier is a BIC code.",
	"Other": "Other PSP Identifier type."
}

global __NameTypes__
__NameTypes__ = {
    "LEGAL"   : "Legal name",
    "BUSINESS": "Business name", 
	"TRADE"   : "Trade name",
	"PERSON"  : "Person name",
	"OTHER"   : "Other name" 
}