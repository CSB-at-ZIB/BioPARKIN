
import logging
import libsbml
from odehandling.odewrapper import ODEWrapper


class ODEGenerator(object):
    """
    This class takes a given SBML model (wrapped into a SBMLMainModel)
    and computes ODEs out of all the given SBML Reactions.

    It is necessary for integrating models that use Reactions (and are not
    only built by using Rules).

    The complete set of generated ODEs and of (Rate)Rules can then be given
    to the integrator.

    @param mainModel: A complete SBML MainModel
    @type mainModel: sbml_model.sbml_mainmodel.SBMLMainModel

    @since: 2010-07-07
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, mainModel):
        """
        Setting up instance variables and invoking the ODE generation.
        """
        self.mainModel = mainModel

        self.ODEs = None

        self._generateODEs()


    def _generateODEs(self):
        """
        The starting point for the ODE generation algorithm.
        """
        logging.info("Starting ODE generation...")
        self.ODEs = []
        self.wrappedODEs = []
        index = 0
        for speciesEntity in self.mainModel.SbmlSpecies:
            if not speciesEntity.isDefiningOde():
                continue

            ode = self._odeFromReactions(speciesEntity)
            if ode:
                ode.speciesEntity = speciesEntity
                self.ODEs.append(ode)
                wrappedODE = ODEWrapper(index, mathNode=ode, mainModel=self.mainModel, id=speciesEntity.getId(),
                                        speciesEntity=speciesEntity)
                self.wrappedODEs.append(wrappedODE)
                index += 1

    def _odeFromReactions(self, speciesEntity):
        """
        Parses through all Reactions of the model that involve the given
        Species and sums up the stoichiometry, etc.
        """
        species = speciesEntity.Item
        ode = None

        #search for the species in all reactions, and
        #add up the kinetic laws * stoichiometry for
        #all consuming and producing reactions to
        #an ODE

        for reactionEntity in self.mainModel.SbmlReactions:
            reaction = reactionEntity[0].Item

            reactionSymbol = libsbml.ASTNode()
            reactionSymbol.setName(reaction.getId())

            kineticLaw = reaction.getKineticLaw()

            if not kineticLaw:
                logging.error("The model has no kinetic law for reaction %s" % reaction.getId())
                return

            reactantReferences = reaction.getListOfReactants()
            if (reactantReferences == None
                or len(reactantReferences) == 0):
                continue

            for reactantReference in reactantReferences:
                reactantWrapper = self.mainModel.dictOfSpecies[reactantReference.getSpecies()]
                if reactantWrapper.Item == species:
                    # Construct expression for reactant by multiplying the
                    # kinetic law with stoichiometry (math) and putting a
                    # minus in front of it
                    if reactantReference.isSetStoichiometryMath():
                        reactant = libsbml.ASTNode()
                        reactant.setCharacter("*")
                        tmp = reactantReference.getStoichiometryMath().getMath()
                        reactant.addChild(self.copyAST(tmp))
                        reactant.addChild(self.copyAST(reactionSymbol))
                    else:
                        if reactantReference.getStoichiometry() == 1.0:
                            reactant = self.copyAST(reactionSymbol)
                        else:
                            reactant = libsbml.ASTNode()
                            reactant.setCharacter("*")
                            tmp = libsbml.ASTNode()
                            tmp.setValue(reactantReference.getStoichiometry())
                            reactant.addChild(tmp)
                            reactant.addChild(self.copyAST(reactionSymbol))

                    # Add reactant expression to ODE
                    if not ode:
                        ode = libsbml.ASTNode()
                        ode.setCharacter("-")
                        ode.addChild(reactant)
                    else:
                        tmp = self.copyAST(ode)
                        ode = libsbml.ASTNode()
                        ode.setCharacter("-")
                        ode.addChild(tmp)
                        ode.addChild(reactant)

            productReferences = reaction.getListOfProducts()
            if (productReferences == None
                or len(productReferences) == 0):
                continue
            for productReference in productReferences:
                try:
                    reactantWrapper = self.mainModel.dictOfSpecies[productReference.getSpecies()]
                except KeyError, e:
                    logging.error("Could not create ODEs. Species is missing: %s" % e)
                    raise
                if reactantWrapper.Item == species:
                    reactant = libsbml.ASTNode()
                    reactant.setCharacter("*")

                    if productReference.isSetStoichiometryMath():
                        tmp = productReference.getStoichiometryMath().getMath()
                        reactant.addChild(self.copyAST(tmp))
                    else:
                        tmp = libsbml.ASTNode()
                        tmp.setValue(productReference.getStoichiometry())
                        reactant.addChild(tmp)
                    reactant.addChild(self.copyAST(reactionSymbol))

                    # Add reactant expression to ODE
                    if not ode:
                        ode = reactant
                    else:
                        tmp = self.copyAST(ode)
                        ode = libsbml.ASTNode()
                        ode.setCharacter("+")
                        ode.addChild(tmp)
                        ode.addChild(reactant)

                    #        # TODO: Reenable this! Stoichiometry won't work correctly without it.
                    #
                    #        # Divide ODE by Name of the species' compartment.
                    #        # If formula is empty skip division by compartment and set formula
                    #        # to 0.  The latter case can happen, if a species is neither
                    #        # constant nor a boundary condition but appears only as a modifier
                    #        # in reactions.  The rate for such species is set to 0.
                    #        if ode:
                    #            #compartment = self.mainModel.SbmlModel.getCompartmentById(species.getCompartment())
                    #            for compartmentEntity in self.mainModel.SbmlCompartments:
                    #                compartment = compartmentEntity.Item
                    #                if compartment.getId() == species.getCompartment():
                    #                    tmp = self.copyAST(ode)
                    #                    ode = libsbml.ASTNode()
                    #                    ode.setCharacter("/")
                    #                    ode.addChild(tmp)
                    #                    temp = libsbml.ASTNode()
                    #                    temp.setName(compartment.getId())
                    #                    ode.addChild(temp)
                    #        else:
                    #            # for modifier species that never appear as products or reactants
                    #            # but are not defined as constant or boundarySpecies, set ODE to 0.
                    #            ode = libsbml.ASTNode()
                    #            ode.setValue(0) # change for DAE models should be defined by algebraic rule!

                    #        simpleOde = self.simplifyAST(ode)    # does not yet work correctly
                    #        return simpleOde

        return ode



    def copyAST(self, original):
        """
        Copies the passed AST, including potential SOSlib ASTNodeIndex, and
        returns the copy.
        """
        copy = libsbml.ASTNode()

        # Distinction of cases

        #integers, reals
        if original.isInteger():
            copy.setValue(original.getInteger())
        elif original.isReal():
            copy.setValue(original.getReal())

        # variables
        elif original.isName():
            #if original.isSetIndex():
            if original is ASTIndexNameNode:
                copy = ASTIndexNameNode()
                copy.setIndex(original.getIndex())
            copy.setName(original.getName())

            # time and delay nodes
            copy.setType(original.getType())

            #if original.isSetData():
            if original is ASTIndexNameNode and original.getData is not None:
                copy.setData()

        # constants, functions, operators
        else:
            copy.setType(original.getType())

            # user-defined functions: name must be set
            if original.getType() == libsbml.AST_FUNCTION:
                copy.setName(original.getName())
            for i in xrange(original.getNumChildren()):
                copy.addChild(self.copyAST(original.getChild(i)))

        return copy


    def simplifyAST(self, org):
        """
        Takes an AST f, and returns a simplified copy of f.

        decomposes n-ary `times' and `plus' nodes into an AST of binary AST.

        simplifies (arithmetic) operations involving 0 and 1: \n
        -0 -> 0;\n
        x+0 -> x, 0+x -> x;\n
        x-0 -> x, 0-x -> -x;\n
        x*0 -> 0, 0*x -> 0, x*1 -> x, 1*x -> x;\n
        0/x -> 0, x/1 -> x;\n
        x^0 -> 1, x^1 -> x, 0^x -> 0, 1^x -> 1;\n

        propagates unary minuses\n
        --x -> x; \n
        -x + -y -> -(x+y), -x + y -> y-x,    x + -y -> x-y; \n
        -x - -y -> y-x,    -x - y -> -(x+y), x - -y -> x+y; \n
        -x * -y -> x*y,    -x * y -> -(x*y), x * -y -> -(x*y);\n
        -x / -y -> x/y,    -x / y -> -(x/y), x / -y -> -(x/y); \n

        calls evaluateAST(subtree), if no variables or user-defined
        functions occur in the AST subtree,

        calls itself recursively for childnodes.
        """
        # new ASTNode
        simple = libsbml.ASTNode()
        nodeType = org.getType()

        # DISTINCTION OF CASES

        # integers, reals
        if org.isInteger():
            simple.setValue(org.getInteger())
        elif org.isReal():
            simple.setValue(org.getReal())

        # variables
        elif org.isName():
            if org is ASTIndexNameNode:
                simple = ASTIndexNameNode()
                simple.setIndex(org.getIndex())

                if org.isSetData():
                    simple.setData()
                simple.setName(org.getName())
                simple.setType(org.getType())

        # --------------- operators with possible simplifications --------------
        # special operator: unary minus
        elif org.isUMinus():
            left = self.simplifyAST(org.getLeftChild())
            if self.zero(left):   # -0 = 0
                simple = left
            elif left.isUMinus(): # - -x
                simple = self.cutRoot(left)
            else:
                simple.setType(libsbml.AST_MINUS)
                simple.addChild(left)
        # general operators
        elif org.isOperator() or nodeType == libsbml.AST_FUNCTION_POWER:
            numOfChildren = org.getNumChildren()
            # zero operands: set to neutral element 
            if numOfChildren == 0:
                if nodeType == libsbml.AST_PLUS:
                    simple.setValue(0)
                elif nodeType == libsbml.AST_TIMES:
                    simple.setValue(1)
            #one operand: set node to operand
            elif numOfChildren == 1:
                if nodeType == libsbml.AST_PLUS:
                    simple = self.simplifyAST(org.getChild(0))
                elif nodeType == libsbml.AST_TIMES:
                    simple = self.simplifyAST(org.getChild(0))
            #>2 operands: recursively decompose
            #       into tree with 2 operands
            elif numOfChildren > 2:
                if nodeType == libsbml.AST_PLUS:
                    simple.setType(libsbml.AST_PLUS)
                elif nodeType == libsbml.AST_TIMES:
                    simple.setType(libsbml.AST_TIMES)
                    #copy/simplify left child ...
                simple.addChild(self.simplifyAST(org.getChild(0)))
                # ... and move other child down
                helper = libsbml.ASTNode()
                helper.setType(nodeType)
                for i in xrange(numOfChildren):
                    helper.addChild(self.simplifyAST(org.getChild(i)))
                    simple.addChild(self.simplifyAST(helper))
            # 2 operands: remove 0s and 1s and unary minuses
            else:
                left = self.simplifyAST(org.getLeftChild())
                right = self.simplifyAST(org.getRightChild())
                # default: simplification
                simplify = 1 # set flag
                if nodeType == libsbml.AST_PLUS:
                    # binary plus x + y
                    if self.zero(right):    # x+0 = x
                        simple = left
                    elif self.zero(left):   # 0+x=x
                        simple = right
                    elif left.isUMinus() and right.isUMinus():
                        # -x + -y
                        simple.setType(libsbml.AST_MINUS)
                        simple.addChild(libsbml.ASTNode())
                        helper = simple.getChild(0)
                        helper.setType(libsbml.AST_PLUS)
                        helper.addChild(self.cutRoot(left))
                        helper.addChild(self.cutRoot(right))
                    elif left.isUMinus():
                        # -x + y
                        simple.setType(libsbml.AST_MINUS)
                        simple.addChild(right)
                        simple.addChild(self.cutRoot(left))
                    elif right.isUMinus():
                        # x + -y
                        simple.setType(libsbml.AST_MINUS)
                        left.addChild(left)
                        simple.addChild(self.cutRoot(right))
                    else:
                        simplify = 0
                elif nodeType == libsbml.AST_MINUS:
                    # binary minus x - y
                    if self.zero(right):
                        # x-0 = x
                        simple = left
                    elif self.zero(left):
                        # 0-x = -x
                        simple.setType(nodeType)
                        simple.addChild(right)
                    elif left.isUMinus() and right.isUMinus():
                        # -x - -y
                        simple.setType(libsbml.AST_MINUS)
                        simple.addChild(self.cutRoot(right))
                        simple.addChild(self.cutRoot(left))
                    elif left.isUMinus():
                        # -x - y
                        simple.setType(libsbml.AST_MINUS)
                        simple.addChild(libsbml.ASTNode())
                        helper = simple.getChild(0)
                        helper.setType(libsbml.AST_PLUS)
                        helper.addChild(self.cutRoot(left))
                        helper.addChild(right)
                    elif right.isUMinus():
                        # x - -y
                        simple.setType(libsbml.AST_PLUS)
                        simple.addChild(left)
                        simple.addChild(self.cutRoot(right))
                    else:
                        simplify = 0
                elif nodeType == libsbml.AST_TIMES:
                    # binary times x * y
                    if self.zero(right):
                        # x*0 = 0
                        simple = right
                    elif self.zero(left):
                        # 0*x = 0
                        simple = left
                    elif self.one(right):
                        # x*1 = x
                        simple = left
                    elif self.one(left):
                        # 1*x = x
                        simple = right
                    elif left.isUMinus() and right.isUMinus():
                        # -x * -y
                        simple.setType(libsbml.AST_TIMES)
                        simple.addChild(self.cutRoot(left))
                        simple.addChild(self.cutRoot(right))
                    elif left.isUMinus():
                        # -x * y
                        simple.setType(libsbml.AST_MINUS)
                        simple.addChild(libsbml.ASTNode())
                        helper = simple.getChild(0)
                        helper.setType(libsbml.AST_TIMES)
                        helper.addChild(self.cutRoot(left))
                        helper.addChild(right)
                    elif right.isUMinus():
                        # x * -y
                        simple.setType(libsbml.AST_MINUS)
                        simple.addChild(libsbml.ASTNode())
                        helper = simple.getChild(0)
                        helper.setType(libsbml.AST_TIMES)
                        helper.addChild(left)
                        helper.addChild(self.cutRoot(right))
                    else:
                        simplify = 0
                elif nodeType == libsbml.AST_DIVIDE:
                    # binary divide x / y
                    if self.zero(left):
                        # 0/x = 0
                        simple = left
                    elif self.one(right):
                        # x/1 = x
                        simple = left
                    elif left.isUMinus() and right.isUMinus():
                        # -x / -y
                        simple.setType(libsbml.AST_DIVIDE)
                        simple.addChild(self.cutRoot(left))
                        simple.addChild(self.cutRoot(right))
                    elif left.isUMinus():
                        # -x / y
                        simple.setType(libsbml.AST_MINUS)
                        simple.addChild(libsbml.ASTNode())
                        helper = simple.getChild(0)
                        helper.setType(libsbml.AST_DIVIDE)
                        helper.addChild(self.cutRoot(left))
                        helper.addChild(right)
                    elif right.isUMinus():
                        # x / -y
                        simple.setType(libsbml.AST_MINUS)
                        simple.addChild(libsbml.ASTNode())
                        helper = simple.getChild(0)
                        helper.setType(libsbml.AST_DIVIDE)
                        helper.addChild(left)
                        helper.addChild(self.cutRoot(right))
                    else:
                        simplify = 0
                elif nodeType == libsbml.AST_POWER or nodeType == libsbml.AST_FUNCTION_POWER:
                    # power x^y
                    if self.zero(right):
                        # x^0 = 1
                        simple.setValue(1.0)
                    elif self.one(right):
                        # x^1 = x
                        simple = left
                    elif self.zero(left):
                        # 0^x = 0
                        simple.setValue(0.0)
                    elif self.one(left):
                        # 1^x = 1
                        simple.setValue(1.0)
                    else:
                        simplify = 0
                else:
                    logging.error("simplifyAST: unknown failure for operator nodeType")

            if not simplify:
                # after all, no simplification
                simple.setType(nodeType)
                simple.addChild(left)
                simple.addChild(right)

        # -------------------- cases with no simplifications ------------------- 
        #  constants (leaves)  
        #  functions, operators (branches)
        else:
            simple.setType((nodeType))
            # user-defined functions: name must be set
            if org.getType() == libsbml.AST_FUNCTION:
                simple.setName(org.getName())

            for i in xrange(org.getNumChildren):
                simple.addChild(self.simplifyAST(org.getChild(i)))

        return simple


    def zero(self, f):
        """
        Small helper function to determine if the value of a node is zero.

        TODO: Is this needed in Python?
        """
        if f.isReal():
            return f.getReal() == 0.0
        if f.isInteger():
            return f.getInteger() == 0
        return 0


    def one (self, f):
        """
        Small helper function to determine if the value of a node is one.

        TODO: Is this needed in Python?
        """
        if f.isReal():
            return f.getReal() == 1.0
        if f.isInteger():
            return f.getInteger() == 1
        return 0


    def cutRoot(self, old):
        return self.copyAST(old.getChild(0))


    def getNameNodes(self, mathNode, nameNodes):
        """
        Recursively gets all children ASTNodes of mathNode that
        are of type "Name".
        """
        if mathNode.isName():
            nameNodes.append(mathNode)

        numChildren = mathNode.getNumChildren()
        for i in xrange(numChildren):
            child = mathNode.getChild(i)
            self.getNameNodes(child, nameNodes)



# TODO:
#/** Returns true (1) if the ASTNode is an ASTIndexNameNode
# */
#SBML_ODESOLVER_API int ASTNode_isIndexName(ASTNode_t *node)
#{
#  return dynamic_cast<ASTIndexNameNode*>(node) != 0;
#}
#
#/** Returns true (1) if the an indexed ASTNode (ASTIndexNameNode) has
#    it's index set
#*/
#SBML_ODESOLVER_API unsigned int ASTNode_isSetIndex(ASTNode_t *node)
#{
#  return ASTNode_isIndexName(node) && static_cast<ASTIndexNameNode*>(node)->isSetIndex();
#}




class ASTIndexNameNode(libsbml.ASTNode):
    def __init__(self):
        self.index = -1
        self.data = None


    def getIndex(self):
        return self.index

    def setIndex(self, index):
        self.index = index

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data


#TODO:
#
#/* appends the symbols in the given AST to the given list.
#   'char *' strings are appended to the list these strings
#   should not be freed and exist as long as the AST. */
#void ASTNode_getSymbols(ASTNode_t *node, List_t *symbols)
#{
#  int i ;
#
#  if ( ASTNode_getType(node) == AST_NAME )
#    List_add(symbols, (char*) ASTNode_getName(node));
#
#  for ( i=0; i<ASTNode_getNumChildren(node); i++ )
#    ASTNode_getSymbols(ASTNode_getChild(node, i), symbols);
#}
#/* appends the indices in the given indexed AST to the given list. */
#int ASTNode_getIndices(ASTNode_t *node, List_t *indices)
#{
#  int i; 
#
#  if ( ASTNode_isSetIndex(node) )
#  {
#    int *idx;
#    ASSIGN_NEW_MEMORY(idx, int, 0);
#    *idx = ASTNode_getIndex(node);
#    List_add(indices, idx);
#  }
#
#  for ( i=0; i<ASTNode_getNumChildren(node); i++ )
#    ASTNode_getIndices(ASTNode_getChild(node, i), indices);
#
#  return 1;
#}