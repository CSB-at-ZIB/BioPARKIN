import math
from backend.base_ast_converter_template import BaseAstConverterTemplate
from parkincpp.parkin import Expression
from parkincpp import parkin

class BioParkinCppAstConverterTemplate(BaseAstConverterTemplate):
    """
    Implements the BaseAstConverterTemplate and fills all the predefined methods with actual code
    to convert libsbml ASTNodes into PARKINcpp Expression objects.

    @param astConverter: The reference to the ASTConverter is needed so that recursive calls along
    the node tree are possible.
    @type astConverter: backend.ASTConverter

    @since: 2010-12-21
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, astConverter = None):
        self.astConverter = astConverter


    def handlePlus(self, node):
        return Expression(parkin.PLUS, self.astConverter.handle(node.getLeftChild()), self.astConverter.handle(node.getRightChild()))

    def handleTimes(self, node):
        left = self.astConverter.handle(node.getLeftChild())
        right = self.astConverter.handle(node.getRightChild())
        if right and left:
            return Expression(parkin.TIMES, left, right)
        else:
            return None

    def handleDivide(self, node):
        return Expression(parkin.DIVIDE, self.astConverter.handle(node.getLeftChild()), self.astConverter.handle(node.getRightChild()))

    def handleMinus(self, node):
        if node.getRightChild():
            return Expression(parkin.MINUS, self.astConverter.handle(node.getLeftChild()), self.astConverter.handle(node.getRightChild()))
        else:
            return Expression(parkin.MINUS, self.astConverter.handle(node.getLeftChild()))

    def handlePower(self, node):
        return Expression(parkin.POWER, self.astConverter.handle(node.getLeftChild()), self.astConverter.handle(node.getRightChild()))

    def handleLn(self, node):
        return Expression(parkin.LN, self.astConverter.handle(node.getLeftChild()))

    def handleLog(self, node):
        return Expression(parkin.LOG, self.astConverter.handle(node.getLeftChild()))

    def handleExp(self, node):
        return Expression(parkin.EXP, self.astConverter.handle(node.getLeftChild()))

    def handleAbs(self, node):
        return Expression(parkin.ABS, self.astConverter.handle(node.getLeftChild()))

    def handleCeiling(self, node):
        return Expression(parkin.CEIL, self.astConverter.handle(node.getLeftChild()))

    def handleFloor(self, node):
        return Expression(parkin.FLOOR, self.astConverter.handle(node.getLeftChild()))

    def handleSin(self, node):
        return Expression(parkin.SIN, self.astConverter.handle(node.getLeftChild()))

    def handleCos(self, node):
        return Expression(parkin.COS, self.astConverter.handle(node.getLeftChild()))


    def handleInt(self, node):
        """ Handles ASTNodes representing a simple Integer. """
        return Expression(node.getInteger())

    def handleReal(self, node):
        """ Handles ASTNodes representing a simple real/double/float. """
        return Expression(node.getReal())

    def handleString(self, node):
        """ Handles ASTNodes representing a simple String. """
        return Expression(node.getName())

    def handleOdeTime(self, node=None):
        """ Handles ASTNodes representing the (ODE-)time variable. """
        return Expression("odeTime")


    def handleConstE(self, node=None):
        """ Handles ASTNodes representing the Euler constant e. """
        return Expression(math.e)

    def handleConstPi(self, node=None):
        """ Handles ASTNodes representing the constant pi. """
        return Expression(math.pi)

    def handleConstTrue(self, node=None):
        """ Handles ASTNodes representing a simple real/double/float. """
        return Expression(1.0)

    def handleConstFalse(self, node=None):
        """ Handles ASTNodes representing a simple real/double/float. """
        return Expression(0.0)

