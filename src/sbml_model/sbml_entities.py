from PySide.QtCore import QObject, SIGNAL, Signal
import backend
from basics.helpers.enum import enum
import libsbml
import logging

TYPE = enum("TYPE", "COMPARTMENT, SPECIES, REACTION, NONE, PARAMETER, RULE, EVENT")

#### defining constant strings for Species/Parameter Threshold XML ####
XML_THRESHOLD_NAMESPACE = "http://www.zib.de/SBML/Threshold" # more or less arbitrary string. Important to define a standard.
XML_SCALE = "Scale"
XML_THRESHOLD_VALUE = "Value"

XML_CONSTRAINTS_NAMESPACE = "http://www.zib.de/SBML/ParameterConstraints" # more or less arbitrary string. Important to define a standard.
XML_CONSTRAINTS = "Constraints"
XML_CONSTRAINTS_TYPE = "Type"
XML_CONSTRAINTS_LOWERBOUND = "LowerBound"
XML_CONSTRAINTS_UPPERBOUND = "UpperBound"

class SBMLEntity(QObject):
    """
    This is a simple wrapper for the entity classes of libsbml.
    It's needed to emit signals when something has changed.

    It's also used for creating "conceptual" entities like a father "node"
    for all the different Species-containing entities. This greatly
    eases the work needed in the MainTreeModel.

    @param entity: A libSBML object. Can be None for father "nodes".
    @type entity: libSBML object

    @param label: Usually None when a libSBML object is given. Otherwise the name of the conceptual entity (e.g. "Species","Reactions", ...)
    @type label: str

    @param parent: Standard Qt parent
    @type parent: QObject

    @since: 2010-03-24
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def GetPosition(self):
        return self.__Position

    def SetPosition(self, value):
        self.__Position = value
        self.emit(SIGNAL("PositionChanged"))

    def DelPosition(self):
        del self.__Position

    Position = property(GetPosition, SetPosition, DelPosition, "The graphical position of this SBMLEntity.")

    idChanged = Signal(object, str, str)
    selectionChange = Signal(bool)
    hasChanged = Signal()


    def __init__(self, entity=None, label=None, parent=None):
        """
        Sets some instance variables, also determines the Type of
        this instance. Type is Type.NONE if no known libSBML entity
        is wrapped (e.g. for conceptual father nodes which don't
        wrap a libSBML object).
        """
        super(SBMLEntity, self).__init__()
        #        self.selectionChange = Signal(type(self),bool) # have to do this here, because of "self"

        self.Item = entity
        self.Label = label
        self.Parent = parent
        #        self.MainModel = self.getMainModel(parent)

        self.GraphicItem = None #: Reference to a QGraphicsView graphics item. Important because it is used to redraw stuff efficiently.
        self.Position = (0.0, 0.0)

        self.Children = []

        if self.Parent is not None:
            self.Parent.Children.append(self)

        # set TYPE
        self.Type = TYPE.NONE
        if isinstance(self.Item, libsbml.Compartment):
            self.Type = TYPE.COMPARTMENT
        elif isinstance(self.Item, libsbml.Species):
            self.Type = TYPE.SPECIES
            self.Threshold = self._initThreshold()
        elif isinstance(self.Item, libsbml.Reaction):
            self.Type = TYPE.REACTION
        elif isinstance(self.Item, libsbml.Parameter):
            self.Type = TYPE.PARAMETER
            self.Threshold = self._initThreshold()
            self._constraintType, self._constraintLowerBound, self._constraintUpperBound = self._initConstraints()
        elif isinstance(self.Item, libsbml.Rule):
            self.Type = TYPE.RULE
        elif isinstance(self.Item, libsbml.Event):
            self.Type = TYPE.EVENT

        self.SelectionStateJustChanged = False
        self.computeSensitivity = True


    def getRowOfChild(self, child):
        """
        Useful method which is used by MainTreeModel for example.
        Given a child, its index in the internal children list is
        returned. Only works for parent nodes (the others don't usually
        have any children).

        @param child: SBMLEntity object
        @type child: SBMLEntity

        @return: Row of given child in internal list.
        @rtype: int
        """
        if self.Children is None or child is None:
            return None
        try:
            return self.Children.index(child)
        except:
            logging.debug("SbmlEntity.getRowOfChild(): %s is no longer a child." % child.getId())
            return

    def getChildrenCount(self):
        """
        Useful method which is used by MainTreeModel for example.

        @return: Number of children.
        @rtype: int

        @todo: Maybe overload len() with this?
        """
        if self.Children is None:
            return 0
        return len(self.Children)

    def getIndex(self):
        """
        Useful method which is used by MainTreeModel for example.
        Returns the index of this instance in the parent's children list.

        @return: the index of this instance in the parent's children list.
        @rtype: int
        """
        return self.Parent.getRowOfChild(self)

    def getChild(self, index):
        """
        Useful method which is used by MainTreeModel for example.

        Returns the child with the given index.

        @return: the child with the given index.
        @rtype: SBMLEntity
        """

        if 0 <= index < self.getChildrenCount():
            return self.Children[index]

    def removeChild(self, index):
        """
        Removes the children with the given index from the internal list.
        """
        self.Children.pop(index)


    def changed(self):
        """
        To call when something has changed. Emits a changed Signal.
        Redraws the referenced graphics item.

        """
        self.emit(SIGNAL("changed()"))

        if self.GraphicItem is not None:
            self.GraphicItem.redraw()

    def on_selectionChange(self, value):
        """
        To call when selection of the corresponding SBMLEntity or
        graphical representation changes.
        Emits a selectionChange Signal.

        @param value: If selected, True; otherwise, False
        @type value: bool
        """
        if self.SelectionStateJustChanged:
            self.selectionChange.emit(self, value)
        self.SelectionStateJustChanged = True

    def getId(self):
        """
        Convenience method to return the ID of the wrapped
        libSBML object.

        @return: The ID of the wrapped libSBML object
        @rtype: str
        """
        if self.Item:
            return self.Item.getId()


    def getLabel(self):
        return self.Label

    def setId(self, id):
        oldId = self.getId()
        self.Item.setId(str(id))
        self.idChanged.emit(self, str(id), oldId)

    def getName(self):
        if self.Item:
            return self.Item.getName()

    def setName(self, name):
        self.Item.setName(str(name))
        self.changed.emit()

    def getValue(self):
        return self.Item.getValue()

    def setValue(self, value):
        try:
            self.Item.setValue(value)
        except:
            logging.debug("SbmlEntity.setValue: Could not set value %s" % value)

    def getInitialValue(self):
        if self.Type != TYPE.SPECIES: # can only do this for Species
            return False

        if self.Item.isSetInitialAmount():
            return self.Item.getInitialAmount()
        elif self.Item.isSetInitialConcentration():
            return self.Item.getInitialConcentration()
        else:
            logging.warning("Encountered Species with neither Initial Amount nor Concentration: %s" % self.getId())
            return

    def setReactants(self, reactantIDString):
        if self.Type != TYPE.REACTION: # can only do this for Reactions
            return False
        reactantIDs = reactantIDString.replace(" ", "").split(",")

        if reactantIDs is None or len(reactantIDs) == 0:
            return False

        reactantRefs = self.Item.getListOfReactants()
        IDsToRemove = []
        for reactantRef in reactantRefs:
            orgID = reactantRef.getSpecies()
            IDsToRemove.append(orgID)

        for ID in IDsToRemove:
            logging.info("Removing Reactant: %s" % ID)
            self.Item.removeReactant(ID)

        for ID in reactantIDs:
            if self.speciesIDExists(ID):
                speciesRef = libsbml.SpeciesReference(self.Item.getLevel(), self.Item.getVersion())
                speciesRef.setSpecies(ID)
                self.Item.addReactant(speciesRef)

        return True



    def setProducts(self, productIDString):
        if self.Type != TYPE.REACTION: # can only do this for Reactions
            return False
        productIDs = productIDString.replace(" ", "").split(",")

        if productIDs is None or len(productIDs) == 0:
            return False

        productRefs = self.Item.getListOfProducts()
        IDsToRemove = []
        for productRef in productRefs:
            orgID = productRef.getSpecies()
            IDsToRemove.append(orgID)

        for ID in IDsToRemove:
            logging.info("Removing Product: %s" % ID)
            self.Item.removeProduct(ID)

        for ID in productIDs:
            if self.speciesIDExists(ID):
                speciesRef = libsbml.SpeciesReference(self.Item.getLevel(), self.Item.getVersion())
                speciesRef.setSpecies(ID)
                self.Item.addProduct(speciesRef)

        return True


    def getTarget(self):
        """
        Get's the "variable" (aka target) of SBML Rules.

        @rtype: String

        @since: 2011-12-14
        """
        if hasattr(self.Item, "getVariable"): # has to be Rule or subclass (or anything with the getVariable method)
            return self.Item.getVariable()

    def getMath(self):
        """
        Returns a math ASTNode tree if self has the getMath method
        (e.g. Rules).

        @rtype: libsbml.ASTNode

        @since: 2011-12-14
        """
        if hasattr(self.Item, "getMath"):   # for everything that had the getMath method
            return self.Item.getMath()

    def setModifiers(self, modifierIdString):
        if self.Type != TYPE.REACTION: # can only do this for Reactions
            return False
        modifierIds = modifierIdString.replace(" ", "").split(",")

        if modifierIds is None or len(modifierIds) == 0:
            return False

        modifierRefs = self.Item.getListOfModifiers()
        IdsToRemove = []
        for modifierRef in modifierRefs:
            orgId = modifierRef.getSpecies()
            IdsToRemove.append(orgId)

        for Id in IdsToRemove:
            logging.info("Removing Modifier: %s" % Id)
            self.Item.removeModifier(Id)

        for Id in modifierIds:
            if self.speciesIDExists(Id):
                speciesRef = libsbml.ModifierSpeciesReference(self.Item.getLevel(), self.Item.getVersion())
                speciesRef.setSpecies(Id)
                self.Item.addModifier(speciesRef)

        return True

    def speciesIDExists(self, ID):
        model = self.Item.getModel()
        speciesRefList = model.getListOfSpecies()
        return ID in [x.getId() for x in speciesRefList]


    def isDefiningOde(self):
        """
        Checks whether the wrapped Species is "constant" or a "boundaryCondition". In those cases, no ODE
        should be generated, as per SBML's standards.
        """
        if self.Type != TYPE.SPECIES:
            return False

        #if self.Item.isSetConstant() and self.Item.getConstant():
        if self.Item.getConstant():
            return False

        #if self.Item.isSetBoundaryCondition() and self.Item.getBoundaryCondition():
        if self.Item.getBoundaryCondition():
            return False

        # if non of the above holds
        return True

    def isConstant(self):
        return self.Item.getConstant()

    def getScope(self):
        if self.Type != TYPE.PARAMETER: #only makes sense for Parameters
            return

        parent = self.Item.getParentSBMLObject()
        if parent:
            grandpa = parent.getParentSBMLObject()
            if type(grandpa) == libsbml.Model:
                return "Global"
            elif type(grandpa) == libsbml.KineticLaw:
                reaction = grandpa.getParentSBMLObject()
                return "%s" % reaction.getId()

    def getCombinedId(self):
        """
        Adds the scope as a prefix to the actual ID with an underscore between.
        This is needed for SBML Parameters because their ID is not necessarily unique (different parameters
        that are local to different Reactions can have identical IDs; e.g. often "k1", etc.)
        """
        if self.Type != TYPE.PARAMETER: #only makes sense for Parameters
            return self.getId()

        scope = self.getScope()
        if scope == "Global":
            return self.getId()
        else:
            return "%s_%s" % (scope, self.getId())


    def _initThreshold(self):
        """
        Parses the wrapped Species' XML annotations and retrieves the scale value
        if one is set.

        @since: 2011-05-23
        """
        self.thresholdNode = None
        species = self.Item

        if not species:
            return

        if not species.isSetAnnotation():
            return None

        annotationRootNode = species.getAnnotation()
        self.thresholdNode = annotationRootNode.getChild(XML_SCALE)
        if self.thresholdNode.isEOF():
            self.thresholdNode = None
            return None

        namespace = self.thresholdNode.getNamespaceURI()
        if namespace != XML_THRESHOLD_NAMESPACE:
            logging.warning("Threshold XML node in SBML file has unsupported namespace: %s" % namespace)

        if self.thresholdNode.hasAttr(XML_THRESHOLD_VALUE):
            value = self.thresholdNode.getAttrValue(XML_THRESHOLD_VALUE)
            return float(value)
        else:
            logging.warning("Species %s has a XML-defined threshold tag but no value is set." % self.getId())
            return None # we don't automatically compute scales any more. This is done via a button (or by hand).

        logging.debug("SbmlEntity._initThreshold(): This line should never be reached.")


    def getThreshold(self):
        """
        Just returns the current value of self.Scale.

        @since: 2011-05-23
        """
        return self.Threshold

    def setThreshold(self, value):
        """
        "Public" method to set the scale factor of this Species/Parameter.
        Updates not only self.Scale but also the XML associated with self.Item (by invoking self._setScaleXml()).
        Whenever the model is saved to a file, this XML will be written.

        @since: 2011-05-23
        """
        self.Threshold = value
        self._setThresholdXml(value)

    def _setThresholdXml(self, value):
        """
        Uses the value to update the internal libsbml.XMLNode structure.
        If there is a reference to an existing XML node (from loading the file)
        it is used. Otherwise, it's created.

        @since: 2011-05-23
        """
        if not self.thresholdNode:  # have to create the XML node
            thresholdNodeTriplet = libsbml.XMLTriple(XML_SCALE, XML_THRESHOLD_NAMESPACE, "")
            thresholdNodeAttribute = libsbml.XMLAttributes()
            thresholdNodeAttribute.add(XML_THRESHOLD_VALUE, str(value))

            self.thresholdNode = libsbml.XMLNode(thresholdNodeTriplet, thresholdNodeAttribute)

            namespace = libsbml.XMLNamespaces() # seems to be necessary to do this again
            namespace.add(XML_THRESHOLD_NAMESPACE)
            self.thresholdNode.setNamespaces(namespace)

            self.Item.appendAnnotation(self.thresholdNode)
        else:
            thresholdNodeAttribute = libsbml.XMLAttributes()
            thresholdNodeAttribute.add(XML_THRESHOLD_VALUE, str(value))
            self.thresholdNode.setAttributes(thresholdNodeAttribute)

    def setComputeSensitivity(self, bool):
        self.computeSensitivity = bool

    def getComputeSensitivity(self):
        return self.computeSensitivity

    def getConstraintType(self):
        """

        @since: 2012-01-25
        """
        return self._constraintType

    def setConstraintType(self, type):
        """

        @since: 2012-01-25
        """
        self._constraintType = type
        self._setConstraintsXml(type, self._constraintLowerBound, self._constraintUpperBound)

    def getConstraintLowerBound(self):
        """

        @since: 2012-01-25
        """
        return self._constraintLowerBound

    def setConstraintLowerBound(self, lower):
        """

        @since: 2012-01-25
        """
        self._constraintLowerBound = lower
        self._setConstraintsXml(self._constraintType, lower, self._constraintUpperBound)

    def getConstraintUpperBound(self):
        """

        @since: 2012-01-25
        """
        return self._constraintUpperBound

    def setConstraintUpperBound(self, upper):
        """

        @since: 2012-01-25
        """
        self._constraintUpperBound = upper
        self._setConstraintsXml(self._constraintType, self._constraintLowerBound, upper)

    def _initConstraints(self):
        """

        @since: 2012-01-25
        """
        self._constraintsXmlNode = None
        entity = self.Item

        defaultValues = (backend.settingsandvalues.DEFAULT_PARAMETER_CONSTRAINTS,
                         backend.settingsandvalues.DEFAULT_PARAMETER_CONSTRAINTS_LOWERBOUND,
                         backend.settingsandvalues.DEFAULT_PARAMETER_CONSTRAINTS_UPPERBOUND)

        if not entity:
            return defaultValues

        if not entity.isSetAnnotation():
            logging.debug("Parameter %s does not have any annotations.\nSetting constraints to 'None'." % self.getId())
            return defaultValues

        annotationRootNode = entity.getAnnotation()
        self._constraintsXmlNode = annotationRootNode.getChild(XML_CONSTRAINTS)
        if self._constraintsXmlNode.isEOF():
            logging.debug("Parameter %s does have annotations but no Constraints information.\nSetting constraints to 'None'." % self.getId())
            self._constraintsXmlNode = None
            return defaultValues

        namespace = self._constraintsXmlNode.getNamespaceURI()
        if namespace != XML_CONSTRAINTS_NAMESPACE:
            logging.warning("Constraints XML node in SBML file has unsupported namespace: %s\nContinuing anyway." % namespace)


        if self._constraintsXmlNode.hasAttr(XML_CONSTRAINTS_TYPE):
            type = self._constraintsXmlNode.getAttrValue(XML_CONSTRAINTS_TYPE)
        else:
            logging.warning("Species %s has a XML-defined Constraint tag but no type is set.\nSetting constraints to 'None'." % self.getId())
            type = backend.settingsandvalues.DEFAULT_PARAMETER_CONSTRAINTS
        if self._constraintsXmlNode.hasAttr(XML_CONSTRAINTS_LOWERBOUND):
            lower = self._constraintsXmlNode.getAttrValue(XML_CONSTRAINTS_LOWERBOUND)
        else:
            lower = backend.settingsandvalues.DEFAULT_PARAMETER_CONSTRAINTS_LOWERBOUND
        if self._constraintsXmlNode.hasAttr(XML_CONSTRAINTS_UPPERBOUND):
            upper = self._constraintsXmlNode.getAttrValue(XML_CONSTRAINTS_UPPERBOUND)
        else:
            upper = backend.settingsandvalues.DEFAULT_PARAMETER_CONSTRAINTS_UPPERBOUND

        return type, lower, upper


    def _setConstraintsXml(self, type, lower, upper):
        """

        @since: 2012-01-25
        """
        if not self._constraintsXmlNode:  # have to create the XML node
            constraintsNodeTriplet = libsbml.XMLTriple(XML_CONSTRAINTS, XML_CONSTRAINTS_NAMESPACE, "")
            constraintsNodeAttribute = libsbml.XMLAttributes()
            constraintsNodeAttribute.add(XML_CONSTRAINTS_TYPE, str(type))
            constraintsNodeAttribute.add(XML_CONSTRAINTS_LOWERBOUND, str(lower))
            constraintsNodeAttribute.add(XML_CONSTRAINTS_UPPERBOUND, str(upper))

            self._constraintsXmlNode = libsbml.XMLNode(constraintsNodeTriplet, constraintsNodeAttribute)

            namespace = libsbml.XMLNamespaces() # seems to be necessary to do this again
            namespace.add(XML_CONSTRAINTS_NAMESPACE)
            self._constraintsXmlNode.setNamespaces(namespace)

            self.Item.appendAnnotation(self._constraintsXmlNode)
        else:
            constraintsNodeAttribute = libsbml.XMLAttributes()
            constraintsNodeAttribute.add(XML_CONSTRAINTS_TYPE, str(type))
            constraintsNodeAttribute.add(XML_CONSTRAINTS_LOWERBOUND, str(lower))
            constraintsNodeAttribute.add(XML_CONSTRAINTS_UPPERBOUND, str(upper))
            self._constraintsXmlNode.setAttributes(constraintsNodeAttribute)