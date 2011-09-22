from backend.ast_converter import AstConverter
from backend_parkincpp.parkincpp_ast_converter_template import BioParkinCppAstConverterTemplate
import basics.helpers

__author__ = 'bzfwadem'


class AssignmentRuleWrapper(object):
    '''
    This is a simple description of an Assignment Rule. It is wrapped to be used by a computation backend.




    @param index: A unique index for every AssignmentRule has to be provided.
    @type index: int

    @param mathNode: A libSBML ASTNode root node
    @type mathNode: ASTNode

    @param rule: A libSBML rule object
    @type rule: libSBML rule (AssignmentRule)

    @since: 2011-02-01
    '''

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, index, mathNode=None, rule=None, id=None, mainModel=None):
        '''
        Each AssignmentRule has an index.
        '''
        if not mathNode:
            logging.error("Trying to create a wrapper AssignmentRule with no libSBML mathNode object. ID: %s" % id)
            self.hasError = True
            return

        self.index = index
        self.mathNode = mathNode    # libSBML ASTNode root node
        self.rule = rule  # this original libSBML Rule
        self.mainModel = mainModel  # to get to function definitions contained in the model
        self.speciesEntity = None

        self.id = None
        if id:
            self.id = id
        elif rule:
            self.id = rule.getId()
        else:
            self.id = "No ID"

        self.hasError = False

    def getId(self):
        return self.id

    def mathForFortran(self):
        '''
        Takes the current libSBML mathNode AST tree and converts it into
        something that is valid FORTRAN code. (e.g. "pow(x,2)" becomes
        "x ** 2", etc.)
        '''
        odeString = helpers.handleMathNode(self.mathNode)
        return odeString

    def mathForBioParkinCpp(self, idsToReplace=None):
        '''
        Creates and uses an AstConverter (with the BioParkinCppAstConverterTemplate) to
        convert the libsbml ASTNode into an PARKINcpp Expression object.
        '''
        astConverter = AstConverter(BioParkinCppAstConverterTemplate(), mainModel=self.mainModel, idsToReplace=idsToReplace)
        return astConverter.handle(self.mathNode)

    def isValid(self):
        '''
        This is a place to do validity checks on an AssignmentRule whether its fit for being
        used in computations.
        '''
        return True # for now, it's always valid