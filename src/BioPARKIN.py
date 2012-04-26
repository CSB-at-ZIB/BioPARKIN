#!/usr/bin/env python


# this might (or might not... don't ask, it's complicated ;)) enable debugging of threads
#import pydevd
#pydevd.settrace(suspend=False)
#import threading
#threading.settrace(pydevd.GetGlobalDebugger().trace_dispatch)


# Note: most commented-out code in this class has to do with creating/managing the network views
# This is the reason why I left the commented code in here although it looks ugly. It can serve as a guideline
# for reenabling graphical network views and hooking them up with the currently selected model, etc.
#import networkx # not used for now

import PySide
from PySide.QtCore import Signal, QSettings, QFile, QFileInfo, Slot, Qt
from PySide.QtGui import QMainWindow, QAction, QFileDialog, QMessageBox, QApplication, QKeySequence
import os
import matplotlib
import sys
import time
import traceback
import Image
import logging
import logging.handlers
from services.optionsservice import OptionsService


try:
    import ctypes # for handling Windows7-specific task bar icon behaviour
except:
    pass

from services.warningservice import WarningService
from sbml_views.warningsdialog import WarningsDialog
from basics.logging.statusbarlogginghandler import StatusBarLoggingHandler
from services.statusbarservice import StatusBarService
from aboutdialog import AboutDialog
from basics.helpers import filehelpers
from sbml_views.modelview import ModelView
#from sbml_networkview.networkviewcontroller import NetworkViewController # not used for now
from libsbml import LIBSBML_VERSION_STRING
from services.dataservice import DataService
from sbml_model.modelcontroller import ModelController
from services.progressbarservice import ProgressBarService, DummyProgressThread, DummyThrobberThread
from sbml_views.sbmlentitywidget import SBMLEntityWidget
from sbml_views.entitytableview import EntityTableView
from simulationworkbench.simulationworkbenchcontroller import SimulationWorkbenchController
from odehandling.odeviewer import ODEViewer
from Ui_BioPARKIN_v2 import Ui_MainWindow
from datamanagement import datahandling
from optparse import OptionParser


OPTION_DEBUG = "debug"  # don't rename!

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s')

_LOG_FILENAME = "./bioparkin_log.txt"
NUM_RECENT_FILES = 6

class BioParkinController(QMainWindow, Ui_MainWindow):
    """
    This is the heart of BioParkin. It sets up the general UI
    (MainWindow, some Views, ...), handles creation and management of
    individual network windows, and instantiates needed services
    (for easy access to data, status bar, ...).

    This class inherits from QMainWindow for its functionality and from
    the (automatically generated) Ui_MainWindow for the design of the UI
    (including the self.setupUi() method).

    @param parent: The standard Qt parent.
    @type parent: QWidget

    @organization: Zuse Insitute Berlin
    """

    __version__ = "1.2.19"
    __author__ = "Moritz Wade & Thomas Dierkes"
    __contact__ = "wade@zib.de or dierkes@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    newNetworkWindowCreated = Signal()
    networkWindowRaised = Signal()
    activeModelChanged = Signal(ModelController)
    modelClosed = Signal(ModelController)


    def __init__(self, args, parent=None):
        """
        This initialization does a lot of stuff. :)

        * State variables are set up
        * Views are created and tied to UI parts (e.g. Docks)
        * Logging is set up
        * Services (StatusBar, Data, ...) are started
        * Necessary slots are connected

        """
        super(BioParkinController, self).__init__(parent)

        # for locale testing
        #locale.setlocale(locale.LC_ALL, 'de_DE')
        #        locale.setlocale(locale.LC_ALL, 'deu_deu')

        self.startTime = time.localtime()


        # set file logger
        self.rotatingFileHandler = logging.handlers.RotatingFileHandler(_LOG_FILENAME,
                                                       maxBytes=1000000,
                                                       backupCount=5)
        self.rotatingFileHandler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        self.logger = logging.getLogger() #gets root logger
        self.logger.addHandler(self.rotatingFileHandler)

        # Status bar logger
        self.statusBarLoggingHandler = StatusBarLoggingHandler()
        self.statusBarLoggingHandler.setLevel(logging.INFO) # only log on info level
        self.logger.addHandler(self.statusBarLoggingHandler)

        # parse command line arguments
        parser = OptionParser()
        parser.add_option("-d", "--debug",
                  action="store_true", dest=OPTION_DEBUG, default=False,
                  help="Include debugging information in console and file log")
        self.options, args = parser.parse_args()

        self.optionsService = OptionsService()
        self.optionsService.setDebug(self.options.debug)

        # set logging options
        if self.options.debug:
            self.logger.setLevel(logging.DEBUG)
            self.rotatingFileHandler.setLevel(logging.DEBUG)
            logging.info("Debug logging active.")
        else:
            self.logger.setLevel(logging.INFO)
            self.rotatingFileHandler.setLevel(logging.INFO)
            logging.info("Debug logging not active.")

        logging.info("Starting BioPARKIN... %s" % self.startTime)

        ##### LOGGING #####
        logging.info("BioPARKIN started (version %s)" % BioParkinController.__version__)
        logging.info("Command line arguments: %s" % args)
        logging.info("Python version: %s" % sys.version)
        logging.info("PySide version: %s" % PySide.__version__)
        logging.info("libSBML version: %s" % LIBSBML_VERSION_STRING)
        logging.info("Matplotlib version: %s" % matplotlib.__version__)
