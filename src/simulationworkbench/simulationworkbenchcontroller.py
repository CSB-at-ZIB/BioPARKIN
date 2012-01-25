from collections import OrderedDict
import time
from PySide.QtCore import  Slot, Qt
from PySide.QtGui import QSortFilterProxyModel, QTabBar, QMessageBox, QTableWidgetItem, QWidget
from backend_parkincpp.parkincppbackend import ParkinCppBackend
from parkincpp import parkin
from services import dataservice
import services.dataservice
import datamanagement.dataset
import backend
import parametertablemodel, speciestablemodel
from services.optionsservice import OptionsService
from services.statusbarservice import StatusBarService
import simulationworkbench
import logging
from simulationworkbench.parametersetstablemodel import ParameterSetsTableModel
from simulationworkbench.Ui_simulationworkbench_v4 import Ui_SimulationWorkbench
from simulationworkbench.widgets import tablewidgetcontroller
from simulationworkbench.widgets.databrowser import DataBrowser
from simulationworkbench.widgets.dataimportwidget import DataImportWidget
from simulationworkbench.widgets.resultswindowcontroller import ResultsWindowController
from simulationworkbench.widgets.timepointchooser import TimepointChooser
import widgets

from simulationworkbench.speciestablemodel import SpeciesTableModel
from simulationworkbench.parametertablemodel import ParameterTableModel
from services.progressbarservice import ProgressBarService
from services.dataservice import DataService
from simulationworkbench.widgets.plotwidgetcontroller import PlotWidgetController
from simulationworkbench.widgets.tablewidgetcontroller import TableWidgetController
from backend.exceptions import InitError


DEFAULT_TIMEUNIT = "s"

