__author__ = "Moritz Wade"
__contact__ = "wade@zib.de"
__copyright__ = "Zuse Institute Berlin 2010"

def stringToBool(theString):
    if type(theString) == str:
        return theString[0].upper()=="T"
    elif type(theString) == bool:
        return theString
    else:
        return