#        logging.info("NetworkX version: %s" % networkx.__version__)
        logging.info("Python Image Library version: %s" % Image.VERSION)






        self.setupUi(self)
        self._mdiArea.hide()
        self.setWindowTitle("BioPARKIN v%s" % BioParkinController.__version__)

        # restore previous settings
        settings = QSettings()
        try:
            self.recentFiles = settings.value("RecentFiles", [])

            # handles the case if only one file is in the "list" in Linux (it's retrieved as unicode string in this case)
            if type(self.recentFiles) is str or type(self.recentFiles) is unicode:
                self.recentFiles = [self.recentFiles]
                
            logging.info("Recently opened files: %s" % self.recentFiles)
        except:
            logging.warning("Can't access list of recently opened files. Resetting the list.")
            self.recentFiles = []

        self.updateFileMenu()
        self.aboutDialog = None

        geometry = settings.value("Geometry")
        if geometry:
            self.restoreGeometry(geometry)

        state = settings.value("MainWindow/State")
        if state:
            self.restoreState(state)


        self.ModelControllers = {}
#        self.SubWindowToModelControllers = {}
#        self.NetworkWindowCount = 0
#        self.ActiveNetworkWindow = None
        self.ActiveModelController = None
#        self.networkSubWindows = {}

        self.integrator = None
        self.odeViewer = None

        self.ModelView = ModelView(self.masterDetailSplitter, self)
        self.ModelTreeView = SBMLEntityWidget(self.masterDetailSplitter)
        self.EntityTableView = EntityTableView(self.masterDetailSplitter)

        self.mainWindowViews = [self.ModelTreeView, self.EntityTableView]   #used to iterate over Views



        # set up Data Service and Data Viewer
        datahandling.parkinController = self
        self.dataService = DataService()


        # debugging#############
        BASE_PATH = reduce(lambda l, r: l + os.path.sep + r,
                           os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1])

        # add ../../templates (relative to the file (!) and not to the CWD)
        dataPath = os.path.join(BASE_PATH, "data")
        #######################

        self.SimulationWorkbenchController = SimulationWorkbenchController(parent=None, parkinController=self)
        self.mainTabWidget.addTab(self.SimulationWorkbenchController, "Workbench")




        # hook up status bar with progress service (that threads can connect to)
        self.statusBarService = StatusBarService(self.statusBar()) # first time, service is instantiated => give statusBar reference!
        self.progressBarService = ProgressBarService(self, self.statusBarService)

        self.statusBarLoggingHandler.setStatusBar(self.statusBarService)

        self.warningsService = WarningService.getInstance()
        self.warningsDialog = WarningsDialog(self, self.actionShow_Warnings, self.warningsService)


        # register signals
        self.activeModelChanged.connect(self.on_activeModelChanged)
        self.modelClosed.connect(self.on_modelClosed)
        self.menuFile.aboutToShow.connect(self.updateFileMenu)


        # for debugging
        self.dummyThread = None

        try:    # try to set correct taskbar icon in Windows 7
            myappid = 'ZIB.BioPARKIN' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass


    def updateFileMenu(self):
        """
        Updates the file menu dynamically, so that recent files can be shown.
        """
        self.menuFile.clear()
