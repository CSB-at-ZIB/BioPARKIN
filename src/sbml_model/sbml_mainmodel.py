from PySide.QtCore import QObject, Signal, Slot, QModelIndex
import libsbml
from sbml_model.definitions import CHANGETYPE, XML_PARAMETER_SET_NAME, XML_PARAMETER_SET_ID, XML_PARAMETER_SBML_ID, XML_PARAMETER_VALUE, XML_PARAMETER_REACTION_ID, XML_LIST_OF_PARAMETER_SETS_ACTIVE, XML_NAMESPACE_PARAMETER_SETS, XML_LIST_OF_PARAMETER_SETS, XML_PARAMETER, XML_PARAMETER_SET, PARAM_SET_INITIAL_GUESS, PARAM_SET_ORIGINAL, PARAM_SET_FIT
from sbml_model.parameter_sets import ListOfParameterSets, ParameterSet, ParameterProxy

import logging
from sbml_model.sbml_entities import SBMLEntity
from sbml_model.sbml_maintreemodel import SBMLMainTreeModel
import sbml_entities
from services.warningservice import WarningService




class SBMLMainModel(QObject):
    """
    This model encapsulates a SBML file and provides relevant parts of it
    (Species, Reactions, ...) in a unified MainTreeModel.

    Using the Qt Model approach enables easy connection to UI Views.

    @param filename: Filename of the SBML file to wrap
    @type filename: str

    @since: 2010-02-024
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    def GetDirty(self):
        return self.__Dirty


    def SetDirty(self, value):
        self.__Dirty = value
        self.dirtyChanged.emit(value)


    def DelDirty(self):
        del self.__Dirty

    Dirty = property(GetDirty, SetDirty, DelDirty, "Defines whether this model has any unsaved changes.")


    dirtyChanged = Signal(bool)
    selectionChange = Signal(SBMLEntity,bool)
    structuralChange = Signal(SBMLEntity,int)

    def __init__(self, filename=None):
        """
        Prepares instance variables, calls the file loading method.
        Connects the dataChanged Signal of the internal MainTreeModel to
        a helper method.
        """
        super(SBMLMainModel, self).__init__()

        # data:
        self.SbmlDocument = None
        self.SbmlModel = None
        self.SbmlCompartments = None
        self.SbmlSpecies = None
        self.SbmlReactions = None
        self.SbmlParameters = None
        self.SbmlRateRules = None
        self.SbmlAlgebraicRules = None
        self.SbmlAssignmentRules = None
        self.SbmlEvents = None

        self.ListOfParameterSets = None #ListOfParameterSets()

        #TODO self.SbmlUnitDefinitions = None

        self.CompartmentWrapper = None
        self.SpeciesWrapper = None
        self.ReactionWrapper = None
        self.ParameterWrapper = None
        self.RateRuleWrapper = None
        self.AlgebraicRuleWrapper = None
        self.AssignmentRuleWrapper = None
        self.EventsWrapper = None

        self.newSpeciesCount = 0 # used for creating implicit Species (needed by some Reactions)

        self.paramSetsListNode = None   # will hold the libsbml.XMLNode

        self.warningService = WarningService.getInstance()

        if filename is not None:
            self._load(filename)

        # models: this class basically exists to access all the individual models
        self.MainTreeModel = SBMLMainTreeModel(self)
        self.checkConsistency()

        self.MainTreeModel.dataChanged.connect(self.dataChanged)
        self.MainTreeModel.structuralChange.connect(self.on_structuralChange)


        #debugging: use modeltester
        #self.modeltest = ModelTest(self.MainTreeModel, self)

    def getSpecies(self, id):
        if self.dictOfSpecies.has_key(id):
            return self.dictOfSpecies[id]
        return None

    def checkConsistency(self):
        errorStringComplete = None
        try:
            numErrors = self.SbmlDocument.Item.checkConsistency()
            if numErrors > 0:
                logging.info("There were errors or warnings while loading the file.")

            errorStringComplete = ""
            for i in xrange(numErrors):
                error = self.SbmlDocument.Item.getError(i)
                errorMsgShort = error.getShortMessage()
                errorMsgLong = error.getMessage()
                severity = error.getSeverityAsString()
                category = error.getCategoryAsString()
                errorString = "Error %s (Severity: %s; Category: %s): %s\n%s" % (
                i, severity, category, errorMsgShort, errorMsgLong)
                logging.info(errorString)
                errorStringComplete += errorString + "\n\n"
        except Exception, e:
            logging.error(
                "SbmlMainmodel.checkConsistency(): Error while checking consistency of SBML Document. Error: %s" % e)

        if errorStringComplete:
            self.showConsistencyDialog(errorStringComplete)

    def showConsistencyDialog(self, errorString):
        self.warningService.appendWarning(errorString, "Opening the SBML file resulted in warnings.")


    def _load(self, filename):
        '''
        Loads an SBML file into memory, prepares access to
        Species, Compartments, etc. parts.
        
        Puts all the libSBML objects into SBMLEntity wrappers.
        
        @param filename: Filename of the SBML file to wrap
        @type filename: str
        '''
        self.filename = str(filename) # assures that filename is not a unicode string which libsbml can't handle

        try:
            logging.info("Loading SBML file %s" % self.filename)
            reader = libsbml.SBMLReader()
            document = reader.readSBML(self.filename)

            numErrors = document.getNumErrors()

            if numErrors > 0:
                logging.warning("The SBML file has errors:")
                for i in range(numErrors):
                    error = document.getError(i)
                    logging.warning("Error #%i: %s" % (i, error.getMessage()))
                return
            else:
                self.SbmlDocument = self.createSBMLEntity(document)
        except Exception, e:
            logging.error("Error loading file %s: %s" % (self.filename, e))
            return



        # store model, parts of model and print some info
        self.SbmlModel = self.createSBMLEntity(self.SbmlDocument.Item.getModel())   # set parent to Document?
        logging.info("Model name: %s" % self.SbmlModel.Item.getName())

        self._loadParameterSets()

        # create wrapper objects for Compartments, Species, Reactions, ... for easy use in tree model
        self.CompartmentWrapper = self.createSBMLEntity(sbmlobject=None, label="Compartments", parent=self.SbmlModel)
        self.SpeciesWrapper = self.createSBMLEntity(sbmlobject=None, label="Species", parent=self.SbmlModel)
        self.ReactionWrapper = self.createSBMLEntity(sbmlobject=None, label="Reactions", parent=self.SbmlModel)
        self.ParameterWrapper = self.createSBMLEntity(sbmlobject=None, label="Parameters", parent=self.SbmlModel)
        self.RateRuleWrapper = self.createSBMLEntity(sbmlobject=None, label="Rate Rules", parent=self.SbmlModel)
        self.AlgebraicRuleWrapper = self.createSBMLEntity(sbmlobject=None, label="Algebraic Rules",
                                                          parent=self.SbmlModel)
        self.AssignmentRuleWrapper = self.createSBMLEntity(sbmlobject=None, label="Assignment Rules",
                                                           parent=self.SbmlModel)
        self.EventsWrapper = self.createSBMLEntity(sbmlobject=None, label="Events", parent=self.SbmlModel)

        self.prepareReactions()

        self.wrapSpecies()

        self.wrapCompartments()

        self.wrapGlobalParameters()

        self.wrapReactions()

        self.wrapRules()

        self.wrapEvents()

        self.createDefaultParameterSet()

#        self._handleScalingValues()

        # region: getters

    #    def get_sbml_model(self): return self.SbmlModel
    #    def get_compartments(self): return self.SbmlCompartments
    #    def get_species(self): return self.SbmlSpecies
    #    def get_reactions(self): return self.SbmlReactions

    #    def get_compartment_model(self):
    #        if self.CompartmentTableModel is None:
    #            self.CompartmentTableModel = SBMLCompartmentModel(self)
    #        return self.CompartmentTableModel


    def createSBMLEntity(self, sbmlobject=None, label=None, parent=None):
        '''
        Small helper method to wrap the given libSBML object into
        a SBMLEntity.
        
        @param sbmlobject: libSBML object to wrap
        @type sbmlobject: any libSBML object (e.g. Species, Reaction, ...)
        
        @param label: A label for the SBMLEntity (usually used for conceptual father "nodes")
        @type label: str
        
        @param parent: A SBMLEntity that is the conceptual father node of the given sbmlobject
        @type parent: SBMLEntity
        
        @return: The just created SBMLEntity
        @rtype: SBMLEntity
        
        '''
        sbmlEntity = SBMLEntity(sbmlobject, label, parent)
        sbmlEntity.selectionChange.connect(self.sbml_entity_selection_changed)
        sbmlEntity.idChanged.connect(self.on_entityIdChanged)
        return sbmlEntity

    def addSpecies(self, params={}, index=None):
        id = params.get("id", "NewSpecies")
        name = params.get("name", "New Species")

        newSpecies = self.SbmlModel.Item.createSpecies()    # best way to create new entities
        newSpecies.setId(id)
        newSpecies.setName(name)

        newSpecies.setCompartment("default")

        logging.info("Species: %s" % newSpecies.getName())
        wrappedEntity = self.createSBMLEntity(sbmlobject=newSpecies, parent=self.SpeciesWrapper)

        if index and index < len(self.SbmlSpecies):
            self.SbmlSpecies.insert(index, wrappedEntity)
        else:
            self.SbmlSpecies.append(wrappedEntity)

        self.dictOfSpecies[newSpecies.getId()] = wrappedEntity

        self.Dirty = True
        self.on_structuralChange(wrappedEntity, CHANGETYPE.ADD)


    def addCompartment(self, params={}, index=None):
        id = params.get("id", "NewCompartment")
        name = params.get("name", "New Compartment")

        newCompartment = self.SbmlModel.Item.createCompartment()    # best way to create new entities
        newCompartment.setId(id)
        newCompartment.setName(name)

        logging.info("Compartment: %s" % newCompartment.getName())
        wrappedEntity = self.createSBMLEntity(sbmlobject=newCompartment, parent=self.CompartmentWrapper)

        if index and index < len(self.SbmlCompartments):
            self.SbmlCompartments.insert(index, wrappedEntity)
        else:
            self.SbmlCompartments.append(wrappedEntity)

        self.Dirty = True
        self.on_structuralChange(wrappedEntity, CHANGETYPE.ADD)


    def addReaction(self, params={}, index=None):
        id = params.get("id", "NewReaction")
        name = params.get("name", "New Reaction")

        newReaction = self.SbmlModel.Item.createReaction()    # best way to create new entities
        newReaction.setId(id)
        newReaction.setName(name)

        logging.info("Reaction: %s" % newReaction.getName())
        wrappedEntity = self.createSBMLEntity(sbmlobject=newReaction, parent=self.ReactionWrapper)

        if index and index < len(self.SbmlReactions):
            self.SbmlReactions.insert(index, wrappedEntity)
        else:
            self.SbmlReactions.append(wrappedEntity)

        self.Dirty = True
        self.on_structuralChange(wrappedEntity, CHANGETYPE.ADD)


    def addParameter(self, params={}, index=None):
        id = params.get("id", "NewParameter")
        name = params.get("name", "New Parameter")

        newParameter = self.SbmlModel.Item.createParameter()    # best way to create new entities
        newParameter.setId(id)
        newParameter.setName(name)

        logging.info("Parameter: %s" % newParameter.getName())
        wrappedEntity = self.createSBMLEntity(sbmlobject=newParameter, parent=self.ParameterWrapper)

        if index and index < len(self.SbmlParameters):
            self.SbmlParameters.insert(index, wrappedEntity)
        else:
            self.SbmlParameters.append(wrappedEntity)

        self.Dirty = True
        self.on_structuralChange(wrappedEntity, CHANGETYPE.ADD)


    def addRateRule(self, params={}, index=None):
        id = params.get("id", "NewRateRule")
        name = params.get("name", "New Rate Rule")

        newRateRule = self.SbmlModel.Item.createRateRule()    # best way to create new entities
        newRateRule.setId(id)
        newRateRule.setName(name)

        logging.info("Rate Rule: %s" % newRateRule.getName())
        wrappedEntity = self.createSBMLEntity(sbmlobject=newRateRule, parent=self.RateRuleWrapper)

        if index and index < len(self.SbmlRateRules):
            self.SbmlRateRules.insert(index, wrappedEntity)
        else:
            self.SbmlRateRules.append(wrappedEntity)

        self.Dirty = True
        self.on_structuralChange(wrappedEntity, CHANGETYPE.ADD)


    #    def addEntity(self, sbmlObject, index = None):
    #        #sbmlWrapper = self.createSBMLEntity(sbmlobject = sbmlObject)
    #
    #        if type(sbmlObject) is libsbml.Species:
    #            logging.info("Species: %s" % sbmlObject.getName())
    #            wrappedEntity = self.createSBMLEntity(sbmlobject=sbmlObject, parent=self.SpeciesWrapper)
    #            if index and index < len(self.SbmlSpecies):
    #                self.SbmlSpecies.insert(index, wrappedEntity)
    #                self.SbmlModel.Item.a
    #            else:
    #                self.SbmlSpecies.append(wrappedEntity)
    #            self.dictOfSpecies[sbmlObject.getId()] = wrappedEntity
    #        elif type(sbmlObject) is libsbml.Compartment:
    #            logging.info("Compartment: %s" % sbmlObject.getName())
    #            wrappedEntity = self.createSBMLEntity(sbmlobject=sbmlObject, parent=self.CompartmentWrapper)
    #            if index and index < len(self.SbmlCompartments):
    #                self.SbmlCompartments.insert(index, wrappedEntity)
    #            else:
    #                self.SbmlCompartments.append(wrappedEntity)
    #            #self.dictOfSpecies[sbmlObject.getId()] = wrappedEntity
    #        elif type(sbmlObject) is libsbml.Reaction:
    #            logging.info("Reaction: %s" % sbmlObject.getName())
    #            wrappedEntity = self.createSBMLEntity(sbmlobject=sbmlObject, parent=self.ReactionWrapper)
    #            if index and index < len(self.SbmlReactions):
    #                self.SbmlReactions.insert(index, wrappedEntity)
    #            else:
    #                self.SbmlReactions.append(wrappedEntity)
    #        elif type(sbmlObject) is libsbml.Parameter:
    #            logging.info("Parameter: %s" % sbmlObject.getName())
    #            wrappedEntity = self.createSBMLEntity(sbmlobject=sbmlObject, parent=self.ParameterWrapper)
    #            if index and index < len(self.SbmlParameters):
    #                self.SbmlParameters.insert(index, wrappedEntity)
    #            else:
    #                self.SbmlParameters.append(wrappedEntity)
    #        elif type(sbmlObject) is libsbml.RateRule:
    #            logging.info("RateRule: %s" % sbmlObject.getName())
    #            wrappedEntity = self.createSBMLEntity(sbmlobject=sbmlObject, parent=self.RuleWrapper)
    #            if index and index < len(self.SbmlRules):
    #                self.SbmlRules.insert(index, wrappedEntity)
    #            else:
    #                self.SbmlRules.append(wrappedEntity)
    #
    #        self.Dirty = True
    #        self.structuralChange()



    def removeEntity(self, sbmlObject):
        '''
        Removes the given SBMLEntity from the corresponding internal list.
        '''
        if type(sbmlObject.Item) is libsbml.Species:
            # remove from Wrapper entity (essential for the TreeModel)
            index = sbmlObject.getIndex()
            self.SpeciesWrapper.removeChild(index)

            # remove internal references
            self.SbmlSpecies.remove(sbmlObject)
            self.dictOfSpecies.pop(sbmlObject.getId())
            
            # remove from libsbml model
            oldSpecies = self.SbmlModel.Item.removeSpecies(sbmlObject.getId())
            #time.sleep(5)
            if oldSpecies:
                del oldSpecies
                #time.sleep(5)
        elif type(sbmlObject.Item) is libsbml.Compartment:
            # remove from Wrapper entity (essential for the TreeModel)
            index = sbmlObject.getIndex()
            self.SpeciesWrapper.removeChild(index)

            self.SbmlCompartments.remove(sbmlObject)
            oldCompartment = self.SbmlModel.Item.removeCompartment(sbmlObject.getId())
            if oldCompartment:
                del oldCompartment
        elif type(sbmlObject.Item) is libsbml.Reaction:
            # remove from Wrapper entity (essential for the TreeModel)
            index = sbmlObject.getIndex()
            self.ReactionWrapper.removeChild(index)

            for reactionTuple in self.SbmlReactions:
                if reactionTuple[0] == sbmlObject:
                    self.SbmlReactions.remove(reactionTuple)
            oldReaction = self.SbmlModel.Item.removeReaction(sbmlObject.getId())
            if oldReaction:
                del oldReaction
        elif type(sbmlObject.Item) is libsbml.Parameter:
            # remove from Wrapper entity (essential for the TreeModel)
            index = sbmlObject.getIndex()
            self.ParameterWrapper.removeChild(index)

            self.SbmlParameters.remove(sbmlObject)
            self.SbmlModel.Item.removeParameter(sbmlObject.getId())
        elif type(sbmlObject.Item) is libsbml.RateRule:
            # remove from Wrapper entity (essential for the TreeModel)
            index = sbmlObject.getIndex()
            self.RateRuleWrapper.removeChild(index)

            self.SbmlRateRules.remove(sbmlObject)
            oldRateRule = self.SbmlModel.Item.removeRule(sbmlObject.getId())
            if oldRateRule:
                del oldRateRule
        elif type(sbmlObject.Item) is libsbml.AssignmentRule:
            # remove from Wrapper entity (essential for the TreeModel)
            index = sbmlObject.getIndex()
            self.AssignmentRuleWrapper.removeChild(index)

            self.SbmlAssignmentRules.remove(sbmlObject)
            oldAssignmentRule = self.SbmlModel.Item.removeRule(sbmlObject.getId())
            if oldAssignmentRule:
                del oldAssignmentRule
#            del sbmlObject # can't do this here; object is still needed to identify references elsewhere
        elif type(sbmlObject.Item) is libsbml.AlgebraicRule:
            # remove from Wrapper entity (essential for the TreeModel)
            index = sbmlObject.getIndex()
            self.AlgebraicRuleWrapper.removeChild(index)

            self.SbmlAlgebraicRules.remove(sbmlObject)
            oldAlgebraicRule = self.SbmlModel.Item.removeRule(sbmlObject.getId())
            if oldAlgebraicRule:
                del oldAlgebraicRule

        self.Dirty = True
        self.on_structuralChange(sbmlObject, CHANGETYPE.REMOVE)
        del sbmlObject  # seems to work
        # TODO: What happens if the above line might be called within a thread?

    def on_structuralChange(self, entity, changeType):
        if changeType == CHANGETYPE.CHANGE_REACTANTS:
            self.updateReaction(entity)
        elif changeType == CHANGETYPE.CHANGE_PRODUCTS:
            self.updateReaction(entity)
        elif changeType == CHANGETYPE.CHANGE_MODIFIERS:
            self.updateReaction(entity)
        self.on_structuralChange.emit(entity, changeType)





    #@Slot("SBMLEntity, bool")
    def sbml_entity_selection_changed(self, value):
        """
        Helper method to emit a Signal when any entity selection state
        has changed.

        @param entity: A SBMLEntity whose selection state has changed.
        @type entity: SBMLEntity

        @param value: New value of the selection state
        @type value: bool
        """
        entity = QObject.sender()
        self.selectionChange.emit(entity, value)

    def save(self, filename=None):
        """
        Save the current SBML data to a SBML file.
        If no filename is given, the current file will be overwritten; if
        a filename is given, this method works like a "save as" method + the
        new filename will become the current filename.

        @param filename: Optional filename to save to
        @type filename: str
        """
        if self.SbmlDocument is None:
            logging.info("There currently is no document, so it can't be saved.")
            return
        if filename is not None:
            self.filename = filename  # sets new filename and makes this to a "Save as" action

        try:
            self._updateParameterSetsXml()
        except:
            logging.warning("The existing Parameter Sets could not be saved. The model will be saved without them.")

        try:
            self._commitActiveParamSetToModel()
        except :
            logging.warning(
                "Could not commit the values of the active Parameter Set to the Model. Parameter values will be out-of-date if the model is opened in another SBML tool.")

        writer = libsbml.SBMLWriter()
        try:
            logging.info("Saving file %s" % self.filename)
            writer.writeSBML(self.SbmlDocument.Item, str(self.filename)) # unicode string is a problem
        except Exception, e:
            logging.error("Could not save SBML file: %s" % e)

            #    def save_compartments(self, compartments, filename = None):
            #        '''
            #        '''
            #        listOfCompartments = self.SbmlModel.getListOfCompartments()
            #        for oldCompartment in listOfCompartments:
            #            self.SbmlModel.removeCompartment(oldCompartment.getId())
            #
            #        self.SbmlCompartments = compartments
            #        for newCompartment in self.SbmlCompartments:
            #            self.SbmlModel.addCompartment(newCompartment)
            #
            #        self.save(filename)

    def dirty_changed(self, value):
        '''
        Small helper method, called when crucial data has changed.
        '''
        self.Dirty = value

    @Slot(QModelIndex, QModelIndex)
    def dataChanged(self, index1, index2):
        '''
        C++: void dataChanged(const QModelIndex&,const QModelIndex&)
        '''
        self.Dirty = True

        # Really do it this way? It's very general and does not only fire when Products/Reactants are changed.

    #        entity = index1.internalPointer()
    #        if entity.Type == sbml_entities.TYPE.REACTION:
    #            # A Reaction has been changed. Possibly, the Products/Reactants
    #            # are affected. The graph around this needs to be rebuilt.
    #            print entity.Item

    #    def selectionChange(self, sbmlEntity, value):
    #        if type(sbmlEntity.Item) is Species:
    #            row = self.SbmlSpecies.index(sbmlEntity.Item)
    #            self.SpeciesTableModel.setData(row, value, Qt)
    ##            type = "species"
    #
    ##        self.emit(SIGNAL("selectionChange(str, int)", type, row)

    def getId(self):
        '''
        Convenience method to get the ID of the current model.
        
        @return: ID of current model
        @rtype: str
        '''
        return self.SbmlModel.getId()

    def wrapCompartments(self):
        logging.info("\nNumber of compartments: %i" % self.SbmlModel.Item.getNumCompartments())
        listOfCompartments = self.SbmlModel.Item.getListOfCompartments()
        self.SbmlCompartments = []
        for compartment in listOfCompartments:
            logging.info("Compartment: %s" % compartment.getName())
            self.SbmlCompartments.append(self.createSBMLEntity(compartment, parent=self.CompartmentWrapper))

    def wrapSpecies(self):
        logging.info("\nNumber of species: %i" % self.SbmlModel.Item.getNumSpecies())
        listOfSpecies = self.SbmlModel.Item.getListOfSpecies()
        self.SbmlSpecies = []
        self.dictOfSpecies = {}
        for species in listOfSpecies:
            logging.info("Species: %s" % species.getName())
            wrappedSpecies = self.createSBMLEntity(species, parent=self.SpeciesWrapper)
            self.SbmlSpecies.append(wrappedSpecies)
            self.dictOfSpecies[species.getId()] = wrappedSpecies

    def wrapGlobalParameters(self):
        logging.info("\nNumber of global parameters: %i" % self.SbmlModel.Item.getNumParameters())
        listOfParameters = self.SbmlModel.Item.getListOfParameters()
        self.SbmlParameters = []
        self.dictOfParameters = {}
        for param in listOfParameters:
            logging.info("Parameter: %s\t%s" % (param.getId(), param.getName()))
            wrappedParam = self.createSBMLEntity(param, parent=self.ParameterWrapper)
            self.SbmlParameters.append(wrappedParam)
            self.dictOfParameters[param.getId()] = wrappedParam

    def wrapReactions(self):
        listOfReactions = self.SbmlModel.Item.getListOfReactions()
        logging.info("\nNumber of reactions: %i" % len(listOfReactions))
        self.SbmlReactions = []
        numLocalParamsTotal = 0 # we will also go through all reactions and get their local parameters
        for reaction in listOfReactions:
            logging.info("Reaction: %s" % reaction.getName())

            reactantReferences = reaction.getListOfReactants()
            productReferences = reaction.getListOfProducts()

            if reactantReferences == None or len(reactantReferences) == 0:
                logging.error("A Reaction's reactant references should never be empty at this point.")

            reactants = [self.dictOfSpecies[reactantReference.getSpecies()] for reactantReference in reactantReferences]

            if productReferences == None or len(productReferences) == 0:
                logging.error("A Reaction's product references should never be empty at this point.")

            products = [self.dictOfSpecies[productReference.getSpecies()] for productReference in productReferences]




            #note: both list already contain the wrapped entities
            self.SbmlReactions.append((self.createSBMLEntity(reaction, parent=self.ReactionWrapper), reactants,
                                       products)) # makes it easier to get to reactants and products later on

            # handle local params
            if reaction.isSetKineticLaw():
                kineticLaw = reaction.getKineticLaw()
                numLocalParams = kineticLaw.getNumParameters()
                for i in xrange(numLocalParams):
                    param = kineticLaw.getParameter(i)
                    logging.info("Parameter: %s\t%s" % (param.getId(), param.getName()))
                    logging.debug("Parent %s" % param.getParentSBMLObject().getParentSBMLObject())
                    wrappedParam = self.createSBMLEntity(param, parent=self.ParameterWrapper)
                    self.SbmlParameters.append(wrappedParam)
                    self.dictOfParameters[param.getId()] = wrappedParam
                    numLocalParamsTotal += 1

        logging.info("\nNumber of local parameters: %i" % numLocalParamsTotal)

    def prepareReactions(self):
        listOfReactions = self.SbmlModel.Item.getListOfReactions()
        logging.info("\nPreparing Reactions (by creating implicit Species)")
        for reaction in listOfReactions:
            self.checkReactionSpecies(reaction)

    def wrapRules(self):
        numOfRules = self.SbmlModel.Item.getNumRules()
        logging.info("\nNumber of rules: %i" % numOfRules)
        listOfRules = self.SbmlModel.Item.getListOfRules()
        self.SbmlRateRules = []
        self.dictOfRateRules = {}
        self.SbmlAlgebraicRules = []
        self.dictOfAlgebraicRules = {}
        self.SbmlAssignmentRules = []
        self.dictOfAssignmentRules = {}
        for rule in listOfRules:
            logging.info("Rule: %s\t%s" % (rule.getId(), rule.getName()))
            if rule.isAlgebraic():
                wrappedRule = self.createSBMLEntity(rule, parent=self.AlgebraicRuleWrapper)
                self.SbmlAlgebraicRules.append(wrappedRule)
                self.dictOfAlgebraicRules[rule.getId()] = wrappedRule
            elif rule.isAssignment():
                wrappedRule = self.createSBMLEntity(rule, parent=self.AssignmentRuleWrapper)
                self.SbmlAssignmentRules.append(wrappedRule)
                self.dictOfAssignmentRules[rule.getId()] = wrappedRule
            elif rule.isRate():
                wrappedRule = self.createSBMLEntity(rule, parent=self.RateRuleWrapper)
                self.SbmlRateRules.append(wrappedRule)
                self.dictOfRateRules[rule.getId()] = wrappedRule


    def wrapEvents(self):
        numEvents = self.SbmlModel.Item.getNumEvents()
        logging.info("\nNumber of Events: %i" % numEvents)
        listOfEvents = self.SbmlModel.Item.getListOfEvents()
        self.SbmlEvents = []
        for event in listOfEvents:
            logging.info("Event: %s\t%s" % (event.getId(), event.getName()))
            wrappedEvent = self.createSBMLEntity(event, parent=self.EventsWrapper)
            self.SbmlEvents.append(wrappedEvent)


    #def createReactants(self, reaction):

    def checkReactionSpecies(self, reaction):
        """
        Checks whether the given Reaction has Reactants/Products. If either
        one is missing, it's created and added to the Reaction.

        @param reaction: A libSBML Reaction
        @type reaction: libsbml.Reaction
        """
        reactantReferences = reaction.getListOfReactants()
        productReferences = reaction.getListOfProducts()

        if reactantReferences == None or len(reactantReferences) == 0:
            self.newSpeciesCount += 1

            newSpecies = self.SbmlModel.Item.createSpecies()
            newSpecies.setId("helper_%s" % self.newSpeciesCount)

            newSpecies.setName("helper_%s" % self.newSpeciesCount)
            newSpecies.setInitialConcentration(0)
            newSpecies.setBoundaryCondition(True)    # so, no ODE will be generated for this (virtual) Species
            #newSpecies.setName("Auto-generated Species as Reactant in Reaction " + reaction.getId())

            #try to set the correct Compartment
            try:
                if productReferences and len(productReferences) > 0:    #should always be the case
                    productReference = productReferences[0]
                    #productSpecies = self.dictOfSpecies[productReference.getSpecies()]
                    productSpecies = self.SbmlModel.Item.getSpecies(productReference.getSpecies())
                    compartmentId = productSpecies.getCompartment()
                    newSpecies.setCompartment(compartmentId)
            except:
                logging.debug(
                    "SbmlMainModel.checkReactionSpecies(): Could not set the correct Compartment for helper Species %s." % "helper_%s" % self.newSpeciesCount)

            newSpeciesRef = reaction.createReactant()
            newSpeciesRef.setSpecies(newSpecies.getId())

        if productReferences == None or len(productReferences) == 0:
            self.newSpeciesCount += 1

            newSpecies = self.SbmlModel.Item.createSpecies()
            newSpecies.setId("helper_%s" % self.newSpeciesCount)
            newSpecies.setName("helper_%s" % self.newSpeciesCount)
            newSpecies.setInitialConcentration(0)
            newSpecies.setBoundaryCondition(True)    # so, no ODE will be generated for this (virtual) Species
            #newSpecies.setName("Auto-generated Species Product in Reaction " + reaction.getId())

            #try to set the correct Compartment
            try:
                if reactantReferences and len(reactantReferences) > 0:    #should always be the case
                    reactantReference = reactantReferences[0]
                    #reactantSpecies = self.dictOfSpecies[reactantReference.getSpecies()]
                    reactantSpecies = self.SbmlModel.Item.getSpecies(reactantReference.getSpecies())
                    compartmentId = reactantSpecies.getCompartment()
                    newSpecies.setCompartment(compartmentId)
            except:
                logging.debug(
                    "SbmlMainModel.checkReactionSpecies(): Could not set the correct Compartment for helper Species %s." % "helper_%s" % self.newSpeciesCount)

            newSpeciesRef = reaction.createProduct()
            newSpeciesRef.setSpecies(newSpecies.getId())

        logging.info("%s implicit Species created." % self.newSpeciesCount)


    def updateReaction(self, reactionWrapper):
        """
        Gets an updated Reaction and updates all relevant references (like
        the reaction tuple).

        The new actual reactant/product references *inside* the ReactionWrapper (and thus, the
        libsbml.Reaction) have already been set. The references in the self.SbmlReactions tuple remain.
        """
        listIDTobeRemoved = None
        tupleToBeAdded = None

        for (i, (currentReactionWrapper, reactants, products)) in enumerate(self.SbmlReactions):
            if reactionWrapper == currentReactionWrapper:
                reaction = reactionWrapper.Item
                logging.info("Updating Reaction: %s" % reaction.getName())

                # the current (new) references
                reactantReferences = reaction.getListOfReactants()
                productReferences = reaction.getListOfProducts()

                if reactantReferences == None or len(reactantReferences) == 0:
                    logging.error("A Reaction's reactant references should never be empty at this point.")

                reactants = [self.dictOfSpecies[reactantReference.getSpecies()] for reactantReference in
                             reactantReferences]

                if productReferences == None or len(productReferences) == 0:
                    logging.error("A Reaction's product references should never be empty at this point.")

                products = [self.dictOfSpecies[productReference.getSpecies()] for productReference in productReferences]

                tupleToBeAdded = (reactionWrapper, reactants, products)
                listIDTobeRemoved = i
                break   # break out of the for loop

                #note: both list already contain the wrapped entities
                #self.SbmlReactions.append((self.createSBMLEntity(reaction, parent=self.ReactionWrapper), reactants, products)) # makes it easier to get to reactants and products later on

                # TODO: Maybe this is needed later, when the actual kinetic can be changed in the UI
                # handle local params
                #                if reaction.isSetKineticLaw():
                #                    kineticLaw = reaction.getKineticLaw()
                #                    numLocalParams = kineticLaw.getNumParameters()
                #                    for i in xrange(numLocalParams):
                #                        param = kineticLaw.getParameter(i)
                #                        logging.info("Parameter: %s\t%s" % (param.getId(), param.getName()))
                #                        logging.debug("Parent %s" % param.getParentSBMLObject().getParentSBMLObject())
                #                        wrappedParam = self.createSBMLEntity(param, parent=self.ParameterWrapper)
                #                        self.SbmlParameters.append(wrappedParam)
                #                        self.dictOfParameters[param.getId()] = wrappedParam
                #                        numLocalParamsTotal += 1

        self.SbmlReactions.pop(i)
        self.SbmlReactions.append(tupleToBeAdded)

    def createDefaultParameterSet(self):
        """
        If no Parameter Set exists, one is created with the Model's Parameter values. This serves as default set,
        as a possible fallback set and gives the option to revert Model Parameters to their "on load" values.

        If one or more Sets exist, this method checks if the Model's Parameter values are identical to all the values
        in one of the Sets. If so, this set is used as default set.  If not, a new default set with the Model's parameter
        values is created.
        """

        if self.ListOfParameterSets and len(self.ListOfParameterSets) > 0:
            # check if it contains a Set that is identical to the data within the model
            paramsInModel = {}
            for sbmlParam in self.SbmlParameters:
                value = sbmlParam.Item.getValue()
                combinedId = sbmlParam.getCombinedId()
                paramsInModel[combinedId] = value
            for parSet in self.ListOfParameterSets:
                if len(self.SbmlParameters) != len(parSet):
                    continue    # this can't be a matching Set, number of Parameters don't match

                allParamValuesIdentical = True
                for combinedId, parProxy in parSet.items():
                #                    id = parProxy.getId()
                #                    reactionId = parProxy.getReactionId()
                    valueInSet = parProxy.getValue()

                    #                    combinedId = id if not reactionId else "%s_%s" % (reactionId, id)
                    if paramsInModel.has_key(combinedId):
                        valueInModel = paramsInModel[combinedId]
                        #compare strings due to loss of precision once floats have been saved to XML
                        # todo: use python's decimal library for exact representations?
                        if str(valueInModel) != str(valueInSet):
                            allParamValuesIdentical = False
                            break
                    else:   # if the Set describes a Parameter that is not in the Model
                        continue

                if allParamValuesIdentical: # reached if a whole Set is iterated through without encountering a wrong value
                    return  # just return; we don't need to create the Set with default values



        # Simplest case: just create a new ParameterSet with the just loaded model param values.
        # This is reached when no fitting Set was found.
        newSet = ParameterSet(PARAM_SET_ORIGINAL)
        for sbmlParam in self.SbmlParameters:
            id = sbmlParam.getId()
            value = sbmlParam.Item.getValue()
            reactionId = sbmlParam.getScope()
            combinedId = sbmlParam.getCombinedId()
            if reactionId == "Global":
                newSet.add(combinedId, id, value)
            else:
                newSet.add(combinedId, id, value, reactionId=reactionId)

        if self.ListOfParameterSets:
            self.ListOfParameterSets.append(newSet)
        else:
            self.ListOfParameterSets = ListOfParameterSets(newSet)
            #            self.ListOfParameterSets.append(newSet)


    def getValueFromActiveSet(self, id):
        """
        Returns the value of the given Paramter (by ID) within the currently
        active Parameter Set.
        """
        try:
            paramProxy = self.ListOfParameterSets.activeSet.getParam(id)
            return paramProxy.getValue()
        except Exception, e:
            logging.debug("SbmlMainmodel.getValueFromActiveSet(): Can't get value. Error: %s" % e)
            return

    def _updateParameterSetsXml(self):
        """
        Goes through the currently existing Parameter Sets and adds them to the SBML Model as annotation
        so that the model can natively save them as XML within the SBML file.
        """

        rootNodeNeedsToBeAdded = False
#        if not self.paramSetsListNode:
        # testing a change: *Always* create the ParamSetsList Node anew. Should solve problems
        # with duplicate Sets.

        # But: We have to remove the "old" ParamSetsList from the Model's XML annotations

        annotationRootNode = self.SbmlModel.Item.getAnnotation()    # returns a libsbml.XMLNode
        paramSetsListNodeIndex = annotationRootNode.getIndex(XML_LIST_OF_PARAMETER_SETS)
        if paramSetsListNodeIndex != -1:
            annotationRootNode.removeChild(paramSetsListNodeIndex)

        #creating the main list
        parListTriplet = libsbml.XMLTriple(XML_LIST_OF_PARAMETER_SETS, XML_NAMESPACE_PARAMETER_SETS, "")
        parListAttribute = libsbml.XMLAttributes()
        parListAttribute.add(XML_LIST_OF_PARAMETER_SETS_ACTIVE, self.ListOfParameterSets.activeSet.getId())

        self.paramSetsListNode = libsbml.XMLNode(parListTriplet, parListAttribute)

        namespaces = libsbml.XMLNamespaces()
        namespaces.add(XML_NAMESPACE_PARAMETER_SETS)
        self.paramSetsListNode.setNamespaces(namespaces)

        rootNodeNeedsToBeAdded = True

        for paramSet in self.ListOfParameterSets:
            id = paramSet.getId()
            name = paramSet.getName()
            parSetTriplet = libsbml.XMLTriple(XML_PARAMETER_SET)
            parSetAttributes = libsbml.XMLAttributes()
            parSetAttributes.add(XML_PARAMETER_SET_ID, str(id))
            parSetAttributes.add(XML_PARAMETER_SET_NAME, str(name))
            parSetNode = libsbml.XMLNode(parSetTriplet, parSetAttributes)

            for combinedId, paramProxy in paramSet._listOfParameters.items():
                sbmlId = paramProxy.getId()
                value = paramProxy.getValue()
                reactionId = paramProxy.getReactionId()
                parProxyTriplet = libsbml.XMLTriple(XML_PARAMETER)
                parProxyAttributes = libsbml.XMLAttributes()
                parProxyAttributes.add(XML_PARAMETER_SBML_ID, str(sbmlId))
                parProxyAttributes.add(XML_PARAMETER_VALUE, str(value))
                if reactionId:
                    parProxyAttributes.add(XML_PARAMETER_REACTION_ID, str(reactionId))
                parProxyNode = libsbml.XMLNode(parProxyTriplet, parProxyAttributes)

                parSetNode.addChild(parProxyNode)

            self.paramSetsListNode.addChild(parSetNode)    # adds a copy, so do this at the end

        if rootNodeNeedsToBeAdded:
            self.SbmlModel.Item.appendAnnotation(
                self.paramSetsListNode)    # self.paramSetsListNode is copied; no reference; so, do this at the end
            # storing in self.paramSetsListNode might make no sense at this point because it's not saved as reference

    def _loadParameterSets(self):
        """
        Parses through all Parameter Sets in the model's annotation and brings them into memory
        as a ListOfParameterSet
        s.
        """
        model = self.SbmlModel.Item

        if not model.isSetAnnotation():
            return # no annotations in Model

        annotationRootNode = self.SbmlModel.Item.getAnnotation()    # returns a libsbml.XMLNode
        self.paramSetsListNode = annotationRootNode.getChild(XML_LIST_OF_PARAMETER_SETS)
        if self.paramSetsListNode.isEOF():
            self.paramSetsListNode = None
            return  # no ListOfParameterSets annotation in model

        #listAttributes = paramSetsListNode.getAttributes()
        namespace = self.paramSetsListNode.getNamespaceURI()
        if namespace != XML_NAMESPACE_PARAMETER_SETS:
            logging.warning("The model defines a parameter set list but uses the wrong namespace: %s" % namespace)

        if self.paramSetsListNode.hasAttr(XML_LIST_OF_PARAMETER_SETS_ACTIVE):
            activeSetId = self.paramSetsListNode.getAttrValue(XML_LIST_OF_PARAMETER_SETS_ACTIVE)
        else:
            logging.warning("The model defines a parameter set list without defining an active set.")
            activeSetId = None

        # create the List (this is the object that's actually used throughout BioPARKIN)
        self.ListOfParameterSets = ListOfParameterSets()
        #        if activeSetId:
        #            self.ListOfParameterSets.activeSet = activeSetId

        # iterating over parameter sets
        numSets = self.paramSetsListNode.getNumChildren()
        for i in xrange(numSets):
            parSetNode = self.paramSetsListNode.getChild(i)
            id = parSetNode.getAttrValue(XML_PARAMETER_SET_ID) # returns "" if not set
            name = parSetNode.getAttrValue(XML_PARAMETER_SET_NAME) # returns "" if not set

            parSet = ParameterSet(id, name=name)
            self.ListOfParameterSets.append(parSet)

            if activeSetId == id:
                self.ListOfParameterSets.activeSet = parSet

            # iterate over parameters in that set
            numParams = parSetNode.getNumChildren()
            for j in xrange(numParams):
                parNode = parSetNode.getChild(j)
                sbmlId = parNode.getAttrValue(XML_PARAMETER_SBML_ID)
                value = float(parNode.getAttrValue(XML_PARAMETER_VALUE))
                reactionId = parNode.getAttrValue(XML_PARAMETER_REACTION_ID)

                combinedId = sbmlId if not reactionId else "%s_%s" % (reactionId, sbmlId)

                parProxy = ParameterProxy(combinedId, sbmlId, value, reactionId)
                parSet[combinedId] = parProxy


    def createParameterSetForFit(self):
        """
        Duplicate the "Original" Parameter Set so that there is
        a designated set for use with parameter identification.

        The user could easily create such a set himself. This is just
        for convenience and an improved UX.
        """
        # check if such a set already exists
        if self.ListOfParameterSets:
            for paramSet in self.ListOfParameterSets:
                if paramSet.getId() == PARAM_SET_INITIAL_GUESS:
                    logging.debug("SbmlMainModel.createParameterSetForFit(): Initial Guess set already exists. No need to create one.")
                    return

            originalSet = self.ListOfParameterSets.getSet(PARAM_SET_ORIGINAL)
            guessSet = ParameterSet(PARAM_SET_INITIAL_GUESS, baseSet=originalSet, duplicate=True)
            self.ListOfParameterSets.activeSet = guessSet
            self.ListOfParameterSets.append(guessSet)
        else:
            logging.debug("No self.ListOfParameterSets in SbmlMainModel. This should not happen.")

    def createParameterSetWithFittedValues(self, dataSet):
        """
        Given the results of a parameter identification run, this method
        creates a Parameter Set with the computed values.
        This is for the convenience of the user so that he may immediately
        compute a plot with the identified values.
        """
#        originalSet = self.ListOfParameterSets.getSet(PARAM_SET_ORIGINAL)
        activeSet = self.ListOfParameterSets.getActiveSet()

        fitSet = ParameterSet(PARAM_SET_FIT, baseSet=activeSet, duplicate=True)

        for id, entityData in dataSet.data.items(): # one entityData per estimated param
            try:
                value = float(entityData.datapoints[0])
            except:
                value = float("nan")

            combinedId = entityData.sbmlEntity.getCombinedId()
            paramProxy = fitSet.getParam(combinedId)
            if paramProxy:
                paramProxy.setValue(value)
                
        self.ListOfParameterSets.append(fitSet) # also emits change signal
        self.ListOfParameterSets.activeSet = fitSet


#    def _handleScalingValues(self):
#        """
#        Inovkes methods to:
#          - Parse scaling values from XML (self._loadScalingValues) for Species and Parameters
#          - Set values for Species (self._setScalingValuesSpecies)
#          - Set values for Parameters (self._setScalingValuesParameters)
#        """
#        self._loadScalingValues()
#        self._setScalingValuesSpecies()
#        self._setScalingValuesParameters()
#
#    def _loadScalingValues(self):
#
#        for speciesEntity in self.SbmlSpecies:
#            species = speciesEntity.Item
#            if not species.isSetAnnotation():
#                continue
#
#            annotationRootNode = species.getAnnotation()
#            scaleNode = annotationRootNode.getChild(XML_SCALE)
#            if scaleNode.isEOF():
#

