from collections import OrderedDict
import logging
from PySide.QtCore import Slot, Signal
from PySide.QtGui import QWidget, QFileDialog

from basics.helpers import filehelpers
import datamanagement
import services
from services.dataservice import DataService
from simulationworkbench.widgets.Ui_dataimportwidget import Ui_DataImportWidget

class DataImportWidget(QWidget, Ui_DataImportWidget):
    """
    This is a very simple widget that provides some buttons
    to load experimental data.

    @since: 2011-08-24
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"


    updatedDataEvent = Signal(OrderedDict)

    def __init__(self, parent, parkinController):
        super(DataImportWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.currentExpDataFilename = None
        self.dataService = DataService()
        self.parkinController = parkinController

    def browseExpData(self):
        """
        Shows a file open dialog.
        """

        homeDir = filehelpers.getHomeDir()
        openDir = self.currentExpDataFilename if self.currentExpDataFilename else homeDir
        filenameTuple = QFileDialog.getOpenFileName(parent=self,
                                               caption="Browse for data file...",
                                               directory=openDir,
                                               filter="BioPARKIN CSV data file (*.csv *.txt);;Legacy PARKIN data file (*.dat);;All filetypes (*.*")

        self.setCurrentExpDataDirectory(filenameTuple[0])

    def setCurrentExpDataDirectory(self, filename):
        self.currentExpDataFilename = filename
        self.lineEdit.setText(self.currentExpDataFilename)

    def updateExpData(self, readFile=False):
        if self.dataService.has_data(self.currentExpDataFilename):   # don't load the same data twice (remove the data first, if you want to reload)
            logging.info("This data file is already loaded: %s" % self.currentExpDataFilename)
            return

        if readFile:
            self.currentExpDataFilename = self.lineEdit.text()
            format = self.getExpDataFileFormat()

            self.dataService.load_data([self.currentExpDataFilename], type=services.dataservice.EXPERIMENTAL,
                                       parkinController=self.parkinController, format=format)

        expData = self.dataService.get_experimental_data()
        if expData:
            self.updatedDataEvent.emit(expData)

    def getExpDataFileFormat(self):
        filename = self.currentExpDataFilename
        if filename.endswith("csv") or filename.endswith("txt"):
            format = datamanagement.dataset.FORMAT_EXP_SIMPLE_CSV
        elif filename.endswith("dat"):
            format = datamanagement.dataset.FORMAT_EXP_PARKIN
        else:
            format = None

        return format

    ###### SLOTS #######

    @Slot("")
    def on_buttonBrowse_clicked(self):
        #logging.debug("SimulationWorkbenchController: in on_buttonBrowseExpData_clicked()")
        self.browseExpData()
        if not self.currentExpDataFilename:
            logging.info("No file selected. Can't import data.")
            return
        self.updateExpData(readFile=True)
        self.lineEdit.clear()

    @Slot("")
    def on_buttonImport_clicked(self):
        if not self.currentExpDataFilename:
            logging.info("No filename given. Can't import data.")
            return
        #logging.debug("SimulationWorkbenchController: in on_buttonBrowseExpData_clicked()")
        self.updateExpData(readFile=True)
        self.lineEdit.clear()