#        self.menuFile.addAction(self.actionNew)    # disable for now
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionClose_Model)

        recentFiles = []
        for filename in self.recentFiles:
            if QFile.exists(filename):
                recentFiles.append(filename)

        if len(self.recentFiles) > 0:
            self.menuFile.addSeparator()
            for i, filename in enumerate(recentFiles):
                action = QAction("&%d %s" % (i + 1, QFileInfo(filename).fileName()), self)
                action.setData(filename)
                action.setStatusTip("Opens recent file %s" % QFileInfo(filename).fileName())
                action.setShortcut(QKeySequence(Qt.CTRL | (Qt.Key_1+i)))
                action.triggered.connect(self.load_model)
                self.menuFile.addAction(action)

        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)

    def new_model(self):
        """
        Not yet supported.
        """
        pass


    def load_model(self, filename=None):
        """
        Loads a given SBML file, thereby creating a new subwindow
        on the main MDI Area.
        If filename is None, it creates a new model.

        There are a lot of reference variables, so that the system knows the
        currently active subwindow, etc.

        @param filename: The filename of the model. If None, a new model is created.
        @type filename: str
        """
        if not filename:
            action = self.sender()
            if type(action) == QAction:
                filename = action.data()
            else:
                return


        # note: this has been (temporarily added) to allow only one file to be open at the same time
        # We will probably change this behaviour again later, once we have decided how to handle
        # multiple-model results, etc. intelligently
        if len(self.ModelControllers) > 0:

            # show warning dialog
            msgBox = QMessageBox()
            infoText =\
            """<b>Another model is currently loaded.</b><br>
            """
            msgBox.setText(infoText)
            infoTextShort = "Do you want to save the current model (you will be prompted to enter a new filename)?"
            msgBox.setInformativeText(infoTextShort)
            msgBox.setWindowTitle(infoTextShort)
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
            msgBox.setDefaultButton(QMessageBox.Save)
            msgBox.setIcon(QMessageBox.Warning)
            clickedButton = msgBox.exec_()

            if clickedButton == QMessageBox.Save:
                self.actionSave_as.trigger()


            for modelController in self.ModelControllers.values(): # close all models (in theory, there should be only one :)
                self.modelClosed.emit(modelController)



#        self.NetworkWindowCount += 1
#        self.setStatusTip("Opening file %s..." % filename)
        self.statusBar().showMessage("Opening file %s..." % filename, 2000)
        modelController = ModelController(filename=filename, views=self.mainWindowViews)

#        # create NetworkViewController
#        networkViewController = NetworkViewController(modelController=modelController)
#        networkView = networkViewController.createNetworkView(self) # sets networkController.networkView internally
#        networkView.setMinimumSize(400, 300)
#        modelController.setViews(networkViewController=networkViewController)

#        # Create Subwindow to hold the NetworkView
#        subWindow = QMdiSubWindow(parent=self._mdiArea)
#        networkViewController.subWindow = subWindow
#        subWindow.setAttribute(Qt.WA_DeleteOnClose)
#        subWindow.setWidget(networkView)
#        subWindow.setOption(QMdiSubWindow.RubberBandResize, True)
#        self._mdiArea.addSubWindow(subWindow)
#        subWindow.activateWindow()
#        subWindow.show()    # important!
#        networkView.show()

        # handle references
        filename = modelController.filename
