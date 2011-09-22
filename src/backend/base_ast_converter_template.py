import logging

class BaseAstConverterTemplate(object):
    '''
    This is an "abstract" base class that defines all the methods that a ASTNode-to-X converter has to provide.

    The converter has several methods. Each method gets a libsbml ASTNode object (and other parameters, optionally)
    and converts it to a suitable representation. Depending on the actual implementation, this could be FORTRAN code
    or an PARKINcpp Expression class instance.

    @since: 2010-12-20
    '''

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    # This class does not have an __init__() because it is meant to be "abstract".
    # Inheriting classes might (and probably should) define a constructor.

    def setAstConverter(self, astConverter):
        '''
        Sets the AstConverter instance needed for recursive calls. (Can also be given to the constructor.)
        '''
        self.astConverter = astConverter

    def handlePlus(self, astNode):
        ''' Handles ASTNodes representing a "+". '''
        logging.debug("AstConverter.handlePlus has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleMinus(self, astNode):
        ''' Handles ASTNodes representing a "-". '''
        logging.debug("AstConverter.handleMinus has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleTimes(self, astNode):
        ''' Handles ASTNodes representing a "*". '''
        logging.debug("AstConverter.handleTimes has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleDivide(self, astNode):
        ''' Handles ASTNodes representing a "/". '''
        logging.debug("AstConverter.handleDivide has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handlePower(self, astNode):
        ''' Handles ASTNodes representing a power function. '''
        logging.debug("AstConverter.handlePower has not been implemented. The resulting mathematical expression will contain errors.")
        return None


    def handleLog(self, node):
        ''' Handles ASTNodes representing a log function. '''
        logging.debug("AstConverter.handleLog has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleLn(self, node):
        ''' Handles ASTNodes representing a ln function. '''
        logging.debug("AstConverter.handleLn has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleHill(self, astNode):
        ''' Handles ASTNodes representing a Hill function. '''
        logging.debug("AstConverter.handleHill has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleUserFunction(self, astNode):
        ''' Handles ASTNodes representing a user-defined function. The actual function has to be
        looked up in the SBML definition and can then be recursively parsed, if it consists of mathematical
        expressions that are supported by the AstConverter. '''
        logging.debug("AstConverter.handleUserFunction has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleLambda(self, astNode):
        ''' Handles ASTNodes representing a Lambda function. These are used internally in SBML's user-defined
        functions. '''
        logging.debug("AstConverter.handleLambda has not been implemented. The resulting mathematical expression will contain errors.")
        return None


    def handleInt(self, astNode):
        ''' Handles ASTNodes representing an Integer value. '''
        logging.debug("AstConverter.handleInt has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleReal(self, astNode):
        ''' Handles ASTNodes representing a Real value. '''
        logging.debug("AstConverter.handleReal has not been implemented. The resulting mathematical expression will contain errors.")
        return None

    def handleString(self, astNode):
        ''' Handles ASTNodes representing a String. '''
        logging.debug("AstConverter.handleString has not been implemented. The resulting mathematical expression will contain errors.")
        return None

