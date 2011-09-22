"""
The purpose of this file is to provide some CONSTANTs and pseudo-ENUMs
to be used within model classes.

@since: 2011-05-30
"""

from basics.helpers.enum import enum

__author__ = "Moritz Wade"
__contact__ = "wade@zib.de"
__copyright__ = "Zuse Institute Berlin 2011"




CHANGETYPE = enum("CHANGETYPE", "ADD, REMOVE, CHANGE_REACTANTS, CHANGE_PRODUCTS, CHANGE_MODIFIERS")

#### defining constant strings for Parameter Set XML ####
XML_NAMESPACE_PARAMETER_SETS = "http://sys-bio.org/ParameterSets"

XML_LIST_OF_PARAMETER_SETS = "listOfParameterSets"
XML_LIST_OF_PARAMETER_SETS_ACTIVE = "active"

XML_PARAMETER_SET = "parameterSet"
XML_PARAMETER_SET_ID = "id"
XML_PARAMETER_SET_NAME = "name"

XML_PARAMETER = "parameter"
XML_PARAMETER_SBML_ID = "sbmlId"
XML_PARAMETER_VALUE = "value"
XML_PARAMETER_REACTION_ID = "reaction"

PARAM_SET_INITIAL_GUESS = "Initial Guess"
PARAM_SET_ORIGINAL = "Original"
PARAM_SET_FIT = "Fit"