class SimulationWorkbenchController(QWidget, Ui_SimulationWorkbench):
    """
    This is the Controller (more in the line of a code-behind file)
    for the Simulation Workbench.

    The UI is handled separately by QT Designer 4 with the
    simulationworkbench_v*.ui file.

    @since: 2010-06-16
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, parent=None, parkinController=None):
        """
        Constructor
        """
        super(SimulationWorkbenchController, self).__init__(parent)
        self.setupUi(self)

        self.computeDetailedSensitivitiesButton.setEnabled(True)

        self.parkinController = parkinController
        self.sbmlModel = None
        self.speciesSliders = {}

        self.speciesTableModel = None
        self.parametersTableModel = None

        self.dataBrowserWidgets = {}

        self.resultsWindow = None # will be created on first creation of plot/table
        self.timepointChooser = None

        self.dataService = DataService()
        self.statusBarService = StatusBarService()
        self.optionsService = OptionsService()

        self.backendBioParkinCpp = None
        self.backendFortran = None
        self.currentBackend = None

        self.on_comboBoxBackendSelect_currentIndexChanged(0) # for updating the GUI

        self.optionStartTime = backend.settingsandvalues.DEFAULT_STARTTIME
        self.optionEndTime = backend.settingsandvalues.DEFAULT_ENDTIME
        self.optionTimeUnit = DEFAULT_TIMEUNIT

        self.optionRTOL = backend.settingsandvalues.DEFAULT_RTOL
        self.optionATOL = backend.settingsandvalues.DEFAULT_ATOL
        self.optionXTOL = backend.settingsandvalues.DEFAULT_XTOL
        self.optionMaxNumNewtonSteps = backend.settingsandvalues.DEFAULT_MAX_NUM_NEWTON_STEPS
        self.optionSDSpecies = backend.settingsandvalues.DEFAULT_SD_SPECIES #obsolete
        self.optionNOROWSCAL = False # backend.settingsandvalues.DEFAULT_NO_AUTO_ROW_SCALING
        self.optionJACGEN = backend.settingsandvalues.DEFAULT_JACOBIAN
        self.optionNONLIN = backend.settingsandvalues.DEFAULT_PROBLEM_TYPE
        self.optionRSCAL = backend.settingsandvalues.DEFAULT_RESIDUAL_SCALING

        self.optionParameterConstraints = backend.settingsandvalues.DEFAULT_PARAMETER_CONSTRAINTS
        self.optionParameterConstraintsLowerbound = backend.settingsandvalues.DEFAULT_PARAMETER_CONSTRAINTS_LOWERBOUND
        self.optionParameterConstraintsUpperbound = backend.settingsandvalues.DEFAULT_PARAMETER_CONSTRAINTS_UPPERBOUND


        self.optionPlotExpDataOnSimulation = False


        self.currentExpDataFilename = ""
        self.currentExpData = []

        self.machineEpsilon = parkin.EPMACH

        self.setUpInputFields()
        self.setUpDataBrowser()

        if self.parkinController: #should always be the case
            self.parkinController.modelClosed.connect(self.clear)
            self.parkinController.activeModelChanged.connect(self.on_activeModelChanged)

    def on_activeModelChanged(self, activeModelController=None):
#        logging.debug("in SimulationWorkbenchController.on_activeModelChanged()")
        try:
            if not activeModelController:   # should only happen when called directly from self.__init__()
                activeModelController = self.parkinController.ActiveModelController

            if activeModelController:
                logging.info("Prepared model from file '%s' for simulation." % activeModelController.filename)
                self.setSBMLModel(activeModelController.sbmlModel)
            else:
                self.clear()

        except Exception, e:
            logging.debug("SimulationWorkbenchController.activeModelChanged() - Error: %s" % e)

    def setSBMLModel(self, model):
        """
        Set the model which should be simulated, etc.
        Also invokes self._initialize() to fill Tables, etc. with data.
        """
        if model == self.sbmlModel: # everything's already initialized, we don't do anything
            return

        self.sbmlModel = model  # None is a valid value! (e.g. after closing the last model)

        if not self.sbmlModel:
            return

        self.sbmlModel.createParameterSetForFit()

        if not self.getListOfParameterSets():
            logging.error(
                "SimulationWorkbench: Encountered a model without a ListOfParameterSets. This should never happen.")

        self._initialize()
        if self.currentBackend:
            self.currentBackend.isCompilationNeeded = True


    def _initialize(self):
        """
        Sets up the main UI parts. Fills tables with data, etc.
        """
        self.setWindowTitle(self.sbmlModel.filename.split('/')[-1])
        try:
            self._initializeTables()
        except Exception, e:
            logging.debug("SimulationWorkbenchController._initialize(): Error while creating tables: %s" %e)


    def _initializeTables(self):
        """
        Sets up all the tables (models + views).
        """

        # Species Tab
        speciesEntities = self.sbmlModel.SbmlSpecies
        self.speciesTableModel = SpeciesTableModel(speciesEntities)
        self.speciesTableModel.dataChanged.connect(self.speciesChanged)

        # use a generic QSortFilterProxyModel for sorting
        speciesProxyModel = QSortFilterProxyModel(self)
        speciesProxyModel.setSourceModel(self.speciesTableModel)

        self.speciesTableView.setSortingEnabled(True)
        self.speciesTableView.setModel(speciesProxyModel)
        self.speciesTableView.sortByColumn(0, Qt.AscendingOrder)
        self.speciesTableView.hideColumn(speciestablemodel.COLUMN.COMPUTESENSITIVITY)
        self.speciesTableView.resizeColumnsToContents()


        # Parameter Tab
        paramEntities = self.sbmlModel.SbmlParameters
        self.parametersTableModel = ParameterTableModel(paramEntities, self.sbmlModel)
        self.parametersTableModel.dataChanged.connect(self.parameterChanged)

        # use a generic QSortFilterProxyModel for sorting
        parametersProxyModel = QSortFilterProxyModel(self)
        parametersProxyModel.setSourceModel(self.parametersTableModel)

        self.parametersTableView.setSortingEnabled(True)
        self.parametersTableView.setModel(parametersProxyModel)
        self.parametersTableView.sortByColumn(0, Qt.AscendingOrder)
        self.parametersTableView.hideColumn(parametertablemodel.COLUMN.COMPUTESENSITIVITY)
        self.parametersTableView.hideColumn(parametertablemodel.COLUMN.ESTIMATE)
        self.parametersTableView.resizeColumnsToContents()


        # Sensitivity Tab

        # use 2nd generic QSortFilterProxyModel for sorting
        sensitivityProxyModel = QSortFilterProxyModel(self)
        sensitivityProxyModel.setSourceModel(self.parametersTableModel)

        self.sensitivityTableView.setSortingEnabled(True)
        self.sensitivityTableView.setModel(sensitivityProxyModel)
        self.sensitivityTableView.sortByColumn(0, Qt.AscendingOrder)
        self.sensitivityTableView.hideColumn(parametertablemodel.COLUMN.INITIALVALUE)
        self.sensitivityTableView.hideColumn(parametertablemodel.COLUMN.ESTIMATE)
        self.sensitivityTableView.hideColumn(parametertablemodel.COLUMN.EMPTY_COL)
        self.sensitivityTableView.hideColumn(parametertablemodel.COLUMN.CONSTRAINT_TYPE)
        self.sensitivityTableView.hideColumn(parametertablemodel.COLUMN.CONSTRAINT_LOWER)
        self.sensitivityTableView.hideColumn(parametertablemodel.COLUMN.CONSTRAINT_UPPER)
        self.sensitivityTableView.resizeColumnsToContents()

        sensitivitySpeciesProxyModel = QSortFilterProxyModel(self)
        sensitivitySpeciesProxyModel.setSourceModel(self.speciesTableModel)

        self.tableViewSensitivitySpecies.setSortingEnabled(True)
        self.tableViewSensitivitySpecies.setModel(sensitivitySpeciesProxyModel)
        self.tableViewSensitivitySpecies.sortByColumn(0, Qt.AscendingOrder)
        self.tableViewSensitivitySpecies.hideColumn(speciestablemodel.COLUMN.COMPARTMENT)
        self.tableViewSensitivitySpecies.hideColumn(speciestablemodel.COLUMN.INITIALQUANTITY)
        self.tableViewSensitivitySpecies.hideColumn(speciestablemodel.COLUMN.ISBC)
        self.tableViewSensitivitySpecies.resizeColumnsToContents()


        # Fit Tab

        # use 2nd generic QSortFilterProxyModel for sorting
        estimateParamsProxyModel = QSortFilterProxyModel(self)
        estimateParamsProxyModel.setSourceModel(self.parametersTableModel)

        self.estimateParamsTableView.setSortingEnabled(True)
        self.estimateParamsTableView.setModel(estimateParamsProxyModel)
        self.estimateParamsTableView.sortByColumn(0, Qt.AscendingOrder)
        self.estimateParamsTableView.hideColumn(parametertablemodel.COLUMN.COMPUTESENSITIVITY)
        self.estimateParamsTableView.resizeColumnsToContents()


        # Parameter Sets Tab
        self.parameterSetsTableModel = ParameterSetsTableModel(self.getListOfParameterSets(), paramEntities)
        self.parameterSetsTableModel.dataChanged.connect(self.parameterChanged)
        self.parameterSetsTableView.setModel(self.parameterSetsTableModel)
        self.parameterSetsTableView.resizeColumnsToContents()

    def clear(self):
        """
        Clears all Views (e.g. when the last model is closed).
        """
        self.speciesTableView.setModel(None)
        self.parametersTableView.setModel(None)
        self.parameterSetsTableView.setModel(None)
        self.sensitivityTableView.setModel(None)
        self.tableViewSensitivitySpecies.setModel(None)
        self.estimateParamsTableView.setModel(None)
        self.sbmlModel = None
        self.currentBackend = None

    def getRTol(self):
        return float(self.optionRTOL)

    def _createSimulationPlot(self):
        """
        Gets the data selected in the dataSourcesTable and plots it to the
        plot tab by inserting a PlotWidget into the Tab.
        """
        logging.info("Creating Plot...")
        if not self.resultsWindow:
            self.resultsWindow = ResultsWindowController(None)
            self.resultsWindow.setAttribute(Qt.WA_QuitOnClose)

        # TODO: Either remove the old plot widget or store all plot widgets in a []/{}
        plotWidget = PlotWidgetController(parent=self.resultsWindow.getMdiArea(), host=self,
            title="Simulation (Plot) - %s" % time.strftime("%H:%M:%S", time.localtime()))
#        self.updateSelectedExpData()
        if not self.optionPlotExpDataOnSimulation:
            plotWidget.updateDataSources(self.dataService.get_simulation_data())
        else:
            selectedExpData = self.dataService.get_selected_experimental_data()
            plotWidget.setPlotStyle(widgets.plotwidgetcontroller.PLOT_LINE, plotNumber=0)
            if selectedExpData:
                for j in xrange(len(selectedExpData)):
                    plotWidget.setPlotStyle(widgets.plotwidgetcontroller.PLOT_CIRCLE, plotNumber=j + 1)
                plotWidget.updateDataSources([self.dataService.get_simulation_data(),
                                              selectedExpData])
            else:
                plotWidget.updateDataSources(self.dataService.get_simulation_data())

        self.resultsWindow.addResultSubWindow(plotWidget)
        self.resultsWindow.show()


    def _createSimulationDataTable(self):
        logging.info("Creating data table (simulated data)...")
        if not self.resultsWindow:
            self.resultsWindow = ResultsWindowController(None)

        # TODO: Either remove the old table widget or store all table widgets in a []/{}
        dataTableWidget = TableWidgetController(parent=self.resultsWindow.getMdiArea(), host=self,
            title="Simulation (Table) - %s" % time.strftime("%H:%M:%S",
                time.localtime()))
        dataTableWidget.sortColumn = 0 # sort by Timepoint
        dataTableWidget.updateDataSources(self.dataService.get_simulation_data())

        self.resultsWindow.addResultSubWindow(dataTableWidget)
        self.resultsWindow.show()


    def _createSensitivityOverviewPlot(self):
        logging.info("Creating data plot (sensitivity data)...")
        if self.currentBackend.mode != backend.settingsandvalues.MODE_SENSITIVITIES_OVERVIEW:
            return

        sensData = self.dataService.get_sensitivity_trajectory_data()
        if not sensData:
            logging.debug("SimulationWorkbenchController._createSensitivityOverviewPlot(): No sensitivity data.")
            return

        if not self.resultsWindow:
            self.resultsWindow = ResultsWindowController(None)

        # filter those DataSets that have not been displayed, yet (e.g. previous runs)
        newDataSets = OrderedDict()
        for key, dataSet in sensData.items():
            if self.resultsWindow.hasResultforData(dataSet):
                continue
            newDataSets[key] = dataSet

        logging.info("Creating data table (sensitivity trajectory data)...")
        # TODO: Either remove the old plot widget or store all plot widgets in a []/{}
        plotWidget = PlotWidgetController(parent=self.resultsWindow.getMdiArea(), host=self,
            title="Sensitivity (Plot) - %s" % time.strftime("%H:%M:%S", time.localtime()))

        plotWidget.updateDataSources(newDataSets)
        self.resultsWindow.addResultSubWindow(plotWidget)

        self.resultsWindow.show()
        self.resultsWindow.raise_()
        self.resultsWindow.activateWindow()


    def _createSensitivityDetailsSubconditionsTables(self):
        sensData = self.dataService.get_sensitivity_details_subcondition_data()
        if not sensData:
            logging.debug("SimulationWorkbenchController._createSensitivityDetailsSubconditionsTables(): No sensitivity data.")
            return

        if not self.resultsWindow:
            self.resultsWindow = ResultsWindowController(None)

        for key, dataSet in sensData.items():
            if self.resultsWindow.hasResultforData(dataSet):
                continue
            logging.info("Creating data table (sensitivity subconditions data)...")

            titleWithTime = "%s - %s" % (key, time.strftime("%H:%M:%S", time.localtime()))
            dataTableWidget = TableWidgetController(parent=self.resultsWindow.getMdiArea(), host=self, title=titleWithTime, mode=tablewidgetcontroller.MODE_SUBCONDITIONS)
            dataTableWidget.sortColumn = -1
            dataTableWidget.setOrientation(simulationworkbench.widgets.tablewidgetcontroller.ORIENTATION_VERTICAL)
            if backend.settingsandvalues.SENSITIVITY_SUBCONDITION_PER_PARAM in key:
                dataTableWidget.sortColumn = 2 # automatically sort those tables by sensitivity
            dataTableWidget.updateDataSources(sensData, dataID=key)

            self.resultsWindow.addResultSubWindow(dataTableWidget)
            


    def _createSensitivityDetailsJacobianTables(self):
        sensData = self.dataService.get_sensitivity_details_jacobian_data()

        for key, dataSet in sensData.items():
            if self.resultsWindow.hasResultforData(dataSet):
                continue
            logging.info("Creating data table (sensitivity jacobian data)...")
            # TODO: Either remove the old table widget or store all table widgets in a []/{}
            dataTableWidget = TableWidgetController(parent=self.resultsWindow.getMdiArea(), host=self,
                title="%s - %s" % (
                    key, time.strftime("%H:%M:%S", time.localtime())), mode=tablewidgetcontroller.MODE_JACOBIAN)
            dataTableWidget.sortColumn = -1
            dataTableWidget.setOrientation(simulationworkbench.widgets.tablewidgetcontroller.ORIENTATION_VERTICAL)
            dataTableWidget.updateDataSources(sensData, dataID=key)
            self.resultsWindow.addResultSubWindow(dataTableWidget)


    def _createSensitivityDetailsTable(self):
        if self.currentBackend.mode != backend.settingsandvalues.MODE_SENSITIVITIES_DETAILS:
            return

        if not self.resultsWindow:
            self.resultsWindow = ResultsWindowController(None)

        self._createSensitivityDetailsSubconditionsTables()
        self._createSensitivityDetailsJacobianTables()


    def _createEstimatedParametersTable(self):
        if self.currentBackend.mode != backend.settingsandvalues.MODE_PARAMETER_ESTIMATION:
            return

        if not self.resultsWindow:
            self.resultsWindow = ResultsWindowController(None)

        estimatedParamData = self.dataService.get_estimated_param_data()
        if not estimatedParamData:
            logging.debug(
                "SimulationWorkbenchController._updateEstimatedParametersTable(): Don't have any estimated data to display.")
            return

        for key in estimatedParamData.keys():
            logging.info("Creating data table (estimated parameters)...")
            # TODO: Either remove the old table widget or store all table widgets in a []/{}
            dataTableWidget = TableWidgetController(parent=self.resultsWindow.getMdiArea(), host=self,
                title="Par. Identification - %s" % time.strftime("%H:%M:%S",
                    time.localtime()))
            dataTableWidget.setOrientation(simulationworkbench.widgets.tablewidgetcontroller.ORIENTATION_VERTICAL)
            dataTableWidget.updateDataSources(estimatedParamData, dataID=key)

            self.resultsWindow.addResultSubWindow(dataTableWidget)
            self.parkinController.ActiveModelController.sbmlModel.createParameterSetWithFittedValues(
                estimatedParamData[key])


    def _setUpBackend(self, mode):
        if not self.sbmlModel:
            logging.info("Cannot set up computation backend. No model loaded.")
            return

        if self.currentBackend:
            self.currentBackend.finishedSignal.disconnect(self.backendRunFinished)

        # always use getNew=True for the time being (there is some problem with references when reusing the "old" backend object)
        self.currentBackend = self._getCurrentBackend(getNew=True)
        self.currentBackend.finishedSignal.connect(self.backendRunFinished)

        self.progressBarService = ProgressBarService()
        self.progressBarService.connect_to_thread(self.currentBackend)

        settings = {
            backend.settingsandvalues.SETTING_STARTTIME: self.optionStartTime,
            backend.settingsandvalues.SETTING_ENDTIME: self.optionEndTime,
            backend.settingsandvalues.SETTING_RTOL: self.optionRTOL,
            backend.settingsandvalues.SETTING_ATOL: self.optionATOL,
            backend.settingsandvalues.SETTING_XTOL: self.optionXTOL,
            backend.settingsandvalues.SETTING_MAX_NUM_NEWTON_STEPS: self.optionMaxNumNewtonSteps,
            backend.settingsandvalues.SETTING_SD_SPECIES: self.optionSDSpecies,
            backend.settingsandvalues.SETTING_JACOBIAN: self.optionJACGEN,
            backend.settingsandvalues.SETTING_PROBLEM_TYPE: self.optionNONLIN,
            backend.settingsandvalues.SETTING_RESIDUAL_SCALING: self.optionRSCAL,
            backend.settingsandvalues.SETTING_PARAMETER_CONSTRAINTS: self.optionParameterConstraints,
            backend.settingsandvalues.SETTING_PARAMETER_CONSTRAINTS_LOWERBOUND: self.optionParameterConstraintsLowerbound,
            backend.settingsandvalues.SETTING_PARAMETER_CONSTRAINTS_UPPERBOUND: self.optionParameterConstraintsUpperbound,
            backend.settingsandvalues.SETTING_IDENTIFICATION_BACKEND:
                backend.settingsandvalues.OPTIONS_IDENTIFICATION_BACKEND[self.comboBoxBackendSelect.currentIndex()]
        }

        try:
            self.currentBackend.setMode(mode)
            self.currentBackend.initialize(self.sbmlModel, settings)
        except Exception as e:
            logging.error("SimulationWorkbenchController: Can't initialize integrator. Error: %s" % e)
            raise

    def setUpInputFields(self):
        """
        Sets up various input fields with their standard values (that have been previously loaded
        into class variables).
        """
        self.lineEditStartTime.setText(str(self.optionStartTime))
        self.lineEditEndTime.setText(str(self.optionEndTime))
        self.lineEditRTOL.setText(str(self.optionRTOL))
        self.lineEditATOL.setText(str(self.optionATOL))
        self.lineEditXTOL.setText(str(self.optionXTOL))
        self.lineEditMaxNumNewtonSteps.setText(str(self.optionMaxNumNewtonSteps))

        self.comboBoxJacobianSelect.setCurrentIndex(int(self.optionJACGEN) - 1) # todo: switch to 0-based counting
        self.comboBoxProblemTypeSelect.setCurrentIndex(int(self.optionNONLIN) - 1) # todo: switch to 0-based counting
        self.comboBoxResidualScalingSelect.setCurrentIndex(int(self.optionRSCAL) - 1) # todo: switch to 0-based counting

        self.comboBoxParameterConstraintsSelect.setCurrentIndex(backend.settingsandvalues.OPTIONS_PARAMETER_CONSTRAINT_TYPES.index(self.optionParameterConstraints))
        self.lineEditConstLowerBound.setText(str(self.optionParameterConstraintsLowerbound))
        self.lineEditConstUpperBound.setText(str(self.optionParameterConstraintsUpperbound))


    def _getCurrentBackend(self, getNew=False):
        if not self.backendBioParkinCpp or getNew:
            del self.backendBioParkinCpp # explicitely destroy the old backend object
            self.backendBioParkinCpp = None
            self.backendBioParkinCpp = ParkinCppBackend()
        return self.backendBioParkinCpp

        # 2011-09-13: The approach changed. The drop down is no longer used
        # to select a different backend but to set a mode *within*
        # the PARKINcpp backend (done during self._setUpBackend())




    ####### functionality for handling experimental data #######


    def updateExpData(self, readFile=False):
        if readFile:
            self.currentExpDataFilename = self.lineEditExpData.text()
            format = self.getExpDataFileFormat()

            self.dataService.load_data([self.currentExpDataFilename], type=services.dataservice.EXPERIMENTAL,
                parkinController=self.parkinController,
                format=format)

        expData = self.dataService.get_experimental_data()
        self.showExpDataInfo(expData)

    def getExpDataFileFormat(self):
        filename = self.currentExpDataFilename
        if filename.endswith("csv") or filename.endswith("txt"):
            format = datamanagement.dataset.FORMAT_EXP_SIMPLE_CSV
        elif filename.endswith("dat"):
            format = datamanagement.dataset.FORMAT_EXP_PARKIN
        else:
            format = None

        return format


    def showExpDataInfo(self, expData):
        if not expData:
            logging.debug("SimulationWorkbenchController - showExpDataInfo: No data")
            self.tableWidgetExpData.setColumnCount(0)
            self.tableWidgetExpData.setRowCount(0)
            return

        expDataTableColHeaders = []
        expDataTableRowHeaders = ["# Species", "Format", "Select"]
        tableData = []
        self.currentExpData = []
        for key, dataSet in expData.items():
            expDataTableColHeaders.append(key)
            currentData = [dataSet.getNumOfRealData(), dataSet.getFormat(), dataSet.isSelected()]
            self.currentExpData.append(dataSet)
            tableData.append(currentData)

        self.tableWidgetExpData.setColumnCount(len(expDataTableColHeaders))
        self.tableWidgetExpData.setRowCount(len(expDataTableRowHeaders))
        self.tableWidgetExpData.setHorizontalHeaderLabels(expDataTableColHeaders)
        self.tableWidgetExpData.setVerticalHeaderLabels(expDataTableRowHeaders)

        for col in xrange(len(tableData)):
            for row in xrange(len(tableData[col])):
                data = tableData[col][row]
                if type(data) != bool:
                    newItem = QTableWidgetItem(str(data))
                    newItem.setFlags(Qt.ItemIsEnabled)
                    self.tableWidgetExpData.setItem(row, col, newItem)
                else:
                    newItem = QTableWidgetItem(QTableWidgetItem.Type)
                    newItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    if data:
                        newItem.setCheckState(Qt.Checked)
                    else:
                        newItem.setCheckState(Qt.Unchecked)
                    newItem.setTextAlignment(Qt.AlignCenter)
                    self.tableWidgetExpData.setItem(row, col, newItem)

    def plotExpData(self, data=None):
        logging.info("Creating Experimental Data Plot...")
        if not self.resultsWindow:
            self.resultsWindow = ResultsWindowController(None)

        if not data:
            data = self.dataService.get_selected_experimental_data()

        plotWidgetExp = PlotWidgetController(parent=self.resultsWindow.getMdiArea(), host=self,
            title="Experimental (Plot) - %s" % time.strftime("%H:%M:%S", time.localtime()))
        plotWidgetExp.setPlotStyle(simulationworkbench.widgets.plotwidgetcontroller.PLOT_POINT)
        plotWidgetExp.updateDataSources(data)   #also plots the data; accepts single dataDict and lists
        self.resultsWindow.addResultSubWindow(plotWidgetExp)


    def updateStatusBar(self, msg, time=1000):
        self.statusBarService.showMessage(msg, time)

    def updateSelectedExpData(self):
        # TODO!
        try:
            return len(self.dataService.get_experimental_data())
        except:
            return 0


    def getListOfParameterSets(self):
        if self.sbmlModel:
            return self.sbmlModel.ListOfParameterSets
        return None


    def setUpDataBrowser(self):
        """
        Adds the small "Load Data UI" to the start "+" tab.
        Also hides the close button of that tab.
        """
        dataImportWidget = DataImportWidget(self.dataBrowserPlusTab, self.parkinController)
        dataImportWidget.updatedDataEvent.connect(self.updateDataBrowser)
        self.dataBrowserTabWidget.addTab(dataImportWidget,"+") # I create the tab here, because the layout is funky, otherwise

        self.dataBrowserTabWidget.removeTab(0)  # remove the tab placed their by default

        # hide the close button of the always-visible "+" tab
        self.dataBrowserTabWidget.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # connect tab close signal
        self.dataBrowserTabWidget.tabCloseRequested.connect(self.on_dataBrowserTabCloseRequested)

        self.dataService.newData.connect(self.on_newData)


    def computeDetailedSensitivities(self, timepoints):
        try:
            self._setUpBackend(mode=backend.settingsandvalues.MODE_SENSITIVITIES_DETAILS)
            if not self.currentBackend:
                return
            self.currentBackend.setParamsForSensitivity(self.parametersTableModel.paramsToSensitivityMap)
            self.currentBackend.setTimepointsForDetailedSensitivities(timepoints)
            if self.optionsService.getDebug():
                self.currentBackend.run() # for debugging (to be able to set breakpoints):
            else:
                self.currentBackend.start()  # using the threading mechanism
        except InitError:
            logging.error("Computation aborted. Couldn't initialize integrator.")
        except Exception, e:
            logging.error("Computation aborted. Exception: %s" % e)
            raise


    def initializeThresholdsSpecies(self):
        if not self.sbmlModel:
            logging.info("No model loaded. Can't set species thresholds.")
            return
        
        if not self.askForThresholdConfirmation():
            return

        for species in self.sbmlModel.SbmlSpecies:
            species.setThreshold(self.machineEpsilon)
        self.speciesTableModel.layoutChanged.emit()

    def initializeThresholdsParameters(self):
        if not self.sbmlModel:
            logging.info("No model loaded. Can't set parameter thresholds.")
            return

        if not self.askForThresholdConfirmation():
            return

        for param in self.sbmlModel.SbmlParameters:
            param.setThreshold(self.machineEpsilon)
        self.parametersTableModel.layoutChanged.emit()


    def askForThresholdConfirmation(self):
        # show warning dialog
        msgBox = QMessageBox()
        infoText =\
        """<b>The threshold describes the value below which an absolute error concept is applied to the respective Species/Parameter.</b><br>
        <br>
        Ideally, thresholds should be set <b>by hand</b>.<br>
        <br>
        If you select Yes, all thresholds will be set to the current machine accuracy (which depends on operating system and CPU).<br>
        <br>
        Please, be aware that these default values <b>might not be the correct choice</b>. To ensure correct results (e.g. sensitivities), set a sensible threshold.<br>
        """
        msgBox.setText(infoText)
        infoTextShort = "Do you want to set all thresholds to default values?"
        msgBox.setInformativeText(infoTextShort)
        msgBox.setWindowTitle(infoTextShort)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        msgBox.setIcon(QMessageBox.Question)
        clickedButton = msgBox.exec_()

        if clickedButton == QMessageBox.No:
            return False

        return True


    ######### SLOTS ###########


    @Slot("")
    def on_actionSimulate_triggered(self):

        if not self.sbmlModel:
            logging.info("No model loaded. No simulation possible.")
            return
        try:
            self._setUpBackend(mode=backend.settingsandvalues.MODE_INTEGRATE)
            if not self.currentBackend:
                logging.info("Can't create backend. No simulation possible.")
                return
            if self.optionsService.getDebug():
                self.currentBackend.run() # for debugging (to be able to set breakpoints):
            else:
                self.currentBackend.start()  # using the threading mechanism
        except InitError:
            logging.error("Computation aborted. Couldn't initialize integrator.")
            self.updateStatusBar("Simulation aborted...")
        except Exception, e:
            logging.error("Computation aborted. Exception: %s" % e)
            self.updateStatusBar("Simulation aborted...")
            raise


    @Slot("")
    def on_actionComputeSensitivityOverview_triggered(self):

        if not self.sbmlModel:
            logging.info("No model loaded. No sensitivity computation possible.")
            return
        try:
            self._setUpBackend(mode=backend.settingsandvalues.MODE_SENSITIVITIES_OVERVIEW)
            if not self.currentBackend:
                logging.info("Can't create backend. No sensitivity computation possible.")
                return
            self.currentBackend.setParamsForSensitivity(self.parametersTableModel.paramsToSensitivityMap)
            if self.optionsService.getDebug():
                self.currentBackend.run() # for debugging (to be able to set breakpoints):
            else:
                self.currentBackend.start()  # using the threading mechanism
        except InitError:
            logging.error("Computation aborted. Couldn't initialize integrator.")
        except Exception, e:
            logging.error("Computation aborted. Exception: %s" % e)
            raise

    @Slot("")
    def on_actionCompute_Detailed_Sensitivities_triggered(self):
        """
        Instantiates a TimepointChooser and let's the user
        choose timepoints. :)
        The dialog's accepted SIGNAL is connected to
        self.on_timeChooser_accepted().
        """

        if not self.sbmlModel:
            logging.info("No model loaded. No sensitivity computation possible.")
            return

        if not self.timepointChooser:
            self.timepointChooser = TimepointChooser(self, startTime=self.optionStartTime, endTime=self.optionEndTime)
            self.timepointChooser.accepted.connect(self.on_timeChooser_accepted)
        else:
            self.timepointChooser.setStartAndEndTime(startTime=self.optionStartTime, endTime=self.optionEndTime)
        self.timepointChooser.show()
        self.timepointChooser.raise_()
        self.timepointChooser.activateWindow()

    def on_timeChooser_accepted(self):
        """
        This is called when the TimepointChooser was
        successfully (hopefully) used to select timepoints.
        This initiates the computation of "detailed sensitivities".
        """
        timepoints = self.timepointChooser.getTimepoints()
        self.computeDetailedSensitivities(timepoints)


    @Slot("")
    def on_actionEstimateParameterValues_triggered(self):
        """
        Starts the parameter value estimation.
        """

        if not self.sbmlModel:
            logging.info("No model loaded. No parameter identification possible.")
            return
        try:
            self._setUpBackend(mode=backend.settingsandvalues.MODE_PARAMETER_ESTIMATION)
            self.currentBackend.setParamsForEstimation(self.parametersTableModel.paramToEstimateMap)
            if self.optionsService.getDebug():
                self.currentBackend.run() # for debugging (to be able to set breakpoints):
            else:
                self.currentBackend.start()  # using the threading mechanism
        except InitError:
            logging.error("Computation aborted. Couldn't initialize PARKINcpp library.")
        except Exception, e:
            logging.error("Computation aborted. Exception: %s" % e)
            raise


    @Slot(int)
    def on_comboBoxBackendSelect_currentIndexChanged(self, index):
        if index == 1: # parkin
            self.labelJACGEN.setEnabled(False)
            self.comboBoxJacobianSelect.setEnabled(False)
            self.labelNONLIN.setEnabled(False)
            self.comboBoxProblemTypeSelect.setEnabled(False)
            self.labelRSCAL.setEnabled(False)
            self.comboBoxResidualScalingSelect.setEnabled(False)
        else: # nlscon
            self.labelJACGEN.setEnabled(True)
            self.comboBoxJacobianSelect.setEnabled(True)
            self.labelNONLIN.setEnabled(True)
            self.comboBoxProblemTypeSelect.setEnabled(True)
            self.labelRSCAL.setEnabled(True)
            self.comboBoxResidualScalingSelect.setEnabled(True)

    @Slot(bool)
    def on_checkBoxPlotExpData_toggled(self, selected):
        self.optionPlotExpDataOnSimulation = selected
        self.checkBoxPlotExpDataDataBrowser.setChecked(selected)

    @Slot(bool)
    def on_checkBoxPlotExpDataDataBrowser_toggled(self, selected):
        self.optionPlotExpDataOnSimulation = selected
        self.checkBoxPlotExpData.setChecked(selected)

    @Slot("")
    def on_lineEditStartTime_editingFinished(self):
        """
        Ensures that only floats are entered into the start time field.
        """
        try:
            self.optionStartTime = float(self.lineEditStartTime.text())
        except:
            #self.lineEditStartTime.setText(str(parkinintegrator.DEFAULT_STARTTIME))
            self.lineEditStartTime.setText(str(self.optionStartTime))   #set last valid value



    @Slot("")
    def on_lineEditEndTime_editingFinished(self):
        """
        Ensures that only floats are entered into the EndTime field.
        """
        try:
            self.optionEndTime = float(self.lineEditEndTime.text())
        except:
            self.lineEditEndTime.setText(str(self.optionEndTime))



    @Slot("")
    def on_lineEditRTOL_editingFinished(self):
        """
        Ensures that only floats are entered into the lineEditRTOL field.
        """
        try:
            self.optionRTOL = float(self.lineEditRTOL.text())
        except:
            self.lineEditRTOL.setText(str(self.optionRTOL))



    @Slot("")
    def on_lineEditATOL_editingFinished(self):
        """
        Ensures that only floats are entered into the lineEditATOL field.
        """
        try:
            self.optionATOL = float(self.lineEditATOL.text())
        except:
            self.lineEditATOL.setText(str(self.optionATOL))



    @Slot("")
    def on_lineEditXTOL_editingFinished(self):
        '''
        Ensures that only floats are entered into the lineEditXTOL field.
        '''
        try:
            self.optionXTOL = float(self.lineEditXTOL.text())
        except:
            self.lineEditXTOL.setText(str(self.optionXTOL))



    @Slot("")
    def on_lineEditTimeUnit_editingFinished(self):
        """
        Ensures that only strings are entered into the lineEditTimeUnit field.
        """
        try:
            self.optionTimeUnit = str(self.lineEditTimeUnit.text())
        except:
            self.lineEditTimeUnit.setText(str(self.optionTimeUnit))


    @Slot("")
    def on_lineEditConstLowerBound_editingFinished(self):
        """
        Ensures that only floats are entered into the lineEditConstLowerBound field.
        """
        try:
            self.optionParameterConstraintsLowerbound = float(self.lineEditConstLowerBound.text())
        except:
            self.lineEditConstLowerBound.setText(str(self.optionParameterConstraintsLowerbound))

    @Slot("")
    def on_lineEditConstUpperBound_editingFinished(self):
        """
        Ensures that only floats are entered into the lineEditConstLowerBound field.
        """
        try:
            self.optionParameterConstraintsUpperbound = float(self.lineEditConstUpperBound.text())
        except:
            self.lineEditConstUpperBound.setText(str(self.optionParameterConstraintsUpperbound))





    def backendRunFinished(self, text):
        self.updateStatusBar("Updating results...")
        if text == backend.settingsandvalues.FINISHED_INTEGRATION:
            self._createSimulationDataTable()
            self._createSimulationPlot()
        elif text == backend.settingsandvalues.FINISHED_SENSITIVITY_OVERVIEW:
            self._createSensitivityOverviewPlot()
        elif text == backend.settingsandvalues.FINISHED_SENSITIVITY_DETAILS:
            self._createSensitivityDetailsTable()
        elif text == backend.settingsandvalues.FINISHED_PARAMETER_ESTIMATION:
            self._createEstimatedParametersTable()

        self.updateStatusBar("Results updated.", 5000)


    def speciesChanged(self, upperLeftindex, lowerRightIndex):
        return


    def parameterChanged(self, upperLeftIndex, lowerRightIndex):
        return

    @Slot("")
    def on_comboBoxJacobianSelect_currentIndexChanged(self):
        self.optionJACGEN = self.comboBoxJacobianSelect.currentIndex() + 1

    @Slot("")
    def on_comboBoxProblemTypeSelect_currentIndexChanged(self):
        self.optionNONLIN = self.comboBoxProblemTypeSelect.currentIndex() + 1

    @Slot("")
    def on_comboBoxResidualScalingSelect_currentIndexChanged(self):
        self.optionRSCAL = self.comboBoxResidualScalingSelect.currentIndex() + 1

    @Slot("int")
    def on_comboBoxParameterConstraintsSelect_currentIndexChanged(self, index):
        self.optionParameterConstraints = backend.settingsandvalues.OPTIONS_PARAMETER_CONSTRAINT_TYPES[index]

        if self.optionParameterConstraints == backend.settingsandvalues.OPTION_PARAMETER_CONSTRAINT_NONE: # no constraints
            self.labelConstLowerBound.setEnabled(False)
            self.labelConstUpperBound.setEnabled(False)
            self.lineEditConstLowerBound.setEnabled(False)
            self.lineEditConstUpperBound.setEnabled(False)
        elif self.optionParameterConstraints == backend.settingsandvalues.OPTION_PARAMETER_CONSTRAINT_POSITIVITY: # positivity
            self.labelConstLowerBound.setEnabled(False)
            self.labelConstUpperBound.setEnabled(False)
            self.lineEditConstLowerBound.setEnabled(False)
            self.lineEditConstUpperBound.setEnabled(False)
        if self.optionParameterConstraints == backend.settingsandvalues.OPTION_PARAMETER_CONSTRAINT_LOWERBOUND: #lower bound
            self.labelConstLowerBound.setEnabled(True)
            self.labelConstUpperBound.setEnabled(False)
            self.lineEditConstLowerBound.setEnabled(True)
            self.lineEditConstUpperBound.setEnabled(False)
        if self.optionParameterConstraints == backend.settingsandvalues.OPTION_PARAMETER_CONSTRAINT_UPPERBOUND: #upper bound
            self.labelConstLowerBound.setEnabled(False)
            self.labelConstUpperBound.setEnabled(True)
            self.lineEditConstLowerBound.setEnabled(False)
            self.lineEditConstUpperBound.setEnabled(True)
        if self.optionParameterConstraints == backend.settingsandvalues.OPTION_PARAMETER_CONSTRAINT_INTERVAL:  # interval
            self.labelConstLowerBound.setEnabled(True)
            self.labelConstUpperBound.setEnabled(True)
            self.lineEditConstLowerBound.setEnabled(True)
            self.lineEditConstUpperBound.setEnabled(True)





    def selectAllSensitivity(self, doSelect):
        if self.parametersTableModel:
            self.parametersTableModel.selectAllSensitivity(doSelect)

    def invertSelectionSensitivity(self):
        if self.parametersTableModel:
            self.parametersTableModel.invertSelectionSensitivity()


    def selectAllSensitivitySpecies(self, doSelect):
        if self.speciesTableModel:
            self.speciesTableModel.selectAllSensitivity(doSelect)

    def invertSelectionSensitivitySpecies(self):
        if self.speciesTableModel:
            self.speciesTableModel.invertSelectionSensitivity()


    def selectAllEstimation(self, doSelect):
        if self.parametersTableModel:
            self.parametersTableModel.selectAllEstimation(doSelect)

    def invertSelectionEstimation(self):
        if self.parametersTableModel:
            self.parametersTableModel.invertSelectionEstimation()

    ##### Other SLOTs ####


    @Slot("")
    def on_actionSelectAllParametersForSensitivity_triggered(self):
        self.selectAllSensitivity(True)

    @Slot("")
    def on_actionDeselectAllParametersForSensitivity_triggered(self):
        self.selectAllSensitivity(False)


    @Slot("")
    def on_actionInvertSelectionOfParametersForSensitivity_triggered(self):
        self.invertSelectionSensitivity()


    @Slot("")
    def on_actionSelectAllSpeciesForSensitivity_triggered(self):
        self.selectAllSensitivitySpecies(True)

    @Slot("")
    def on_actionDeselectAllSpeciesForSensitivity_triggered(self):
        self.selectAllSensitivitySpecies(False)

    @Slot("")
    def on_actionInvertSelectionOfSpeciesForSensitivity_triggered(self):
        self.invertSelectionSensitivitySpecies()


    @Slot("")
    def on_actionSelect_All_Parameters_for_Estimation_triggered(self):
        self.selectAllEstimation(True)

    @Slot("")
    def on_actionDeselect_All_Parameters_for_Estimation_triggered(self):
        self.selectAllEstimation(False)

    @Slot("")
    def on_actionInvert_Selection_of_Parameters_for_Estimation_triggered(self):
        self.invertSelectionEstimation()


        #### SLOTs and methods for handling parameter set interactions ####

    @Slot("")
    def on_actionDuplicate_Parameter_Set_triggered(self):
        if self.getListOfParameterSets():
            self.getListOfParameterSets().createNewParameterSet(duplicate=True)

    @Slot("")
    def on_actionRemove_Parameter_Set_triggered(self):
        if self.getListOfParameterSets():
            self.getListOfParameterSets().removeParameterSet()


    #### Data Browser-related SLOTs ####

    def updateDataBrowser(self, expData):
        """
        Go through *all* the loaded experimental data
        and create tabs for data for which no tab yet exists.

        @todo: Make the whole managing of data more sensible (especially within
        DataService, so that it's easy to get only "new" data after something [e.g. a file]
        has been loaded).
        """
        if not expData:
            return

        for filepath, data in expData.items():
            logging.debug("SimulationWorkbenchController.updateDataBrowser: Handling data from file %s" % filepath)
            # todo: is the filename a good identifier in this case? what about data that is not from a file...?
            if filepath in self.dataBrowserWidgets.keys():  # there's already a tab for that data
                continue

            # create tab for data
            dataBrowser = DataBrowser(None, filepath, data) # provide no parent here; normal way of adding tabs
            dataBrowser.setSimulationWorkbench(self)
            self.dataBrowserWidgets[filepath] = dataBrowser

            if "/" in filepath:
                tabID = filepath.rsplit("/", 1)[1]
            else:
                tabID = filepath
            numTabs = self.dataBrowserTabWidget.count()
            self.dataBrowserTabWidget.insertTab(numTabs - 1, dataBrowser,
                tabID) # returns index of new tab; not needed here
            self.dataBrowserTabWidget.setCurrentIndex(numTabs - 1)

            tabBar = self.dataBrowserTabWidget.tabBar()
            tabBar.setTabButton(numTabs - 1, QTabBar.LeftSide, dataBrowser.getSelectionCheckBox())

    def on_dataBrowserTabCloseRequested(self, tabIndex):
        """
        This Slot is called when the user klicks on the "close tab"
        icon of a Data Browser tab.
        It cleans up references (e.g. in the self.dataBrowserWidgets
        management dict), asks the Data Browser to remove itself
        (e.g. internal clean up) and, finally, removes the tab.
        The data that was shown inside the tab is also removed from
        the DataService.
        """
        dataBrowser = self.dataBrowserTabWidget.widget(tabIndex)
        self.dataBrowserWidgets.pop(dataBrowser.getId())
        self.dataService.remove_data(dataBrowser.data)
        dataBrowser.remove()
        self.dataBrowserTabWidget.removeTab(tabIndex)


    @Slot("")
    def on_buttonPlotAllData_clicked(self):
        data = self.dataService.get_experimental_data()
        self.plotExpData(data)


    @Slot("")
    def on_buttonPlotSelectedData_clicked(self):
        self.plotExpData()


    @Slot("")
    def on_buttonInitializeThresholdsSpecies_clicked(self):
        self.initializeThresholdsSpecies()

    @Slot("")
    def on_buttonInitializeThresholdsParameters_clicked(self):
        self.initializeThresholdsParameters()

    def on_newData(self, dataSet):
        if dataSet.type == dataservice.EXPERIMENTAL: # display exp. data in data browser
            self.updateDataBrowser({dataSet.getId(): dataSet})