#        self.SubWindowToModelControllers[subWindow] = modelController
#        self.networkSubWindows[modelController] = subWindow #networkView
        self.ModelControllers[filename] = modelController
#        self.ActiveNetworkWindow = networkWindow
        self.ActiveModelController = modelController

#        self.connectNetworkWindowSignals(networkView, subWindow)

        # emit custom Signal so that e.g. Simulationworkbench are notified of the new subwindow
#        self.newNetworkWindowCreated.emit()
        self.activeModelChanged.emit(modelController)

        # handle recent files list
        if filename in self.recentFiles:
            self.recentFiles.remove(filename)
        self.recentFiles.insert(0, filename)
        if len(self.recentFiles) > NUM_RECENT_FILES:    # cap list at length of NUM_RECENT_FILES
            self.recentFiles = self.recentFiles[:NUM_RECENT_FILES]

#    def getMdiArea(self):
#        return self._mdiArea

#    @Slot("QWidget")
#    def connectNetworkWindowSignals(self, networkWindow, subWindow):
#        """
#        Connect the signals of network windows (e.g. network is about to be destroyed, etc.)
#
#        @param networkWindow: A network view
#        @type networkWindow: NetworkView
#
#        @param subWindow: A Qt QMdiArea sub window
#        @type subWindow: QMdiSubWindow
#        """
#        #self.connect(button3, SIGNAL("clicked()"),    lambda who="Three": self.anyButton(who))
#
#        self.connect(networkWindow, SIGNAL("destroyed()"),
#                     lambda who=networkWindow: self.on_networkwindow_destroyed(who))

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('Filename'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Handles the drop event if the user "drops" a file somewhere within BioPARKIN's window.
        """
        # get filename
        uris = event.mimeData().urls()  # support opening several models at once

        # note: uncomment this, to enable drag'n'dropping of multiple models again
#        for uri in uris:
#            filename = uri.toLocalFile()
#            #open file
#            self.load_model(filename)
        filename = uris[0].toLocalFile()
        self.load_model(filename)
        if len(uris)>1:
            logging.info("You dragged more than one model to BioPARKIN. Currently, only one model is supported to be opened at the same time. Only the first dragged model was loaded.")

    def on_modelClosed(self, modelController):
        """
        Whenever the Signal self.modelClosed is emitted, this
        method is called.
        It removes the modelController of the closed model from
        the management dictionary and updates all local Views.
        """
        if not modelController:
            logging.info("Can't close the model. No model selected.")

            #### abusing this place for testing ####
#            self.dummyThread = DummyProgressThread()
#            self.progressBarService.connect_to_thread(self.dummyThread)
#            self.dummyThread.start()

#            self.dummyThread = DummyThrobberThread()
#            self.progressBarService.connect_to_thread(self.dummyThread)
#            self.dummyThread.start()
            

            ########################################

            return
        if self.ModelControllers.has_key(
            modelController.filename): # we do this to remove the model controller from the management dict
            self.ModelControllers.pop(modelController.filename)

        if len(self.ModelControllers) == 0:
#            self.dataService.remove_all_simulated_data()
            self.ActiveModelController = None
            for view in self.mainWindowViews:
                view.setModel(None)

#    def on_networkwindow_destroyed(self, networkWindow):
#        """
#        This is a slot. It's called to clean things up when a network
#        window is destroyed. Basically, it just gets the correct ModelController
#        and passes it on using the modelClosed signal of the BioPARKIN controller.
#
#        @param networkWindow: A network view
#        @type networkWindow: NetworkView
#        """
#        logging.debug("Destroying a NetworkWindow: %s" % networkWindow)
#        modelController = networkWindow.controller.modelController
#        self.modelClosed.emit(modelController)
#
#    def closeNetworkWindow(self, modelController):
#        if self.networkSubWindows.has_key(modelController): # might have been removed already
#            self.networkSubWindows.pop(modelController).close() #removes window from dict and closes it


    def on_activeModelChanged(self, activeModelController):
        """
        Whenever the active model changes, the appropriate Signal
        self.activeModelChanged should be emitted. When that is done, this method
        is called.
        """
        logging.info("Active Model: %s" % activeModelController.filename)
        if activeModelController is not None:
            self.ActiveModelController = activeModelController
            for view in self.mainWindowViews:
                view.setModel(self.ActiveModelController.proxyModel, mainModel=self.ActiveModelController.sbmlModel)
                view.setSelectionModel(self.ActiveModelController.selectionModel)

#    def selectNetworkView(self, modelController):
#        subwindow = self.networkSubWindows[modelController]
##        subwindow.show()
#        subwindow.raise_()
#        subwindow.activateWindow()
##        subwindow.setFocus()

#    def on_networkwindow_raised(self, subWindow):
#        """
#        This is a slot. It's called when a network window gets focus.
#        Some references have to be set, and most importantly, all the Views
#        have to be switched so that they use the data model behind the
#        newly focused network window.
#
#        @param subWindow: A sub window
#        @type subWindow: QMdiSubWindow
#        """
#        if subWindow is None:
#            return
#        if not self.SubWindowToModelControllers.has_key(subWindow):
#            return
#
#        activeModelController = self.SubWindowToModelControllers[subWindow]
##        self.ActiveNetworkWindow = self.ActiveModelController.getNetworkView()
#
##        self.on_activeModelChanged()
#        self.activeModelChanged.emit(activeModelController)
##        self.networkWindowRaised.emit()
#
##        logging.debug("Leaving on_networkwindow_raised()")


    @Slot("")
    def on_actionNew_triggered(self):
        """
        This is a slot. It's automatically connected to the actionNew
        created in the QtDesigner.
        """
        self.new_model()

    @Slot("")
    def on_actionOpen_triggered(self):
        """
        This is a slot. It's automatically connected to the actionOpen
        created in the QtDesigner.
        """
        homeDir = filehelpers.getHomeDir()

        filenameTuple = QFileDialog.getOpenFileName(parent=self,
                                               directory=homeDir,
                                               filter="SBML files (*.sbml *.xml)",
                                               caption="Open SBML file...")

        if filenameTuple and filenameTuple[0]: # if user presses cancel, the tuple exists but is two empty unicode strings.
            filename = filenameTuple[0]
            self.load_model(filename)
        else:
            logging.info("No file selected. Didn't load anything.")


    @Slot("")
    def on_actionClose_Model_triggered(self):
#        self.on_modelClosed(self.ActiveModelController)
        self.modelClosed.emit(self.ActiveModelController)

    @Slot("")
    def on_actionSave_triggered(self):
        """
        This is a slot. It's automatically connected to the actionSave
        created in the QtDesigner.
        """
        self.saveActiveNetwork(filename=None)

    @Slot("")
    def on_actionSave_as_triggered(self):
        """
        This is a slot. It's automatically connected to the actionSaveAs
        created in the QtDesigner.
        """
        if not self.ActiveModelController:
            logging.info("Can't save anything. No model loaded.")
            return
        filenameTuple = QFileDialog.getSaveFileName(parent=self,
            dir=self.ActiveModelController.filename,
            caption="Save as...",
            filter="SBML file (*.sbml)")
        if filenameTuple:
            self.saveActiveNetwork(filenameTuple[0])


    def saveActiveNetwork(self, filename=None):
        """
        Tell the currently active network controller to
        save to a file.

        @param filename: Filename of the network.
        @type filename: str
        """
        if self.ActiveModelController is None:
            logging.warning("No model loaded. Can't save anything.")
            return
        self.ActiveModelController.save(filename=filename)



    @Slot("")
    def on_actionShow_Data_Manager_triggered(self):
        """
        This is a slot. It's automatically connected to the actionShowDataManager
        created in the QtDesigner.
        """
        self.DataManagementController.show()


    @Slot("")
    def on_actionODEGenerator_triggered(self):
        """
        Open the ODE Generator information dialog.
        """
        if self.ActiveModelController and self.ActiveModelController.sbmlModel:
            self.odeViewer = ODEViewer(self, self.ActiveModelController.sbmlModel)
            self.odeViewer.show()
        else:
            logging.info("ODEs can't be shown. No model selected.")



    def closeEvent(self, event):
        """
        Override the close event to handle file saving.
        """
        if self.okToContinue(): # files will be saved in self.okToContinue()
            settings = QSettings()
            settings.setValue("Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
            settings.setValue("RecentFiles", self.recentFiles)

            event.accept()
        else:
            event.ignore()

    def okToContinue(self):
        """
        Checks if it is ok to close the application.
        The user will be prompted to save files.

        @return: True, if it is ok to continue (e.g. close the app); False, otherwise
        @rtype: bool

        @todo: Make a smart save dialog to allow the user to save only certain files.
        """
        dirtyFilenames = []
        for filename, networkController in self.ModelControllers.items():
            if networkController.Dirty:
                dirtyFilenames.append(
                    networkController.filename)   # we don't use the filename key because it might be outdated
        if len(dirtyFilenames) == 0:    #nothing to save
            return True

        reply = QMessageBox.question(self,
                                     "BioParkin - Unsaved Changes",
                                     "Unsaved changes in these files:\n\n%s\n\nDo you want to save them?" % "\n".join(
                                         dirtyFilenames),
                                     buttons=QMessageBox.SaveAll | QMessageBox.Discard | QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return False
        elif reply == QMessageBox.SaveAll:
            for networkController in self.ModelControllers:
                if networkController.Dirty:
                    networkController.save()
        return True



    ############ SLOTS for SimulationWorkbenchWidget ##############


    @Slot("")
    def on_actionSimulate_triggered(self):
        self.SimulationWorkbenchController.actionSimulate.trigger()


    @Slot("")
    def on_actionComputeSensitivityOverview_triggered(self):
        self.SimulationWorkbenchController.actionComputeSensitivityOverview.trigger()

    @Slot("")
    def on_actionCompute_Detailed_Sensitivities_triggered(self):
        self.SimulationWorkbenchController.actionCompute_Detailed_Sensitivities.trigger()

    @Slot("")
    def on_actionEstimateParameterValues_triggered(self):
        self.SimulationWorkbenchController.actionEstimateParameterValues.trigger()


    @Slot("")
    def on_actionAbout_triggered(self):
        self.aboutDialog = AboutDialog(self)
        self.aboutDialog.show()


    @Slot("")
    def on_actionShow_Results_Window_triggered(self):
        if self.SimulationWorkbenchController and self.SimulationWorkbenchController.resultsWindow:
            self.SimulationWorkbenchController.resultsWindow.show()
        else:
            logging.info("Cannot show Results Window. Nothing has been simulated, yet.")


###### end of class



def my_excepthook(type, value, tback):
    """
    Pipes all exceptions to the logger, then lets the exceptions continue on
    their normal way.

    @param value: An exception
    @type value: Exception

    @param tback: The Traceback
    @type tback: Traceback
    """
    # log the exception 
    tbackString = traceback.format_list(traceback.extract_tb(tback))
    logging.exception("\nAn exception occurred: %s\nTraceback: %s" % (value,
                                                                      tbackString))

    # then call the default handler
    sys.__excepthook__(type, value, tback)


if __name__ == '__main__':
    sys.excepthook = my_excepthook  # catch all exceptions for the logger

    app = QApplication(sys.argv)
    #set some info, just to be thorough (this stuff is mainly set in BioParkinController or the Ui_MainWindow itself).
    app.setOrganizationName("Zuse Institute Berlin")
    app.setOrganizationDomain("zib.de")
    app.setApplicationName("BioPARKIN")

    parkin = BioParkinController(sys.argv)
    parkin.show()

    app.exec_()


