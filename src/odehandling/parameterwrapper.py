'''
Created on Apr 21, 2010

@author: bzfwadem
'''
import logging
import libsbml

class ParameterWrapper(object):
    '''
    Simple wrapper for a libSBML Parameter. It enables easy use
    in computation backends.
    
    @param parameter: A libSBML parameter object
    @type parameter: libSBML Parameter
    
    @since: 2010-04-21
    '''
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, parameter, index):
        '''
        Just gets some infos from the given libSBML
        parameter object.
        '''
        if parameter is None:
            error = "Tried to create a wrapper Parameter object without supplying a libSBML Parameter."
            logging.error(error)
            return

        self.wrappedParameter = parameter
        self.wrappedEntity = parameter
        self.id = self.wrappedParameter.getId()
#        self.initialValue = self.getInitialValue()
        self.index = index
        self.paramProxy = None  # for supporting ParameterProxys of a ParameterSet

    def getScope(self):
        '''
        Returns the scope of the wrapped libSBML object iff it is
        a parameter. (Scope = global/local)
        
        @since: 2010-08-04
        
        @return: Scope of Parameter object
        @rtype: str
        '''
        if not type(self.wrappedParameter) == libsbml.Parameter:
            return
        
        parent = self.wrappedParameter.getParentSBMLObject() # parent= ListOfParameters
        if parent:
            grandpa = parent.getParentSBMLObject()
            if type(grandpa) == libsbml.Model:
                return "Global"
            elif type(grandpa) == libsbml.KineticLaw:
                reaction = grandpa.getParentSBMLObject()
                return "%s" % reaction.getId()
            
    def getCombinedId(self):
        scope = self.getScope()
        if scope == "Global":
            return self.id
        else:
            return "%s_%s" % (scope, self.id)

    def getId(self):
        return self.id
    
    
    def getInitialValue(self):
        '''
        @return: The initial value of the wrapped Parameter. Existing 
        AssignmentRules are taken into account.
        
        @since: 2010-08-16
        '''
        if self.paramProxy:
            return float(self.paramProxy.getValue())
        else:
            return float(self.wrappedParameter.getValue())
    
        # todo: take rules into account!

    def isConstant(self):
        return self.wrappedParameter.getConstant()