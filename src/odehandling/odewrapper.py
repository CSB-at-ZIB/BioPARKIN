import logging
import libsbml
from backend.ast_converter import AstConverter
from backend_parkincpp.parkincpp_ast_converter_template import BioParkinCppAstConverterTemplate
from odehandling import helpers


class ODEWrapper(object):
    """
    This is a simple description of an ODE.

    If the ODE is based on a libSBML Rule, the Rule
    is wrapped. An ODE can also result out of the Reactions
    between Species, in which case there is no explicit
    Rule to wrap.

    The ODE is wrapped to be used by a computation backend.


    @param index: A unique index for every ODE has to be provided.
    @type index: int

    @param mathNode: A libSBML ASTNode root node
    @type mathNode: ASTNode

    @param formula: A math string in FORTRAN syntax
    @type formula: str

    @param rule: A libSBML rule object
    @type rule: libSBML rule (AssignmentRule, RateRule, ...)

    @since: 2010-04-21
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, index, mathNode=None, formula=None, rule=None, id=None, mainModel=None, speciesEntity=None):
        """
        Each ODE has an index and a mathematic formula
        (right-hand side) given as infix-notated string.
        """
        if not mathNode and not formula:
            logging.error(
                "Trying to create a wrapper ODE with neither formula string nor libSBML mathNodeNode object. ID: %s" % id)
            self.hasError = True
            return

        self.index = index
        self.mathNode = mathNode    # libSBML ASTNode root node
        self.formula = formula  # is used if given
        self.rule = rule  # this ODE may wrap a libSBML Rule
        self.mainModel = mainModel  # to get to function definitions contained in the model
        self.speciesEntity = speciesEntity

        self.id = None
        if id:
            self.id = id
        elif rule:
            self.id = rule.getId()
        else:
            self.id = "No ID"

        self.target = None
        if self.rule and self.mainModel:
            self.target = self._assignTarget()
            if type(self.target) == libsbml.Species:
                self.speciesEntity = self.target

        self.hasError = False

    def _assignTarget(self):
        """
        Tries to find the target Species (or Parameter, ...) given the current self.rule.getVariable()
        """
        if not self.rule or not self.mainModel:
            return

        try:
            return self._findSbmlEntity(self.rule.Item.getVariable(), self.mainModel)
        except Exception, e:
            logging.debug("OdeWrapper: Problems while trying to find target of rule %s.\Error:%s" % (self.rule.getId(), e))

    def mathForFortran(self):
        """
        DEPRECATED! The FORTRAN backend is no longer... :)

        Takes the current libSBML mathNode AST tree and converts it into
        something that is valid FORTRAN code. (e.g. "pow(x,2)" becomes
        "x ** 2", etc.)

        If "formula" was given during creation of this instance it is assumed
        that this formula string already is valid FORTRAN code. It will
        be returned unaltered.
        """
        if self.formula:
            return self.formula

        # else: get string from self.mathNode (libSBML ASTNode graph)

        odeString = helpers.handleMathNode(self.mathNode)
        return odeString

    def mathForBioParkinCpp(self, idsToReplace=None):
        """
        Creates and uses an AstConverter (with the BioParkinCppAstConverterTemplate) to
        convert the libsbml ASTNode into an PARKINcpp Expression object.
        """
        astConverter = AstConverter(BioParkinCppAstConverterTemplate(), mainModel=self.mainModel, idsToReplace=idsToReplace)
        return astConverter.handle(self.mathNode)


    def replaceIDs(self, odeString):
        """
        Takes the original mathematic string and replaces all Reaction IDs
        with an altered ID. This is needed so that Reactions and Parameters
        can't have the same variable name in the FORTRAN code.
        """
        reactionIDs = []

        for reactionWrapper in self.mainModel.SbmlReactions:
            reaction = reactionWrapper[0].Item
            id = reaction.getId()
            reactionIDs.append(id)

        # we start with replacing the longest IDs first. should help
        # to minimize problems with IDs that are substrings of longer IDs
        # Note: The problem still persists, it's not gone entirely. (Because
        # the replacement also contains the original ID and can still overlap
        # with other IDs.)
        reactionIDs = sorted(reactionIDs, key=len, reverse=True)

        for id in reactionIDs:
            if id in odeString:
                odeString = odeString.replace(id, "r_%s" % id)

        return odeString

    def isValid(self):
        """
        @returns: True, if the wrapped ODE (generated or given by a rule)
        is a valid ODE for simulation. For example, if the ODE's Species is constant, it won't be included
        in simulation.
        """
        if self.hasError:
            return False

        if self.id.startswith("helper"):
            return False

        if self.speciesEntity:
            species = self.speciesEntity.Item
            if not type(species) == libsbml.Species:    # if the speciesEntity is no Species, something's wrong :)
                logging.debug("OdeWrapper.isValid(): self.speciesEntity holds no Species but a: %s" % type(species))
                return False

            isConstant = species.getConstant()
            isBoundaryCondition = species.getBoundaryCondition()
            if isConstant and isBoundaryCondition: # Species quantity never changes
                return False
            if not isConstant and isBoundaryCondition: # Species quantity only changed by Rules and Events
                return False
            if isConstant and not isBoundaryCondition: # Species quantity never changes
                return False
            if not isConstant and not isBoundaryCondition: # Species Quantity changed by Reactions *or* Rules, and Events
                return True

        return True


    def getId(self):
        return self.id


    def getName(self):
        entity = self._findSbmlEntity(self.id, self.mainModel)
        
        if entity:
            return entity.Item.getName()
        else:
            return "noname"



    def _findSbmlEntity(self, id, sbmlMainModel):
        """
        Tries to find a SBML entity given a SBMLMainModel
        and an ID.

        @param id: ID to search for
        @type id: str

        @param sbmlMainModel: A BioParkin SBMLMainModel
        @type sbmlMainModel: SBMLMainModel

        @since: 2010-06-07
        """

        entityTypes = [sbmlMainModel.SbmlSpecies,
                       sbmlMainModel.SbmlCompartments,
                       sbmlMainModel.SbmlParameters]

        for type in entityTypes:
            if not type:
                continue
            for entity in type:
                try:
                    if id == entity.getId():
                        return entity
                except:
                    logging.debug("sbmlhelpers: Can't get SBMLEntity with ID %s." % id)

        return None
