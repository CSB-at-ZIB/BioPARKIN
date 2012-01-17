
import logging
import libsbml
from backend.ast_converter import AstConverter
from backend_parkincpp.parkincpp_ast_converter_template import BioParkinCppAstConverterTemplate
from odehandling import helpers
from parkincpp.parkin import Expression

class ReactionWrapper(object):
    """
    Simple wrapper for a libSBML Reaction. It enables easy use
    in computation backends.

    @param reaction: A libSBML Reaction object
    @type reaction: libSBML Reaction

    @since: 2010-07-28
    """
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, reaction, index, mainModel=None):
        """
        Just gets some infos from the given libSBML
        Reaction object.
        """
        if reaction is None:
            error = "Tried to create a wrapper Reaction object without supplying a libSBML Reaction."
            logging.error(error)
            return

        self.mainModel = mainModel

        self.wrappedReaction = reaction
        self.id = self.wrappedReaction.getId()
        
        if self.wrappedReaction.isSetKineticLaw():
            self.kineticLaw = self.wrappedReaction.getKineticLaw()
        else:
            self.kineticLaw = None
            logging.info("Reaction %s has no kinetic law!" % self.id)
            
        self.index = index

        self.localParams = None
        self.localParameterIDs = self.getLocalParameters()

    def getId(self):
        return self.id
        
    def getLocalParameters(self):
        if self.kineticLaw:
            localParamIDs = []
            self.localParams = []
            numLocalParams = self.kineticLaw.getNumParameters()
            for i in xrange(numLocalParams):
                param = self.kineticLaw.getParameter(i)
                localParamIDs.append(param.getId())
                self.localParams.append(param)
            return localParamIDs
        
    def mathForFortran(self):
        """
        Takes the libSBML mathNode AST tree of this Reaction's
        KineticLaw and converts it into
        something that is valid FORTRAN code. (e.g. "pow(x,2)" becomes
        "x ** 2", etc.)

        """
        if not self.kineticLaw:
            return 
        
        validFortran = helpers.handleMathNode(self.kineticLaw.getMath())
        
        # we start with replacing the longest IDs first. should help
        # to minimize problems with IDs that are substrings of longer IDs
        # Note: The problem still persists, it's not gone entirely. (Because
        # the replacement also contains the original ID and can still overlap
        # with other IDs.)
        sortedLocalParamIDs = sorted(self.localParameterIDs, key=len, reverse=True)
        
        for localParam in sortedLocalParamIDs:
            if localParam in validFortran:
                validFortran = validFortran.replace(localParam, "%s_%s" % (self.id, localParam))
                
        return validFortran


    def mathForBioParkinCpp(self, idsToReplace=None):
        """
        Creates and uses an AstConverter (with the BioParkinCppAstConverterTemplate) to
        convert the libsbml ASTNode into an PARKINcpp Expression object.
        """
        if self.localParams:
            if not idsToReplace:
                idsToReplace = {}
            for param in self.localParams:
                idsToReplace[param.getId()] = Expression(self.getCombinedId(param))


        astConverter = AstConverter(BioParkinCppAstConverterTemplate(), mainModel=self.mainModel, idsToReplace=idsToReplace)
        return astConverter.handle(self.kineticLaw.getMath())


    def getScope(self, param):
        """
        Returns the scope of the wrapped libSBML object iff it is
        a parameter. (Scope = global/local)

        This is duplicate code. It originaly appears in the parameterwrapper.But, here we have to handle a
        non-wrapped Parameter, so this is a quick fix.

        @since: 2011-02-18

        @return: Scope of Parameter object
        @rtype: str
        """
        if not type(param) == libsbml.Parameter:
            return

        parent = param.getParentSBMLObject() # parent= ListOfParameters
        if parent:
            grandpa = parent.getParentSBMLObject()
            if type(grandpa) == libsbml.Model:
                return "Global"
            elif type(grandpa) == libsbml.KineticLaw:
                reaction = grandpa.getParentSBMLObject()
                return "%s" % reaction.getId()

    def getCombinedId(self, param):
        scope = self.getScope(param)
        if scope == "Global":
            return param.getId()
        else:
            return "%s_%s" % (scope, param.getId())