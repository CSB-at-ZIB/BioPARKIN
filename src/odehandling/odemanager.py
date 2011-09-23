from backend.exceptions import InitError
from odehandling.odewrapper import ODEWrapper
from odehandling.parameterwrapper import ParameterWrapper
from odehandling.specieswrapper import SpeciesWrapper
from odehandling.odegenerator import ODEGenerator
from odehandling.reactionwrapper import ReactionWrapper
from odehandling.assignmentrulewrapper import AssignmentRuleWrapper
from odehandling.compartmentwrapper import CompartmentWrapper
from services.dataservice import DataService


class ODEManager(object):
    '''
    This manager handles ODE objects and provides
    some information (e.g. number of equations, etc.)
    which are needed by computation backends.
    
    This class is thought as a kind of container which has useful
    references but no (or only little) logic. 
    
    
    @since: 2010-04-21
    '''
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, mainModel):
        '''
        Just init with empty variables. They will be set from the outside.
        '''
        
        self.mainModel = mainModel
        #self.mode = mode # None is the default mode == MODE_INTEGRATE

        # "interface" definition
        self.projectId = mainModel.getId() #TODO: Sanitize string
        self.odeList = []
        self.parameterList = []
        self.speciesList = []
        self.odeDefiningSpeciesList = []
        self.reactionList = []
        self.compartmentList = []
        self.assignmentRuleList = []
        
        self.experimentalDataFilename = None    # TODO: Set!

        self.parameterSet = self.mainModel.ListOfParameterSets.activeSet

        # these can be computed once variables are set
        self.odeCount = -1
        self.parameterCount = -1
        self.entityCount = -1
        #self.tObservedCount = -1
        self.timepointList = []
        self.measuredTimepointList = []    # union of all loaded Sensitivity Timepoints

        # these have to be given (for now)
        
        ### deprecated ###
        #self.maxNumOfDenseOutput = 0    #number of delayed functions?
        #self.odeDelayCount = 0
        #self.tMax = 1
        ##################
        
        self.intervalCount = None
        self.measuredTimepointCount = None
        
        self.startTime = None
        self.endTime = None
        
        self.rtol = None    # relative tolerance for integrator
        self.atol = None    # absolute tolerance for integrator
        self.xtol = None    # required tolerance for gauss newton
        self.globalParamStdDeviation = None

        self.useMeasuredTimepoints = False
        
    
    def init(self):
        '''
        Public init method which is to be called after settings (start/end time
        etc.) have been set.
        '''
        self.createEntities()
        self.initValues()
    
    def createEntities(self):
        '''
        Creates wrapped ODEs (class ODEWrapper), wrapped Parameters, and
        wrapped Species. Entities are wrapped so that the templates can access
        their properties in a defined way.
        
        ODEs are wrapped by wrapping RateRules and by creating ODEs from
        the reaction network (using ODEGenerator).
        '''
        
        # TODO: Replace this wrapping by using the original SBMLEntities
        
        # for every Reaction and every (Rate)Rule, create a ODE wrapper
        reactionIndex = 1
        for reaction in self.mainModel.SbmlReactions:
            reactionWrapper = ReactionWrapper(reaction[0].Item, reactionIndex, mainModel=self.mainModel)
            self.reactionList.append(reactionWrapper)
            reactionIndex += 1 
        
        
        index = 1
        odeGenerator = ODEGenerator(self.mainModel)
        for odeWrapper in odeGenerator.wrappedODEs:
            #if not odeWrapper.hasError and not odeWrapper.id.startswith("helper"):
            if odeWrapper.isValid():
                odeWrapper.index = index
                self.odeList.append(odeWrapper)
                index += 1

        for ruleEntity in self.mainModel.SbmlRateRules:
            # TODO: What about "generated ODE vs RateRule"? Overwrite generated ODE? Might happen inherently because of identical ID in {} in backend
            ode = ODEWrapper(index, mathNode = ruleEntity.Item.getMath(), rule= ruleEntity, mainModel=self.mainModel)
            if ode.isValid():
                self.odeList.append(ode)
                index += 1


        assignmentRuleIndex = 1
        for ruleEntity in self.mainModel.SbmlAssignmentRules:
#            if ruleEntity.Item is libsbml.RateRule:    # only for RateRules?
            rule = AssignmentRuleWrapper(index, mathNode = ruleEntity.Item.getMath(), rule= ruleEntity.Item, mainModel=self.mainModel)
            #if not ode.hasError:
            if rule.isValid():
                self.assignmentRuleList.append(rule)
                assignmentRuleIndex += 1


        speciesCount = 1  # start counting entries (Species, Parameters) from 1, FORTRAN-style
        paramCount = 1
        
        # handle parameters
        for paramEntity in self.mainModel.SbmlParameters:
            param = ParameterWrapper(paramEntity.Item, paramCount)
            if self.parameterSet:
                combinedId = param.getCombinedId()
                paramProxy = self.parameterSet.getParam(combinedId)
                if paramProxy:
                    param.paramProxy = paramProxy
            self.parameterList.append(param)
            paramCount += 1
            
            
        # wrap compartments (handled as if they are Parameters)
        for compartmentEntity in self.mainModel.SbmlCompartments:
            compartmentWrapper = CompartmentWrapper(compartmentEntity.Item, paramCount)
            self.compartmentList.append(compartmentWrapper)
            paramCount += 1
        
        # handle species
        for speciesEntity in self.mainModel.SbmlSpecies:
            #if not speciesEntity.Item.getId().startswith("helper"):
            if speciesEntity.isDefiningOde():

                species = SpeciesWrapper(speciesEntity, speciesCount)
                self.speciesList.append(species)
                speciesCount += 1
            

    def initValues(self):
        '''
        Initialize Values which can be calculated based on intrinsic properties.
        This has to be called after setting self.odeList, etc.
        '''
        self.odeCount = len(self.odeList)
        self.parameterCount = len(self.parameterList) + len(self.compartmentList)
        self.entityCount = self.odeCount + self.parameterCount

        # no more up-front use of timepoints...
        
##        stepSize = (self.endTime - self.startTime) / float(self.intervalCount)
##        time = self.startTime
##        for i in range(self.intervalCount + 1): # +1 because we need intervalCount many steps + the start time
##            self.timepointList.append(time)
##            time = time + stepSize
#        self.timepointList = [self.startTime + j*(self.endTime-self.startTime)/float(self.intervalCount) for j in range(0, self.intervalCount+1)]
#
#        # if sensitivites should be calculated, we need some additional information
#        if self.useMeasuredTimepoints:
#            # get the currently loaded experimental data
#            dataService = DataService()
#            #expData = dataService.get_experimental_data()
#            expData = dataService.get_selected_experimental_data()
#            if not expData:
#                raise InitError("No measurement sets selected.")
#
#            #collect timepoints
#            timepointsSet = set()   # allows no duplicates
#            for dataSetID, dataSet in expData.items():
#                logging.debug("ODEManager: Getting timepoints from %s" % dataSetID)
#                for entityID, entityData in dataSet.getData().items():
#                    for dataDescriptor in entityData.dataDescriptors:
#                        try:
#                            timepoint = float(dataDescriptor)
#                            #if not timepoint in timepointsSet:
#                            timepointsSet.add(timepoint)
#                        except:
#                            continue
#            timepoints = list(timepointsSet)
#            timepoints.sort()
#
#            # self.measuredStartTime = 0 #TODO : Does measuredstarttime = 0 make sense? Not quite, but the approach below is also debatable
#            delta = 0.0
#            nIntervals = len(timepoints) - 1
#            for j in xrange(nIntervals):
#                delta += (timepoints[j+1] - timepoints[j])/float(nIntervals)
#            if delta <= 0.0:
#                delta = 1.0
#
#            timepoints.insert(0, timepoints[0]-delta)
#
#            self.measuredTimepointList = timepoints
#            self.measuredTimepointCount = len(timepoints)
#            self.measuredStartTime = timepoints[0]
#            self.measuredEndTime = timepoints[len(timepoints) - 1]
#
#            #TODO: handling of (measured) timepoints in future version?!?? Urgend RFC, I think...
#            self.startTime = self.measuredStartTime
#            self.endTime = self.measuredEndTime
#            # self.intervalCount = self.measuredTimepointCount - 1







    def setParameterValue(self, paramID, newValue):
        for param in self.parameterList:
            if paramID == param.getCombinedId():
                param.initialValue = newValue

    def getTimepoints(self):
        if self.useMeasuredTimepoints:
            return self.measuredTimepointList
        else:
            return self.timepointList