#        model = self.SbmlModel.Item
#
#        if not model.isSetAnnotation():
#            return # no annotations in Model
#
#        annotationRootNode = self.SbmlModel.Item.getAnnotation()    # returns a libsbml.XMLNode
#        self.paramSetsListNode = annotationRootNode.getChild(XML_LIST_OF_PARAMETER_SETS)
#        if self.paramSetsListNode.isEOF():
#            self.paramSetsListNode = None
#            return  # no ListOfParameterSets annotation in model
#
#        #listAttributes = paramSetsListNode.getAttributes()
#        namespace = self.paramSetsListNode.getNamespaceURI()
#        if namespace != XML_NAMESPACE_PARAMETER_SETS:
#            logging.warning("The model defines a parameter set list but uses the wrong namespace: %s" % namespace)
#
#        if self.paramSetsListNode.hasAttr(XML_LIST_OF_PARAMETER_SETS_ACTIVE):
#            activeSetId = self.paramSetsListNode.getAttrValue(XML_LIST_OF_PARAMETER_SETS_ACTIVE)
#        else:
#            logging.warning("The model defines a parameter set list without defining an active set.")
#            activeSetId = None

    def on_entityIdChanged(self, entity, newId, oldId):
        """
        Slot that should be invoked whenever the ID of some
        SBMLEntity is changed.
        This can be used to ensure that references within this class are
        up-to-date (e.g. self.dictOfSpecies uses the IDs as keys).

        Currently, this is only used for Species IDs.
        """
        if entity.Type == sbml_entities.TYPE.SPECIES:
            self.dictOfSpecies.pop(oldId)
            self.dictOfSpecies[newId] = entity

    def _commitActiveParamSetToModel(self):
        """
        Goes through the active Parameter Set (if there is one)
        and "commits" its Parameter values to the "real" Parameter
        entities of the model.
        BioPARKIN doesn't use the Parameter entity values (except
        if there is not yet any Parameter Set) but other software
        uses these values.
        """
        if not self.ListOfParameterSets:
            raise Exception("There is no current list of Parameter Sets.")


        # prepare access to model params
        modelParams = {}
        for paramEntity in self.SbmlParameters:
            modelParams[paramEntity.getCombinedId()] = paramEntity

        activeSet = self.ListOfParameterSets.getActiveSet()
        for combinedId in activeSet.getParamIds():
            param = activeSet.getParam(combinedId)
            activeValue = param.getValue()
            reactionId = param.getReactionId()
            id = param.getId()

            modelParam = modelParams[combinedId]
            modelParam.setValue(activeValue)

        
