from collections import OrderedDict
import logging
import math, time, sys
import libsbml
from basics.logging.stdoutwrapper import StdOutWrapper
import backend
from backend.basebackend import BaseBackend
from backend.exceptions import InitError
from backend import settingsandvalues
import datamanagement.entitydata
from datamanagement.dataset import DataSet
from datamanagement.entitydata import EntityData
from odehandling.odemanager import ODEManager
from odehandling.odewrapper import ODEWrapper
from sbml_model.sbml_entities import SBMLEntity
import services
from services.dataservice import DataService
from services.optionsservice import OptionsService
from parkincpp.parkin import ValueList, StringList, ExpressionMap, ExprTypeMap, BioSystem, Expression, Param, Vector, BioProcessor, Matrix, QRconDecomp, IOpt, MeasurementPoint, MeasurementList
from parkincpp.parkin import MakeCppOStream

TASK_PARAMETER_IDENTIFICATION = "task_parameter_identification"
TASK_SENSITIVITY_OVERVIEW = "task_sensitivity_overview"
TASK_SENSITIVITIES_DETAILS = "task_sensitivites_details"

class ParkinCppBackend(BaseBackend):
    """
    This class uses the SWIG-wrapped PARKINcpp library to do computations.

    It is used to do:
        - Simple (forward) integration
        - Compute sensitivites (and subconditions)
        - Identify Parameters ("Fit") based on experimental data
        - Manage experimental and simulation data
        - Invoke plots and result tables
        - Manage Parameter Sets
        - Manage/Show/Edit Species and Parameter values.

    TODO (big one): Refactor this class and split it up in meaningful functional units. As it is,
    it is much too large.

    @since: 2010-12-17
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self):
        """
        Do parameterless initialization here.

        Mostly, set up lots of class variables.
        """
        super(ParkinCppBackend, self).__init__()

        logging.info("Loading PARKINcpp library interface...")

        self.selectedParams = None

        self.mainModel = None
        self.settings = None
        self.odeManager = None
        self.bioSystem = None
        self.bioProcessor = None

        self.rawSimResultVector = None
        self.timepoints = None
        self.timepointsPruned = None
        self.sensitivityTimepoints = None
        self.sensitivityTrajectoryMap = None

        self.paramToSensitivityMap = OrderedDict()
        self.parameterSensitivity = None
        self.speciesParameterSensitivity = None
        self.paramToEstimateMap = OrderedDict()

        # we set lots of variables as class variables because they might otherwise go out of scope (in Python)
        # when passed to SWIG-generated interfaces...
        self.sensitivityTimepoints = None
        self.sensitivityTimepointsVector = None
        self.timepointVector = None
        self.measurementMapVector = None
        self.breakpoints = None
        self.eventMap = None
        self.paramMap = None
        self.paramThresholdMap = None
        self.speciesThresholdMap = None
        self.iOpt = None

        self.optionsService = OptionsService()
        self.dataService = DataService()

        self.mode = backend.settingsandvalues.MODE_INTEGRATE    # default mode

    def __del__(self):
        self.wait() #blocks this thread until it has finished

    def setMode(self, mode):
        """
        Sets the main computation mode of the backend:
            - C{backend.settingsandvalues.MODE_INTEGRATE}
            - C{backend.settingsandvalues.MODE_SENSITIVITIES_OVERVIEW}
            - C{backend.settingsandvalues.MODE_SENSITIVITIES_DETAILS}
            - C{backend.settingsandvalues.MODE_PARAMETER_ESTIMATION}

        Don't set the mode string "by hand". Use the "constants" defined
        in backend.settingsandvalues!

        @param mode: A mode string
        @type mode: str
        """
        self.mode = mode

    def setSettings(self, settings):
        """
        Set the settings dictionary. Keys are from
        C{backend.settingsandvalues.SETTING_*}.

        @parameter settings: Dictionary with settings
        @type settings: {}
        """
        self.settings = settings

    def setMainModel(self, model):
        """
        Set the reference to the main model that is needed
        everywhere throughout the class.

        @parameter model: Current/active main model
        @type model: L{SBMLMainModel}
        """
        self.mainModel = model

    def setParamsForSensitivity(self, paramMap):
        """
        Method to set the parameters (given a dict) for which the sensitivities are to be calculated
        from the outside.
        """
        self.paramToSensitivityMap = paramMap

    def setParamsForEstimation(self, paramMap):
        """
        Method to set the parameters (given a dict) for which values are to be identified
        from the outside.
        """
        self.paramToEstimateMap = paramMap

    def setTimepointsForDetailedSensitivities(self, timepoints):
        """
        Public method to set the timepoints for which to return
        the detailed sensitivities (e.g. subconditions).

        Has to be called before computing the detailed sensitivities.
        """
        if not timepoints:
            self.timepoints = None
            return

        startTime = self.settings[settingsandvalues.SETTING_STARTTIME]
        endTime = self.settings[settingsandvalues.SETTING_ENDTIME]
        self.sensitivityTimepoints = []
        for timepoint in timepoints:
            if  startTime < timepoint and timepoint <= endTime:
                self.sensitivityTimepoints.append(timepoint)



    def initialize(self, mainModel, settings):
        """
        Do real initialization given a model and settings.

        Before the actual computations are invoked (see self._doSimulation and self._computeSensitivities),
        the ODEManager is generated (and filled with data) and given to self._createBioSystem to create
        a BioParkinCpp BioSystem instance.

        This does not run in a Thread. (self._compute() does)
        """
        if mainModel:
            self.mainModel = mainModel
        if settings:
            self.settings = settings

        if self.mainModel is None or self.settings is None:
            errorMsg = "Can't invoke PARKINcpp library without Model/Settings."
            logging.error(errorMsg)
            raise InitError(errorMsg)

        initStartTime = time.time()

        # Create ODEManager and fill with data
        self.odeManager = self._createOdeManager()

        # create the "bio system" (basically one of the two main PARKINCpp classes for interfacing with BioPARKIN)
        self._createBioSystem()
        self._createBioProcessor()

        initEndTime = time.time()
        timeElapsed = initEndTime - initStartTime
        logging.info("Initialization of PARKINcpp backend took %s seconds" % round(timeElapsed, 2))


    def _compute(self):
        """
        Do not call this directly! Call start() instead. This will run as a thread.

        Invokes computations. Be sure to have set self.mode to the appropriate mode
        (settingsandvalues.MODE_INTEGRATE or one of the sensitivity/parameter estimation modes) first.
        """
        if not self.odeManager:
            errorMsg = "Can't invoke computation. ODEManager has not been set up."
            logging.error(errorMsg)
            raise InitError(errorMsg)

        computeStartTime = time.time()

        # switch to relevant computation mode
        if self.mode == settingsandvalues.MODE_INTEGRATE:
            self.start_progress_report(False, "Starting Integrator...")
            integrationSuccess = self._doSimulation()
            if not integrationSuccess:
                logging.error("Error while integrating.")
                logging.debug("ParkinCppBackend._compute(): Error while integrating.")
                self.stop_progress_report("Could not start integrator.")
                return
            self.stop_progress_report(settingsandvalues.FINISHED_INTEGRATION)    # also emits the finished signal

        elif self.mode == settingsandvalues.MODE_SENSITIVITIES_OVERVIEW:
            self.start_progress_report(False, "Computing Sensitivity Overview...")
            computationSuccess = self._computeSensitivityOverview()
            if not computationSuccess:
                logging.error("Error while computing sensitivity overview.")
                logging.debug("ParkinCppBackend._compute(): Computation of sensitivities returned False.")
                self.stop_progress_report("Error while computing sensitivities.")
                return
            self.stop_progress_report(settingsandvalues.FINISHED_SENSITIVITY_OVERVIEW)    # also emits the finished signal

        elif self.mode == settingsandvalues.MODE_SENSITIVITIES_DETAILS:
            self.start_progress_report(False, "Computing Detailed Sensitivities...")
            computationSuccess = self._computeSensitivityDetails()
            if not computationSuccess:
                logging.error("Error while computing detailed sensitivities.")
                logging.debug("ParkinCppBackend._compute(): Computation of sensitivities returned False.")
                self.stop_progress_report("Error while computing sensitivities.")
                return
            self.stop_progress_report(settingsandvalues.FINISHED_SENSITIVITY_DETAILS)    # also emits the finished signal

        elif self.mode == settingsandvalues.MODE_PARAMETER_ESTIMATION:
            self.start_progress_report(False, "Identifying Parameters...")
            computationSuccess = self._doParameterEstimation()
            if not computationSuccess:
                logging.error("Error while identifying parameters.")
                logging.debug("ParkinCppBackend._compute(): Parameter identification returned False.")
                self.stop_progress_report("Error while identifying parameters. (Did you load experimental data?)")
                return
            self._handleEstimatedParamResults()
            self.stop_progress_report(settingsandvalues.FINISHED_PARAMETER_ESTIMATION)    # also emits the finished signal

        computeEndTime = time.time()
        timeElapsed = computeEndTime - computeStartTime
        logging.info("Computation took %s seconds" % round(timeElapsed, 2))


    def _createOdeManager(self):
        """
        Creates the ODEManager, sets all settings, and calls init() on that object so that the ODEManager
        calculates a number of metrics for later consumption (e.g. when creating the BioModel).
        """
        logging.debug("Creating ODE Manager...")

        self.odeManager = ODEManager(self.mainModel)
        
        # 10.02.14 td: numerical integrator switch
        self.odeManager.odesolver = self.settings[settingsandvalues.SETTING_INTEGRATOR_BACKEND]\
        if settingsandvalues.SETTING_INTEGRATOR_BACKEND in self.settings\
        else settingsandvalues.DEFAULT_INTEGRATOR_BACKEND

        # 04.03.13 td: cubic Hermite interpolation flag
        self.odeManager.cubintflag = self.settings[settingsandvalues.SETTING_USE_CUBIC_HERMITE]\
        if settingsandvalues.SETTING_USE_CUBIC_HERMITE in self.settings\
        else settingsandvalues.DEFAULT_CUBIC_HERMITE

        self.odeManager.startTime = self.settings[settingsandvalues.SETTING_STARTTIME]\
        if settingsandvalues.SETTING_STARTTIME in self.settings\
        else settingsandvalues.DEFAULT_STARTTIME

        self.odeManager.endTime = self.settings[settingsandvalues.SETTING_ENDTIME] if settingsandvalues.SETTING_ENDTIME\
        in self.settings else settingsandvalues.DEFAULT_ENDTIME

        # 29.08.12 td: debug flag for ODE solver: switched on if debugging active via command line switch
        self.odeManager.debugflag = 1 if self.optionsService.getDebug() else 0

        self.odeManager.rtol = self.settings[settingsandvalues.SETTING_RTOL] if settingsandvalues.SETTING_RTOL\
        in self.settings else settingsandvalues.DEFAULT_RTOL

        self.odeManager.atol = self.settings[settingsandvalues.SETTING_ATOL] if settingsandvalues.SETTING_ATOL\
        in self.settings else settingsandvalues.DEFAULT_ATOL

        self.odeManager.xtol = self.settings[settingsandvalues.SETTING_XTOL] if settingsandvalues.SETTING_XTOL\
        in self.settings else settingsandvalues.DEFAULT_XTOL

        self.odeManager.init()
        return self.odeManager


    def _createBioSystem(self):
        """
        Uses the ODEManager to create a system of BioParkinCpp Expression objects
        (+ other data and information).
        """
        if not self.odeManager:
            logging.debug("ParkinCppBackend._createBioSystem invoked without ODEManager.")
            return None

        logging.info("Creating BioSystem...")

        parameter = StringList()
        expressionMap = ExpressionMap()
        typeMap = ExprTypeMap()
        self.bioSystem = BioSystem(float(self.odeManager.startTime), float(self.odeManager.endTime))
        logging.info("Start time: %s" % self.odeManager.startTime)
        logging.info("End time: %s" % self.odeManager.endTime)

        odeSolver = self.odeManager.odesolver
        rTol = float(self.odeManager.rtol)
        aTol = float(self.odeManager.atol)
        xTol = float(self.odeManager.xtol)
        logging.info("INTEGARTOR: %s" % odeSolver)
        logging.info("RTOL: %s" % rTol)
        logging.info("ATOL: %s" % aTol)
        logging.info("PTOL: %s" % xTol)
        if odeSolver==settingsandvalues.OPTIONS_INTEGRATOR_BACKEND[1]: # metan1
            self.bioSystem.setSolver(3)
        elif odeSolver==settingsandvalues.OPTIONS_INTEGRATOR_BACKEND[2]: # dop853
            self.bioSystem.setSolver(2)
        else: # limex
            self.bioSystem.setSolver(1)
        self.bioSystem.setSolverRTol(rTol)
        self.bioSystem.setSolverATol(aTol)
        self.bioSystem.setSystemTol(xTol)

        cflag = int(not self.odeManager.cubintflag)
        self.bioSystem.setSolverInterpolationFlag(cflag)
        logging.info("Cubic Hermite Interpolation: %s" % ("ON" if cflag <= 0 else "OFF"))
        
        dflag = int(self.odeManager.debugflag)
        self.bioSystem.setSolverDebugFlag(dflag)
        logging.info("Monitoring of ODE Solver: %s" % ("OFF" if dflag <= 0 else "ON"))

        # set names / identifies of parameters
        for paramWrapper in self.odeManager.parameterList:
            pID = paramWrapper.getCombinedId()
#            logging.debug("Putting Parameter %s into BioSystem." % pID)
            parameter.push_back(pID)
        for compartmentWrapper in self.odeManager.compartmentList:   # we handle compartments as if they were parameters
            pID = compartmentWrapper.getId()
            parameter.push_back(pID)

        self.bioSystem.setParameters(parameter)


        # set the initial value(s) for ODE system
        for speciesWrapper in self.odeManager.speciesList:
            try:
                value = float(speciesWrapper.getInitialValue())
            except :    # if initial value is None (it probably will be set by an AssignmentRule)
                value = 0
            self.bioSystem.setInitialValue(speciesWrapper.getId(), value)


        # set expressions for ODE system

        # put reactions into the BioSystem (within ExpressionMap)
        substitutionMap = ExpressionMap()

        # AssignmentRules are replaced directly inside reactions
        for assignmentRule in self.odeManager.assignmentRuleList:
            substitutionMap[assignmentRule.getId()] = assignmentRule.mathForBioParkinCpp()

        # Reactions use replaced AssignmentRules and are themselves used for replacing their IDs in ODEs
        for reactionWrapper in self.odeManager.reactionList:
            expression = reactionWrapper.mathForBioParkinCpp(idsToReplace=substitutionMap)
            if expression:
                substitutionMap[reactionWrapper.getId()] = expression

        # Params are used with their combined ID: "scope_id"
        for paramWrapper in self.odeManager.parameterList:
            expression = Expression(paramWrapper.getCombinedId())
            substitutionMap[paramWrapper.getId()] = expression

        # Finally, ODE Expressions are created using all the above substitutions
        for odeWrapper in self.odeManager.odeList:
            expression = odeWrapper.mathForBioParkinCpp(idsToReplace=substitutionMap)
            expressionMap[odeWrapper.getId()] = expression
            if odeWrapper.isDAE():
                typeMap[odeWrapper.getId()] = 2
                logging.info("DAE with ID %s : 0 = %s" % (odeWrapper.getId(), expression))
            else:
                # 09.08.12 td: default value for typeMap within PARKINcpp
                # typeMap[odeWrapper.getId()] = 1
                logging.info("ODE for ID %s = %s" % (odeWrapper.getId(), expression))

        self.bioSystem.setODESystem(expressionMap)
        self.bioSystem.setODETypes(typeMap)

        self._initBioSystemParameters()

        self._setBioSystemEvents()


    def _initBioSystemParameters(self):
        """
        Set initial param values for BioSystem.
        """
        for paramWrapper in self.odeManager.parameterList:
            pID = paramWrapper.getCombinedId()
            initialValue = self.mainModel.getValueFromActiveSet(pID)
            ## initialValue = float(self.mainModel.getValueFromActiveSet(pID))
            self.bioSystem.setParamValue(pID, initialValue)

        for compartmentWrapper in self.odeManager.compartmentList:  #again, handle compartments as parameters
            pID = compartmentWrapper.getId()
            initialSize = compartmentWrapper.getSize()
            self.bioSystem.setParamValue(pID, initialSize)



    def _setBioSystemEvents(self):
        """
        Check if the model defines events.
        Note: we currently only support ONE format for triggers: eq(time, float) where float is an actual float.
        E.g.: eq(time, 10.0)

        Note: We currently only support ONE type of assignment. They have to target a SPECIES. The right hand side,
        the assignment, is arbitrary and will be converted to a PARKINcpp Expression.
        """
        if len(self.mainModel.SbmlEvents) == 0:
            logging.info("Model does not have events. No need to set any.")
            return
        logging.info("Processing SBML Events...")

        errorMsg = "ParkinCppBackend: The only support event trigger has the format: eq(time, float) where float is an actual float. E.g.: eq(time, 10.0)"
        events = OrderedDict()
        events[self.settings[
               settingsandvalues.SETTING_STARTTIME]] = None # kind of a default breakpoint at 0 that we always jump over
        for eventEntity in self.mainModel.SbmlEvents:
            try:
                sbmlEvent = eventEntity.Item
                trigger = sbmlEvent.getTrigger()
                # we currently only support ONE format for triggers: eq(time, float) where float is an actual float
                triggerMathString = libsbml.formulaToString(trigger.getMath())
                errorMsg += "\nThe current trigger is %s" % triggerMathString
                if not triggerMathString.startswith("eq(time,"):
                    errorMsg += "\nThe current trigger is %s" % triggerMathString
                    logging.error(errorMsg)
                    continue
                timeString = triggerMathString.split(",")[1].split(")")[0].strip() # TODO: A RegEx would be nicer
                time = float(timeString)
                if not self.settings[settingsandvalues.SETTING_STARTTIME] < time < self.settings[settingsandvalues.SETTING_ENDTIME]:
                    logging.info("Event ID %s at timepoint %s is out of integration interval." % (sbmlEvent.getId(), time))
                    continue

                logging.info("Processed event. ID: %s\tTime: %s" % (sbmlEvent.getId(), time))

                numEventAssignments = sbmlEvent.getNumEventAssignments()
                if numEventAssignments < 1:
                    continue
                events[time] = []
                for i in xrange(numEventAssignments):
                    eventAssignment = sbmlEvent.getEventAssignment(i)
                    target = str(eventAssignment.getVariable())
                    assignmentMath = eventAssignment.getMath()
                    events[time].append((target, assignmentMath))
                #                    logging.debug("\tTarget: %s\tAssignment: %s" % (target,assignmentMath))




            except Exception, e:
                logging.error("%s\nException: %s" % (errorMsg, e))

        events[self.settings[settingsandvalues.SETTING_ENDTIME]] = None

        try:
            self.breakpoints = Vector(ValueList(events.keys()))
            self.bioSystem.setBreakpoints(self.breakpoints)

            for i, (time, assignmentList) in enumerate(events.items()):
                if i == 0 or i == len(self.breakpoints) - 1 or not assignmentList:
                    continue

                self.eventMap = self.bioSystem.getEvent(i)

                for target, assignment in assignmentList:
                    wrappedAssignment = ODEWrapper(None, mathNode=assignment, mainModel=self.mainModel)
                    expressionBioParkinCpp = wrappedAssignment.mathForBioParkinCpp()
                    self.eventMap[target] = expressionBioParkinCpp
                    logging.info("Event #%s\tTime: %s\tTarget: %s\tExpression: %s" % (i,time,target,expressionBioParkinCpp))

                self.bioSystem.setEvent(i, self.eventMap)
        except Exception, e:
            logging.error("ParkinCppBackend._setBioSystemEvents(): Error while creating events: %s" % e)

        return

    def _createBioProcessor(self):
        """
        This creates the BioProcessor. The BioProcessor is the means to do
        computations on a BioSystem object.
        It provides methods for forward integrations, sensitivity calculations, and
        parameter identification.

        The BioProcessor is the abstraction level between BioPARKIN and actual
        internal numerical classes like GaussNewton, Parkin, etc.
        """
        self.bioProcessor = BioProcessor(self.bioSystem, self.settings[settingsandvalues.SETTING_IDENTIFICATION_BACKEND])

        # 22.08.12 td : need to wrap sys.stdout *first* ; only then the redirected stream can be set to parkin
        # # 21.08.12 td : an awkward trail to get the two logging systems (dlib::logger & logging), somehow unified
        # self.bioProcessor.setLogStream(MakeCppOStream(sys.stdout))

    def _doSimulation(self):
        """
        Entry point to start a normal forward computation run.
        """
        if not self.bioSystem:
            logging.debug("ParkinCppBackend._doSimulation invoked without a bioSystem.")
            return False

        if not self.bioProcessor:
            logging.debug("ParkinCppBackend._doSimulation invoked without a BioProcessor.")
            return False

        rawSimData = self._computeTimecourse()
        simDataSet = self._handleSimulationResults(rawSimData)
        self.dataService.add_data(simDataSet)

        return True

    def _computeTimecourse(self):
        """
        Does a single forward calculation and puts the results
        into some class variables.
        """
        logging.info("Computing Timecourse...")

        trajectoryMap = self.bioProcessor.computeModel()

        # extract the computed solution vectors
        tp = self.bioProcessor.getAdaptiveTimepoints()
        self.timepointsPruned = [tp.t()[i] for i in xrange(tp.nr())]
        self.timepoints = [self.settings[backend.settingsandvalues.SETTING_STARTTIME]] + self.timepointsPruned

        simResults = OrderedDict()
        for speciesId in trajectoryMap.keys():
            correspondingSpecies = self.mainModel.getSpecies(speciesId)
            if correspondingSpecies:  # 09.08.12 td: what happens with DAE entries??? They have no SBML corresponding IDs
                dataTuple = trajectoryMap[speciesId]
                data = list(dataTuple)
                data.insert(0, correspondingSpecies.getInitialValue())
                simResults[correspondingSpecies] = data

        return simResults


    def _handleSimulationResults(self, simResults):
        """
        Strutures the data so that the DataService can make use of it.
        """
        logging.info("Handling simulation results...")
        dataSet = DataSet(None) # no filename given
        dataSet.setType(services.dataservice.SIMULATION)
        dataSet.setId(settingsandvalues.SIMULATION_RESULTS)
        dataSet.setSelected(True)
        for speciesEntity, data in simResults.items():
            entityData = EntityData()
            entityData.setId(speciesEntity.getId())
            entityData.setType(datamanagement.entitydata.TYPE_SIMULATED)
            entityData.setAssociatedDataSet(dataSet)
            entityData.setSelected(True)

            entityData.timepoints = self.timepoints
            entityData.datapoints = data
            entityData.dataDescriptorName = "Timepoint"
            # can't set dataDescriptorUnit here because the backend knows nothing about it
            # TODO: Handle DataDescriptorUnit

            entityData.sbmlEntity = speciesEntity
            dataSet.setData(entityData, keyEntity=speciesEntity)

        return dataSet


    def _handleSensitivityResults(self, sensResults):
        """
        Strutures the sensitivity data so that the DataService can make use of it.
        """
        logging.info("Handling sensitivity results...")
        dataSet = DataSet(None) # no filename given
        dataSet.setType(services.dataservice.SENSITIVITY_DETAILS_SUBCONDITION)
        dataSet.setId(settingsandvalues.SENSITIVITY_RAW_JACOBIAN)
        dataSet.setSelected(True)
        for (speciesEntity, paramID), data in sensResults.items():
            entityData = EntityData()
            entityData.setId("%s/%s" % (speciesEntity.getId(), paramID))
            entityData.setType(datamanagement.entitydata.TYPE_SIMULATED)
            entityData.setAssociatedDataSet(dataSet)
            entityData.setSelected(True)

            entityData.timepoints = self.timepoints
            entityData.datapoints = data
            entityData.dataDescriptorName = "Timepoint"
            # can't set dataDescriptorUnit here because the backend knows nothing about it
            # TODO: Handle DataDescriptorUnit

            entityData.sbmlEntity = speciesEntity
            dataSet.setData(entityData, keyEntity=speciesEntity)

        return dataSet


    def _computeSensitivityOverview(self):
        """
        Computing the sensitivities of parameters using the
        PARKINcpp library.
        """
        logging.info("Computing Sensitivity Overview...")
        self.report_progress(text="Computing Sensitivity Overview...")

        isSetUp = self._setUpBioProcessor(mode = TASK_SENSITIVITY_OVERVIEW)
        if not isSetUp:
            logging.error("Could not start sensitivity computation.")
            return False

        if not self.bioProcessor:
            return False

#        # set up FORTRAN console capturing
#        # found here: http://stackoverflow.com/questions/977840/redirecting-fortran-called-via-f2py-output-in-python
#        # open 2 fds
#        #null_fds = [os.open(os.devnull, os.O_RDWR) for x in xrange(2)]
#        null_fds = [os.open("d:/test%s.txt" % x, os.O_RDWR) for x in xrange(2)]
#        # save the current file descriptors to a tuple
#        save = os.dup(1), os.dup(2)
#        # put /dev/null fds on 1 and 2
#        os.dup2(null_fds[0], 1)
#        os.dup2(null_fds[1], 2)

        self.bioProcessor.computeSensitivityTrajectories() # compute non-scaled trajectories but don't use them
        self.sensitivityTrajectoryMap = self.bioProcessor.getScaledSensitivityTrajectories() # always get the scaled trajectories

        if not self.sensitivityTrajectoryMap:
            logging.error("Computation of Sensitivity Overview failed. Empty trajectory map returned.")
            return False

        # update timepoints to those that were actually used (generated) during sensitivity calculations
        tp = self.bioProcessor.getAdaptiveTimepoints()
        self.timepointsPruned = [tp.t()[i] for i in xrange(tp.nr())]
        self.timepoints = [self.settings[backend.settingsandvalues.SETTING_STARTTIME]] + self.timepointsPruned

#        # 2nd part of FORTRAN console capturing
#        # restore file descriptors so I can print the results
#        os.dup2(save[0], 1)
#        os.dup2(save[1], 2)
#        # close the temporary fds
#        os.close(null_fds[0])
#        os.close(null_fds[1])

        dataSets = {}
        for key, dataPoints in self.sensitivityTrajectoryMap.items():
            if len(dataPoints) == 0:
                logging.error("No trajectory for %s" % key)
                continue
                
            splitKey = key.split(" / ")
            speciesId = splitKey[0]
            paramId = splitKey[1]

            if not dataSets.has_key(paramId):
                dataSet = DataSet(None) # no filename given
                dataSet.setType(services.dataservice.SENSITIVITY_OVERVIEW)
                dataSet.setId(paramId)
                dataSet.setSelected(True)
                dataSets[paramId] = dataSet
                self.dataService.add_data(dataSet)
            else:
                dataSet = dataSets[paramId]

            speciesEntity = self.mainModel.getSpecies(speciesId)
            if not speciesEntity.getComputeSensitivity():   # don't save data of non-selected species
                continue

            entityData = EntityData()
            entityData.setId(speciesId)
            entityData.setType(datamanagement.entitydata.TYPE_SENSITIVITY_OVERVIEW)
            entityData.setAssociatedDataSet(dataSet)
            entityData.setSbmlEntity(speciesEntity)
            entityData.setSelected(True)

            entityData.timepoints = self.timepointsPruned
            entityData.datapoints = list(dataPoints)
            entityData.dataDescriptorName = "Timepoint"
            # can't set dataDescriptorUnit here because the backend knows nothing about it
            # TODO: Handle DataDescriptorUnit

            dataSet.setData(entityData, keyEntity=speciesId)
#            logging.debug("Adding data for Species %s" % speciesId)

        logging.info("Finished computing Sensitivity Overview...")

        return True

    def _computeSensitivityDetails(self):
        logging.info("Computing Detailed Sensitivities...")

        isSetUp = self._setUpBioProcessor(mode = TASK_SENSITIVITIES_DETAILS)
        if not isSetUp:
            logging.error("Could not start sensitivity computation.")
            return False

        if not self.bioProcessor:
            return False
        if not self.sensitivityTimepoints:
            logging.debug("ParkinCppBackend._computeSensitivityDetails(): No timepoints set, aborting.")
            logging.error("No timepoints given. Please provide some.")
            return False

        logging.debug("ParkinCppBackend._computeSensitivityDetails(): Setting timepoints for detailed sensitivities to %s" % self.sensitivityTimepoints)
        self.sensitivityTimepointsVector = Vector(ValueList(self.sensitivityTimepoints))
        logging.debug("ParkinCppBackend._computeSensitivityDetails(): About to prepare detailed sensitivities...")
        errorInt = self.bioProcessor.prepareDetailedSensitivities(self.sensitivityTimepointsVector)
        if errorInt != 0:
            logging.error("Could not prepare detailed sensitivities. Return code: %s" % errorInt)
            return False
            
        qrConDecompVector = self.bioProcessor.getSensitivityDecomps()
        rawJacobianMatrixVector = self.bioProcessor.getSensitivityMatrices()  # gets raw Jacobian matrix

        for i, qrConDecomp in enumerate(qrConDecompVector):
            timepoint = self.sensitivityTimepoints[i]
            subconditionDataSet = self._computeSensSubconditions(qrConDecomp, timepoint)
            rank = qrConDecomp.getRank()
            logging.info("Rank of matrix at timepoint %s: %s" % (timepoint, rank))
            self.dataService.add_data(subconditionDataSet)

        for i, rawJacobianMatrix in enumerate(rawJacobianMatrixVector):
            timepoint = self.sensitivityTimepoints[i]
            speciesParameterSensitivity = self._handleJacobianMatrix(rawJacobianMatrix, timepoint)
            self.dataService.add_data(speciesParameterSensitivity)

        logging.info("Finished computing Detailed Sensitivities...")

        return True


    def _handleJacobianMatrix(self, rawJacobian, timepoint):
        """
        The raw Jacobian matrix will be packed into EntityData objects (one per Parameter).
        The resulting output is wrapping into a DataSet structure.
        """
        
        if type(rawJacobian) is not Matrix:
            logging.debug("parkinCppBackend._computeSpeciesParameterSens: Didn't get a Matrix as input.")
            return None

        numSpecies = len(self.odeManager.odeList)

        if (rawJacobian.nr() % numSpecies != 0):
            logging.debug("parkinCppBackend._computeSpeciesParameterSens: Wrong format of raw Jacobian.")
            return None

        logging.info("Preparing sensitivity data for timepoint %s..." % timepoint)

        listOfSpecies = self.bioSystem.getSpecies()
        
        speciesParameterSensitivity = DataSet(None)
        speciesParameterSensitivity.setId("%s | Timepoint %s" % (settingsandvalues.SENSITIVITY_PER_PARAM_AND_SPECIES, timepoint))
        speciesParameterSensitivity.setType(services.dataservice.SENSITIVITY_DETAILS_JACOBIAN)
        speciesParameterSensitivity.setSelected(True)

        for k, param in enumerate(self.selectedParams): # needed to get Param object corresponding to index
            jacobianColumn = rawJacobian.colm(k+1)  # note: type(rawJacobian)==Matrix starts counting with 1, not with 0
            paramID = param.getCombinedId()

            sensData = [abs(jacobianColumn[j]) for j in xrange(jacobianColumn.nr())] # convert Vector to list

            paramSpeciesData = EntityData()
            paramSpeciesData.setAssociatedDataSet(speciesParameterSensitivity)
            paramSpeciesData.setId("Sensitivity of Parameter %s for timepoint %s" % (paramID, timepoint))
            paramSpeciesData.setType(datamanagement.entitydata.TYPE_SENSITIVITY_DETAILS_JACOBIAN)
            paramSpeciesData.dataDescriptors = listOfSpecies
            paramSpeciesData.datapoints = sensData
            paramSpeciesData.setSelected(True)
            speciesParameterSensitivity.setData(paramSpeciesData, keyEntity=param)

        return speciesParameterSensitivity


    def _computeSensSubconditions(self, qr, timepoint):
        """
        Takes the qr-decomposed matrix and computes subconditions. This method
        then puts the resulting data into a DataSet.
        """
        if type(qr) is not QRconDecomp:
            logging.debug("FortranBackend._computeSensSubconditions: Didn't get a QRconDecomp as input.")
            return None

        logging.info("Computing Subconditions...")

        diagonals = qr.getDiag()
        rank = qr.getRank()    # not used right now
        logging.info("QR decomposition rank: %s" % rank)
        logging.debug("QR decompsition diag: %s" % diagonals.t())
        pivotIndices = qr.getPivot()

        colSubconditions = []
        firstDiag = abs(diagonals[0])
        for i in xrange(len(diagonals)):
            diagEntry = abs(diagonals[i])
            if diagEntry != 0.0 and i < rank:
                colSubcondition = firstDiag / diagEntry
                colSubconditions.append(colSubcondition)
            else:
                colSubconditions.append(float("nan"))

        maxValue = max(colSubconditions)

        colSubconditionsScaled = []
        for i in xrange(len(colSubconditions)):
            oldValue = colSubconditions[i]
            if math.isnan(oldValue):
                scaledValue = oldValue  # push "nan" through to the end; should be handled by Views
            else:
                scaledValue = oldValue / maxValue
            colSubconditionsScaled.append(scaledValue)

        # 4th: put into DataSet
        subconditionsDataSet = DataSet(None)
        subconditionsDataSet.setId("%s | Timepoint %s" % (settingsandvalues.SENSITIVITY_SUBCONDITION_PER_PARAM, timepoint))
        subconditionsDataSet.setType(services.dataservice.SENSITIVITY_DETAILS_SUBCONDITION)
        subconditionsDataSet.setSelected(True)

        for i in xrange(len(colSubconditionsScaled)):
            paramIndex = int(pivotIndices[i] - 1)    # pivot elements are counted 1-based
            param = self.selectedParams[paramIndex]

            subconditionScaled = colSubconditionsScaled[i]
            subconditionAbs = colSubconditions[i]
            paramData = EntityData()
            paramData.setAssociatedDataSet(subconditionsDataSet)
            paramData.setId("Sensitivity Subcondition of Parameter %s at timepoint %s" % (param.getCombinedId(), timepoint))
            paramData.setType(datamanagement.entitydata.TYPE_SENSITIVITY_DETAILS_SUBCONDITION)
            paramData.dataDescriptors = ["Subcondition (as %% of %g)" % maxValue, settingsandvalues.SUBCONDITION_HEADER_ABSOLUTE]
            paramData.datapoints = [subconditionScaled, subconditionAbs]
            paramData.setSelected(True)
            subconditionsDataSet.setData(paramData, keyEntity=param)

        return subconditionsDataSet



    def _setUpBioProcessor(self, mode = TASK_PARAMETER_IDENTIFICATION):
        """
        Further prepares the BioSystem so that it can be used by a GaussNewton object.
        Also creates said GaussNewton object and all the input it needs.
        """
        # get selected parameters (exclude non-constant ones, e.g. with assignm. rules)
        if mode == TASK_PARAMETER_IDENTIFICATION:
            self.selectedParams = [param for param, isSelected in self.paramToEstimateMap.items() if isSelected and param.isConstant()]
        elif mode == TASK_SENSITIVITY_OVERVIEW or mode == TASK_SENSITIVITIES_DETAILS:
            self.selectedParams = [param for param, isSelected in self.paramToSensitivityMap.items() if isSelected and param.isConstant()]

        if not self.selectedParams:
            logging.error("No parameters selected.")
            return False

        if mode == TASK_PARAMETER_IDENTIFICATION:
            self.timepointVector, self.measurementMapVector = self._getBioParkinCppCompatibleMeasurements()

            if not self.measurementMapVector or not self.timepointVector:
                logging.debug("ParkinCppBackend._doParameterEstimation(): Could not obtain timepoints and/or datapoints.")
                return False

            self.bioSystem.setMeasurementList(self.timepointVector, self.measurementMapVector)

        # set up parameters for BioProcessor
        self.paramMap = Param()
        self.paramThresholdMap = Param()
        for selectedParam in self.selectedParams:
            combinedID = selectedParam.getCombinedId()  # includes "scope_"
            value = self.mainModel.getValueFromActiveSet(combinedID)
            self.paramMap[combinedID] = value
            thres = selectedParam.getThreshold()
            if not thres:
                logging.error("There are Parameters for which thresholds have not been set. Computing sensitivities is not possible without thresholds. Please, set thresholds!")
                return False
            self.paramThresholdMap[combinedID] = thres
#
        self.bioProcessor.setCurrentParamValues(self.paramMap)
        self.bioProcessor.setCurrentParamThres(self.paramThresholdMap)

        # set up Species thresholds
        self.speciesThresholdMap = Param()
        for species in self.odeManager.speciesList:
            speciesID = species.getId()
            thres = species.getThreshold()
            if not thres:
                continue
            self.speciesThresholdMap[speciesID] = thres
        if self.speciesThresholdMap:
            self.bioProcessor.setCurrentSpeciesThres(self.speciesThresholdMap)

        self.iOpt = self.bioProcessor.getIOpt()
        self.iOpt.mode = 0                                                                      # 0:normal run, 1:single step
        self.iOpt.jacgen = int(self.settings[settingsandvalues.SETTING_JACOBIAN])               # 1:user supplied Jacobian, 2:num.diff., 3:num.diff.(with feedback)
        self.iOpt.qrank1 = False                                                                # allow Broyden rank-1 updates if __true__
        self.iOpt.nonlin = int(self.settings[settingsandvalues.SETTING_PROBLEM_TYPE])           # 1:linear, 2:mildly nonlin., 3:highly nonlin., 4:extremely nonlin.
        self.iOpt.rscal = int(self.settings[settingsandvalues.SETTING_RESIDUAL_SCALING])        # 1:use unchanged fscal, 2:recompute/modify fscal, 3:use automatic scaling only
        self.iOpt.mprmon = 2
        self.iOpt.mprerr = 1
        self.iOpt.itmax = int(self.settings[backend.settingsandvalues.SETTING_MAX_NUM_NEWTON_STEPS])
        self.bioProcessor.setIOpt(self.iOpt)

        # consider contstarints for both parameter identification *and* sensitivities

        # global constraints
        globalConstraintsType = self.settings[settingsandvalues.SETTING_PARAMETER_CONSTRAINTS]
        trans, upperbounds, lowerbounds = [],[],[]
        if not self.settings[settingsandvalues.SETTING_PARAMETER_CONSTRAINTS_PER_PARAMETER]:
            trans = [settingsandvalues.OPTIONS_PARAMETER_CONSTRAINT_TYPES.index(globalConstraintsType)] * len(self.selectedParams)
            lowerbounds = [self.settings[settingsandvalues.SETTING_PARAMETER_CONSTRAINTS_LOWERBOUND]] * len(self.selectedParams)
            upperbounds = [self.settings[settingsandvalues.SETTING_PARAMETER_CONSTRAINTS_UPPERBOUND]] * len(self.selectedParams)

        else: #local constraints
            for selectedParam in self.selectedParams:
                typeInt = settingsandvalues.OPTIONS_PARAMETER_CONSTRAINT_TYPES.index(str(selectedParam.getConstraintType()))
                trans.append(typeInt)
                lowerbounds.append(float(selectedParam.getConstraintLowerBound()))
                upperbounds.append(float(selectedParam.getConstraintUpperBound()))

        trans = Vector(ValueList(trans))
        lowerbounds = Vector(ValueList(lowerbounds))
        upperbounds = Vector(ValueList(upperbounds))
        self.bioProcessor.setParameterConstraints(trans, lowerbounds, upperbounds)

        return True
        

    def _doParameterEstimation(self):
        """
        Create the Gauss Newton object (involves calling ._setUpGaussNewton())
        and run the parameter identification.
        """

        isSetUp = self._setUpBioProcessor(mode = TASK_PARAMETER_IDENTIFICATION)
        if not isSetUp:
            logging.error("Could not start parameter identification.")
            return False
        if not self.bioProcessor:
            return False

        xtol = float(self.settings[settingsandvalues.SETTING_XTOL])

        # 21.08.12 td : counterpart of logging unification test
        out = StdOutWrapper()
        self.bioProcessor.setLogStream(MakeCppOStream(sys.stdout))
        error = self.bioProcessor.identifyParameters(xtol=xtol)
        out.close()

        # 24.07.12 td
        # condition error == 0 for successful convergence is too much to ask
        # if error != 0:
        if error > 2:
            logging.error("Error during parameter identification in PARKINcpp.")
            return False
        paramMap = self.bioProcessor.getIdentificationResults()

        # convert results; put into class variable
        self.estimatedParams = OrderedDict()
        for paramID, value in paramMap.items():
            self.estimatedParams[paramID] = value

	# 26.04.12 td
	# compute RMS values according to available measurement points and
	# for each species seperately (in relation!)
	measMapVector = self.bioSystem.getMeasurementList()
	synMapVector = self.bioSystem.getSimTrajectoryList()
	if measMapVector and synMapVector:
		logging.info("------------------------------")
		logging.info("Computing relative RMS values.")
		self.relRMS = OrderedDict()
		countMeas = 0
		for i in xrange(len(measMapVector)):
			measPointMap = measMapVector[i]
			synPointMap = synMapVector[i]
			for speciesID in measPointMap.keys():
				(measVal, weight) = measPointMap[speciesID]
				if speciesID in synPointMap:
					(synVal, dummy) = synPointMap[speciesID]
				else:
					continue
				dval = 0.0
				countMeas += 1
				if float(weight) != 0.0 and float(weight) != float("nan"):
					dval = (float(measVal) - float(synVal)) / float(weight)
				
				if speciesID in self.relRMS.keys():
					self.relRMS[speciesID] += dval*dval
				else:
					self.relRMS[speciesID] = dval*dval

		if countMeas > 0:
			totRMS = sum([self.relRMS[spec] for spec in self.relRMS.keys()])
			logging.info(" Total RMS**2: %e" % (float(totRMS)/float(countMeas)) )
			for speciesID, rmsValue in self.relRMS.items():
				logging.info("    (%5.2f%%)   %e  =  relRMS[%s]**2 " % ( 100.0*float(rmsValue)/float(totRMS), float(rmsValue)/float(countMeas), speciesID) )
		else:
			logging.warning("   No measurements present?!?  ")
		logging.info("------------------------------")


        return True # computation successful



    def _getBioParkinCppCompatibleMeasurements(self):
        """
        Takes experimental data from the DataService and puts it into PARKINcpp classes.
        """
        # get the currently loaded experimental data
        dataService = DataService()
        expData = dataService.get_selected_experimental_data() # get's the *datasets* that are selected (in the data browser)
        if not expData or len(expData.items()) == 0:
            logging.debug("ParkinCppBackend._getBioParkinCppCompatibleMeasurements(): No Experimental Data.")
            logging.info("No experimental data loaded. Can't estimate parameter values.")
            return None, None

        # Step 1: Create a global timepoint list. The number of times any timepoint occurs is the
        # maximum of occurences within the Species.
        timepointList = []
        for dataSetID, dataSet in expData.items():
            logging.debug("ParkinCppBacken._getBioParkinCppCompatibleMeasurements(): Getting timepoints from %s" % dataSetID)
            for sbmlSpecies, entityData in dataSet.getData().items():
                if not entityData.isSelected(): # ignores entity data that is not selected (i.e. non-selected columns in the data browser)
                    continue
                speciesTimepointsList = []
                speciesTimepointsSet = set()
                for i, dataDescriptor in enumerate(entityData.dataDescriptors):
                    try:
                        if type(sbmlSpecies) is SBMLEntity:
                            speciesID = sbmlSpecies.getId()
                        else:
                            speciesID = str(sbmlSpecies)
                        timepoint = float(dataDescriptor)

                        # ignore timepoints that are outside of the current integration interval
                        if timepoint <= self.settings[settingsandvalues.SETTING_STARTTIME]\
                        or timepoint > self.settings[settingsandvalues.SETTING_ENDTIME]:
                            continue

                        speciesTimepointsList.append(timepoint) # may be unordered
                        speciesTimepointsSet.add(timepoint)
                    except Exception, e:
                        logging.debug(
                            "ParkinCppBackend._getBioParkinCppCompatibleMeasurements(): Problem while creating global timepoint list with Species %s" % speciesID)

                # Check timepoints of this Species and add them to the global list if needed.
                for timepoint in speciesTimepointsSet:
                    countSpecies = speciesTimepointsList.count(timepoint)
                    countGlobal = timepointList.count(timepoint)
                    if countSpecies > countGlobal:   # if this timepoint isn't included in the global list often enough
                        difference = countSpecies - countGlobal
                        toAdd = [timepoint for i in range(difference)]
                        timepointList.extend(toAdd) # add it as often as is needed
        timepointList.sort()    # sort timepoints ascending

        # Step 2: Go through the local timepoints of each Species and put their data into the correct places in the global list

        # prepare list with empty MeasurementPoints
        datapointList = []
        for i in xrange(len(timepointList)):
            datapointList.append(MeasurementPoint())

        for dataSetID, dataSet in expData.items():
            #logging.debug("ODEManager: Getting timepoints from %s" % dataSetID)
            for sbmlSpecies, entityData in dataSet.getData().items():
                if not entityData.isSelected(): # ignores entity data that is not selected (i.e. non-selected columns in the data browser)
                    continue
                countTimepoints = {}
                for i, dataDescriptor in enumerate(entityData.dataDescriptors):
                    try:
                        if type(sbmlSpecies) is SBMLEntity:
                            speciesID = sbmlSpecies.getId()
                        else:
                            speciesID = str(sbmlSpecies)
                        timepoint = float(dataDescriptor)

                        # ignore timepoints that are outside of the current integration interval
                        if timepoint <= self.settings[settingsandvalues.SETTING_STARTTIME]\
                        or timepoint > self.settings[settingsandvalues.SETTING_ENDTIME]:
                            continue

                        # 31.07.12 td
                        # ignore datapoint if not set/loaded at all
                        if not entityData.datapoints[i]:
                            continue


                        dataPoint = float(entityData.datapoints[i])


                        # 26.07.12 td
                        try:
                            thres = abs(sbmlSpecies.getThreshold())
                        except:
                            thres = 0.0

                        try:
                            weightRaw = entityData.getWeights()[i]
                            weight = max( abs(float(weightRaw)), thres )
                        #    weight /= sbmlSpecies.getThreshold()
                        # except: # take user-defined value if no float was provided by the loaded data
                        #     weight = float(self.settings[settingsandvalues.SETTING_SD_SPECIES])
                        # 25.07.12 td
                        except: # take datapoint value if no float was provided by the loaded data (as in YeOldeParkin!)
                            weight = max( abs(dataPoint), thres )

                    except Exception, e:
                        logging.debug(
                            "ParkinCppBackend._getBioParkinCppCompatibleMeasurements(): Problem while getting data of Species %s" % speciesID)

                    try:
                        if timepoint in countTimepoints.keys(): # already had this timepoint at least once
                            # handle non-unique timepoint
                            index = timepointList.index(timepoint) #always gets the first occurence of that timepoint
                            index += countTimepoints[timepoint] # this should yield the correct index
                            if speciesID in datapointList[index].keys():
                                logging.debug(
                                    "ParkinCppBackend._getBioParkinCppCompatibleMeasurements(): MeasurementPoint entry for Species %s at timepoint %s already there." % (
                                    speciesID, timepoint))
                            datapointList[index][speciesID] = (dataPoint, weight)
                            countTimepoints[timepoint] += 1
                        else:
                            # handle new timepoint
                            index = timepointList.index(timepoint)
                            datapointList[index][speciesID] = (dataPoint, weight)
                            countTimepoints[timepoint] = 1
                    except Exception, e:
                        logging.debug("ParkinCppBackend._getBioParkinCppCompatibleMeasurements(): Error while trying to assign Species datapoint to global data list. Error: %s" % e)


            measurementMapVector = MeasurementList(len(datapointList))
        for i in xrange(len(datapointList)):
            measurementMapVector[i] = datapointList[i]

        timepointVector = Vector(ValueList(timepointList))

        return (timepointVector, measurementMapVector)


    def _handleEstimatedParamResults(self):
        """
        Takes the previously computed parameter values (stored in a OrderedDict), wraps
        them into EntityData objects and a DataSet and puts that into the DataService.
        """
        estimatedParamSet = DataSet(None)
        estimatedParamSet.setId("Identified Parameter Values")
        estimatedParamSet.setType(services.dataservice.ESTIMATED_PARAMS)

        selected = {}
        for selectedParam in self.selectedParams:
            selected[selectedParam.getCombinedId()] = selectedParam

        for i, (paramID, estimatedValue) in enumerate(self.estimatedParams.items()):
            if not paramID in selected.keys():
                continue
            param = selected[paramID]  # if paramID is in selected dict, get the related sbmlEntity object 
            paramData = EntityData()
            paramData.setId(param.getId())
            paramData.setType(datamanagement.entitydata.TYPE_PARAMETERS_ESTIMATED)
            paramData.setAssociatedDataSet(estimatedParamSet)
            paramData.dataDescriptors = ["Identified Value"]
            paramData.datapoints = [estimatedValue]
            paramData.sbmlEntity = param

            estimatedParamSet.setData(paramData, keyEntity=param)

        self.dataService.add_data(estimatedParamSet)

