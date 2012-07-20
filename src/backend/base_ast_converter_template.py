import logging

class BaseAstConverterTemplate(object):
    """
    This is an "abstract" base class that defines all the methods that a ASTNode-to-X converter has to provide.

    The converter has several methods. Each method gets a libsbml ASTNode object (and other parameters, optionally)
    and converts it to a suitable representation. Depending on the actual implementation, this could be FORTRAN code
    or an PARKINcpp Expression class instance.

    @since: 2010-12-20
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    # This class does not have an __init__() because it is meant to be "abstract".
    # Inheriting classes might (and probably should) define a constructor.

    def setAstConverter(self, astConverter):
        """
        Sets the AstConverter instance needed for recursive calls. (Can also be given to the constructor.)
        """
        self.astConverter = astConverter

    def handleConstE(self, astNode):
        """ Handles ASTNodes representing the Euler constant e. """
        logging.debug("AstConverter.handleConstE has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleConstPi(self, astNode):
        """ Handles ASTNodes representing the constant pi. """
        logging.debug("AstConverter.handleConstPi has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleConstTrue(self, astNode):
        """ Handles ASTNodes representing "true". """
        logging.debug("AstConverter.handleConstTrue has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleConstFalse(self, astNode):
        """ Handles ASTNodes representing "false". """
        logging.debug("AstConverter.handleConstFalse has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handlePlus(self, astNode):
        """ Handles ASTNodes representing a "+". """
        logging.debug("AstConverter.handlePlus has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleMinus(self, astNode):
        """ Handles ASTNodes representing a "-". """
        logging.debug("AstConverter.handleMinus has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleTimes(self, astNode):
        """ Handles ASTNodes representing a "*". """
        logging.debug("AstConverter.handleTimes has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleDivide(self, astNode):
        """ Handles ASTNodes representing a "/". """
        logging.debug("AstConverter.handleDivide has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handlePower(self, astNode):
        """ Handles ASTNodes representing a power function. """
        logging.debug("AstConverter.handlePower has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleLog(self, node):
        """ Handles ASTNodes representing a log function. """
        logging.debug("AstConverter.handleLog has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleLn(self, node):
        """ Handles ASTNodes representing a ln function. """
        logging.debug("AstConverter.handleLn has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleExp(self, node):
        """ Handles ASTNodes representing an exp function. """
        logging.debug("AstConverter.handleExp has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleAbs(self, node):
        """ Handles ASTNodes representing an abs function. """
        logging.debug("AstConverter.handleAbs has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleCeiling(self, node):
        """ Handles ASTNodes representing a ceil function. """
        logging.debug("AstConverter.handleCeiling has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleFloor(self, node):
        """ Handles ASTNodes representing a floor function. """
        logging.debug("AstConverter.handleFloor has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleSin(self, node):
        """ Handles ASTNodes representing a sin function. """
        logging.debug("AstConverter.handleSin has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleCos(self, node):
        """ Handles ASTNodes representing a cos function. """
        logging.debug("AstConverter.handleCos has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleHill(self, astNode):
        """ Handles ASTNodes representing a Hill function. """
        logging.debug("AstConverter.handleHill has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleUserFunction(self, astNode):
        """ Handles ASTNodes representing a user-defined function. The actual function has to be
        looked up in the SBML definition and can then be recursively parsed, if it consists of mathematical
        expressions that are supported by the AstConverter. """
        logging.debug("AstConverter.handleUserFunction has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleLambda(self, astNode):
        """ Handles ASTNodes representing a Lambda function. These are used internally in SBML's user-defined
        functions. """
        logging.debug("AstConverter.handleLambda has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleInt(self, astNode):
        """ Handles ASTNodes representing an Integer value. """
        logging.debug("AstConverter.handleInt has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleReal(self, astNode):
        """ Handles ASTNodes representing a Real value. """
        logging.debug("AstConverter.handleReal has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleOdeTime(self, astNode):
        """ Handles ASTNodes representing the (ODE-)Time value. """
        logging.debug("AstConverter.handleOdeTime has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleString(self, astNode):
        """ Handles ASTNodes representing a String. """
        logging.debug("AstConverter.handleString has not been implemented. The resulting mathematical expression will contain errors.")
        return None

