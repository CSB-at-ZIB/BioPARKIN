import logging
import os
import random
from PySide.QtCore import Slot, Qt
from PySide.QtGui import QWidget, QFileDialog, QCheckBox
import time
from basics.widgets.selectabletableheader import SelectableTableHeader
from datamanagement.entitydata import EntityData
from services.dataservice import DataService
from simulationworkbench.widgets.databrowsermodel import DataBrowserModel
from simulationworkbench.widgets.ui_databrowser import Ui_DataBrowser
from services.optionsservice import OptionsService

class DataBrowser(QWidget, Ui_DataBrowser):
    """
    The DataBrowser provides a GUI to handle experimental data (loaded from files)
    as well as other data that has been added to the DataService.

    It shows a table-like view on the data and has various options to select data (with checkboxes)
    on several levels (DataSet level and EntityData level). It also provides option to timeshift data
    and to perturb it (the latter option is only shown when BioPARKIN is in debug mode).

    @since: 2011-08-24
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"


    def __init__(self, parent, id, dataSet):
        super(DataBrowser, self).__init__(parent)
        self.setupUi(self)

        self._simWorkbench = None
        self.dataService = None

        self.id = id
        self.data = dataSet

        self.optionsService = OptionsService()

        # create the custom selectable table header
        self.selectableHeader = SelectableTableHeader(Qt.Horizontal, self.tableView)
        self.selectableHeader.setNonSelectableIndexes([0])
        self.selectableHeader.sectionSelectionChanged.connect(self.on_columnSelectionChanged)

        self.tableView.setHorizontalHeader(self.selectableHeader)

        # create the data model
        self.dataModel = DataBrowserModel(self, self.id, self.data)
        self.tableView.setModel(self.dataModel)

        self._setUpSelectionCheckBox()
        self._updateInfoPane()

        if not self.optionsService.getDebug():
            self.groupBoxPerturbation.setVisible(False)


    def getId(self):
        return self.id

    def setSimulationWorkbench(self, simWorkbench):
        self._simWorkbench = simWorkbench

    def getSelectionCheckBox(self):
        return self._selectionCheckBox

    def isSelected(self):
        checkState = self._selectionCheckBox.checkState()
        return True if checkState == Qt.Checked else False


    def _setUpSelectionCheckBox(self):
        self._selectionCheckBox = QCheckBox()
        self._selectionCheckBox.setChecked(True)
        infoText = "Select or deselect this data (e.g. to be included in plots and computations)."
        self._selectionCheckBox.setStatusTip(infoText)
        self._selectionCheckBox.setToolTip(infoText)

        self._selectionCheckBox.stateChanged.connect(self._selectionChanged)

    def _updateInfoPane(self):
        """
        Updates the info pane with basic info about the loaded data
        and the data file (if any).
        """
        self.lineEditInfoSpecies.setText(str(self.data.getNumOfRealData()))
        self.lineEditInfoDataType.setText(self.data.type)

        filepath = self.data.filename
        if filepath and os.path.exists(filepath):
            self.lineEditInfoPath.setText(filepath)

            filesize = os.path.getsize(filepath)
            filesize = filesize / 1024 # displaying kB
            self.lineEditInfoFilesize.setText("%s kB" % filesize)

            timeLastModifiedEpoch = os.path.getmtime(filepath)
            timeLastModified = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(timeLastModifiedEpoch))
            self.lineEditInfoLastModified.setText(str(timeLastModified))
        else:
            noFileText = "No File"
            self.lineEditInfoPath.setText(noFileText)
            self.lineEditInfoFilesize.setText(noFileText)
            self.lineEditInfoLastModified.setText(noFileText)


    def remove(self):
        """
        Cleans up stuff then destroys self.

        It's not sure whether this is really needed
        but it might serve to close some memory holes
        (e.g. dangling references somewhere).
        """
        del self.dataModel
        del self

    @Slot()
    def on_actionPlot_triggered(self):
        dataDict = {self.data.getId(): self.data}
        self._simWorkbench.plotExpData(dataDict)

    @Slot()
    def on_buttonPerturb_clicked(self):
        """
        Perturbs the data by the % given
        in self.spinBoxPerturb.
        """
        percentage = self.spinBoxPerturb.value()
        factor = percentage / 100.0

        for entity, entityData in self.data.getData().items():
            if not entityData.isSelected():
                continue
            id = entity.getId() if type(entity) == EntityData else str(entity)
            logging.info("Perturbing data of EntityData: %s" % id)
            for i in xrange(len(entityData.datapoints)):
                value = entityData.datapoints[i]
                if not value:   # for None values
                    continue
                fraction = value * factor   # fraction of value that will be added or substracted
                newValue = value + random.uniform(-1, 1) * fraction
                entityData.setDatapoint(i, newValue)

    @Slot("")
    def on_buttonSaveAs_clicked(self):
        logging.info("Saving data. Displaying file chooser...")
        file_choices = "Tab-Delimited Text File *.txt (*.txt)"

        path = unicode(QFileDialog.getSaveFileName(self, 'Save file', '', file_choices)[0])

        if not path.endswith(".txt"):
            path += ".txt"

        if path:
            if not self.dataService:
                self.dataService = DataService()

            id = self.data.getId()
            self.dataService.save_data_as_csv(id, path)
            logging.info("Saved data to %s" % path)


    @Slot()
    def on_buttonTimeshift_clicked(self):
        """
        Timeshift data within this DataBrowser (i.e. DataSet).
        Not only shift the global timepoints but also the timepoint lists
        within the individiual EntityData objects.
        """
        try:
            shiftValue = float(self.lineEditTimeshift.text())
            self.dataModel.doTimeshift(shiftValue)
        except Exception, e:
            logging.error("DataBrowser.on_buttonTimeshift_clicked(): Error while timeshifting the data: %s" % e)


    def _selectionChanged(self, state):
        """
        This SLOT is connected to the stateChanged SIGNAL of
        the internal self._selectionCheckBox. It changes the
        isSelected boolean of the underlying self.data DataSet.
        """
        isSelected = True if state == Qt.Checked else False
        self.data.setSelected(isSelected)

    def on_columnSelectionChanged(self, index, checkstate):
        entityData = self.dataModel.getEntityData(index)
        if entityData and type(entityData) == EntityData:
            selected = True if checkstate == Qt.Checked else False
            entityData.setSelected(selected)