import copy
from copy import copy
import logging
import csv
import math
from backend import settingsandvalues
import services.dataservice
import datamanagement.entitydata
from PySide.QtGui import QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QFont, QBrush, QColor
from PySide.QtCore import Qt, SIGNAL, Slot
from datamanagement.dataset import DataSet
from services.dataservice import DataService
from services.statusbarservice import StatusBarService
from simulationworkbench.widgets.sortedtablewidgetitem import SortedTableWidgetItem
from simulationworkbench.widgets.ui_tablewidget_v1 import Ui_TableWidget
from simulationworkbench.widgets.abstractviewcontroller import AbstractViewController

__author__ = 'bzfwadem'

#OPTION_SORTABLE_COLUMNS = "option_sortable_columns"
#OPTION_LABEL_X = "option_label_x"
#OPTION_SHOW_LEGEND = "option_show_legend"
#OPTION_LOG_Y_AXIS = "option_log_y_axis"

ORIENTATION_HORIZONTAL = "orientation_horizontal"
ORIENTATION_VERTICAL = "orienation_vertical"

DEFAULT_SHOW_UNITS = True

MODE_DEFAULT = "mode_default"
MODE_SUBCONDITIONS = "mode_subconditions"

COLOR_HIGH = QColor(50,200,50, 200) # medium green
COLOR_MEDIUM = QColor(50,200,50,50) # light green
COLOR_LOW = QColor(200,50,50,100)   # light red

#class TableWidgetController(QWidget, Ui_TableWidget, AbstractViewController):
class TableWidgetController(AbstractViewController, Ui_TableWidget):
    '''
    The controller part for a data table widget. The UI part is declared
    in tablewidget_v1.ui and then converted to ui_tablewidget.py.

    This widget can be fed tabular data and has several options for showing it.

    @since: 2010-11-10
    '''
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"



    def __init__(self, parent=None, host=None, title="Table"):
        '''
        Constructor
        '''
        super(TableWidgetController, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        
        self._initialize()

        #        self.options = {
        #            OPTION_SORTABLE_COLUMNS: self.checkBoxSortableColumns.isChecked(),
        #        }

        self._mode = MODE_DEFAULT
        self.maxValue = -1

        self.host = host
        self.data = None

        self.dataTableHeaders = []
        self.dataTableColumnData = []
        self.dataTableRowCount = -1
        self.dataTableRowHeaders = None

        self.dataTableWidget = None
        self.isColored = False

        self.checkBoxShowUnits.setChecked(DEFAULT_SHOW_UNITS)
        self.showUnits = DEFAULT_SHOW_UNITS

        self.orientation = ORIENTATION_HORIZONTAL

        self.sortColumn = -1    # default: do not sort at load
        self.colorThreshold = None
        self.colorThresholdBase = self.doubleSpinBox_Coloring_Threshold.value()
        self.colorThresholdExponent = self.spinBox_Coloring_Exponent.value()
        self._updateThreshold()

    def setMode(self, mode):
        self._mode = mode
        if mode == MODE_SUBCONDITIONS:
            self.doubleSpinBox_Coloring_Threshold.setMinimum(self.host.getRTol())
            self.doubleSpinBox_Coloring_Threshold.setMaximum(1)
            self.doubleSpinBox_Coloring_Threshold.setSingleStep(0.1)
            self.label_Coloring_Threshold.setText("Anticipated Relative Measurement Error")
            self.groupBox_Coloring.setEnabled(True)

    def _updateView(self, data=None):
        '''
        Overriding the "abstract" base class method. This does the main "drawing" of data, i.e.
        generates the table and fills it with data.
        '''

        if data:
            self.data = data

        if self.data:
            self._updateDataTable(self.data)

    def _clearView(self):
        if self.dataTableWidget:
            self.dataTableWidget.clear()

    def _setRowHeaders(self, dataDescriptors):
        '''
        Sets the given datadescriptors (from an EntityData object) as row headers
        of the table, thereby checking for floats and rounding them, as not to show too
        many digits after the point.
        '''
        #self.dataTableRowHeaders = dataDescriptors
        if not dataDescriptors:
            logging.debug("TableWidgetController._setRowHeaders(): Empty dataDescriptor list.")
            return

        self.dataTableRowHeaders = []

        for descriptor in dataDescriptors:
            try:
                descriptor = float(descriptor)
                descriptor = round(descriptor, 4)
            except ValueError:
                pass
            self.dataTableRowHeaders.append(str(descriptor)) # the QTableWidget needs a list of Strings


    def _computeColor(self, value):
        if type(value) == str:
            if value == "N/A":
                return COLOR_LOW
            value = float(value)

        if self._mode == MODE_DEFAULT:
            if value <= self.colorThreshold:
                color = COLOR_LOW
            else:
                color = COLOR_HIGH
        elif self._mode == MODE_SUBCONDITIONS:
            if value >= self.colorThreshold:
                color = COLOR_LOW
            else:
                #percentage = value / float(self.maxValue)
                percentage = (self.maxValue - value + 1) / float(self.maxValue) # +1 because it's the "lowest" subconditon, and represents 100%

                highRed, highGreen, highBlue, highAlpha = COLOR_HIGH.red(), COLOR_HIGH.green(), COLOR_HIGH.blue(), COLOR_HIGH.alpha()
                mediumRed, mediumGreen, mediumBlue, mediumAlpha = COLOR_MEDIUM.red(), COLOR_MEDIUM.green(), COLOR_MEDIUM.blue(), COLOR_MEDIUM.alpha()

                diffRed, diffGreen, diffBlue, diffAlpha = highRed-mediumRed, highGreen-mediumGreen, highBlue-mediumBlue, highAlpha-mediumAlpha

                valueRed = diffRed*percentage+mediumRed
                valueGreen = diffGreen*percentage+mediumGreen
                valueBlue = diffBlue*percentage+mediumBlue
                valueAlpha = diffAlpha*percentage+mediumAlpha

                color = QColor(valueRed,valueGreen,valueBlue,valueAlpha)
        else:
            color = QColor(0,0,0,255)   #transparent

        return color

    def _updateDataTable(self, data):
        '''
        Updates the data table with data from the last integration.
        '''

        #prepare data
        self.dataTableHeaders = []
        self.dataTableColumnData = []
        self.dataTableRowCount = -1
        self.dataTableRowHeaders = None
        self.maxValue = -1
        for (entity, entityDataList) in data.items():
            for entityData in entityDataList:
                dataDescriptors = entityData.dataDescriptors
                if not self.dataTableRowHeaders:
                    self._setRowHeaders(dataDescriptors)
                elif len(self.dataTableRowHeaders) != len(dataDescriptors):
                    logging.debug(
                        "Different number of time points for two Species. Last Species (%s) will be skipped." % entity)
                    continue

                # set header for first column (dataDescriptor/Timepoint col)
                # in first iteration
                if len(self.dataTableHeaders) == 0: 
                    dataDescriptorName = entityData.dataDescriptorName
                    dataDescriptorUnit = entityData.dataDescriptorUnit
                    if not dataDescriptorUnit and "timepoint" in str(dataDescriptorName).lower():
                        dataDescriptorUnit = self.host.optionTimeUnit
                    firstColHeader = ""
                    if dataDescriptorName:
                        if self.showUnits:
                            firstColHeader = "%s [%s]" % (dataDescriptorName,dataDescriptorUnit)
                        elif dataDescriptorName:
                            firstColHeader = "%s" % dataDescriptorName
                    self.dataTableHeaders.append(firstColHeader)

                #self.dataTableHeaders.append("Time species %s [%s]" % (str(speciesID), self.lineEditTimeUnit.text()))
                #self.dataTableColumnData.append(timepoints)
                if len(dataDescriptors) > self.dataTableRowCount:
                    self.dataTableRowCount = len(dataDescriptors)

                #datapoints = entityData.datapoints
                datapoints = []

                # shorten datapoints
                for i, datapoint in enumerate(entityData.datapoints):
                    try:
                        #datapoints.append(round(float(datapoint), 4))
#                        valueString = "%g" % (float(datapoint))
                        floatValue = float(datapoint)   # will jump to except if no float
                        valueString = "N/A" if math.isnan(floatValue) else ' {0:-.4f}'.format(floatValue)
                        datapoints.append(valueString)

                        # preparing color computation
#                        logging.debug(entityData.dataDescriptorName)
#                        logging.debug(entityData.dataDescriptors[i] == settingsandvalues.SUBCONDITION_HEADER_ABSOLUTE)
                        if self._mode == MODE_SUBCONDITIONS \
                            and entityData.dataDescriptors[i] == settingsandvalues.SUBCONDITION_HEADER_ABSOLUTE \
                            and floatValue > self.maxValue\
                            and floatValue < self.colorThreshold:
                            self.maxValue = floatValue

                    except:
#                        datapoints.append(round(float("nan"), 4))
                        datapoints.append(str(datapoint))

                    #                logging.debug("TableWidgetController - datapoints: %s" % datapoints)   # too much overhead
                    #self.dataTableHeaders.append("Data species %s [%s]" % (str(speciesID), entityData.getUnit()))
                if self.showUnits:
#                    if type(entity) == str:
#                        self.dataTableHeaders.append("%s" % entity)
#                    else:
                    self.dataTableHeaders.append("%s [%s]" % (entity.getCombinedId(), entityData.getUnit()))
                else:
                    self.dataTableHeaders.append("%s" % entity.getCombinedId())
                self.dataTableColumnData.append(datapoints)
#                if len(datapoints) > self.dataTableRowCount:
#                    self.dataTableRowCount = len(datapoints)

        # Put those labels into the actual data that would be the vertical/row labels.
        # We can't use .setVerticalHeaderLabers() because those labels don't get sorted together with the data.
        # Very weird but that seems to be the intended behaviour of Qt.
        if self.orientation == ORIENTATION_VERTICAL:
            #self.dataTableColumnData.insert(0, self.dataTableHeaders) # handle as if it were data so that sorting works

            self.dataTableHeaders = self.dataTableHeaders[1:]   # remove unnecessary dataDescriptor name
            for i in xrange(len(self.dataTableColumnData)):
                entry = self.dataTableColumnData[i]
                entry.insert(0, self.dataTableHeaders[i])
            self.dataTableRowHeaders.insert(0,"")
        else:
            self.dataTableColumnData.insert(0, self.dataTableRowHeaders)
            #self.dataTableHeaders.insert(0,"")


        if not self.dataTableWidget:    # create for the first time
            tableLayout = QVBoxLayout(self.tableWrapper)
            self.dataTableWidget = QTableWidget(self)
            tableLayout.addWidget(self.dataTableWidget)

        #prepare table
        self.dataTableWidget.setSortingEnabled(False)   # will be set to True after everything has been set up and added
        if self.orientation == ORIENTATION_HORIZONTAL:
            self.dataTableWidget.setColumnCount(len(self.dataTableHeaders))
            self.dataTableWidget.setRowCount(self.dataTableRowCount)
            self.dataTableWidget.setHorizontalHeaderLabels(self.dataTableHeaders)
#            self.dataTableWidget.setVerticalHeaderLabels(
#                self.dataTableRowHeaders)  # has to be called after setRowCount?
        elif self.orientation == ORIENTATION_VERTICAL:
            self.dataTableWidget.setRowCount(len(self.dataTableHeaders))
            self.dataTableWidget.setColumnCount(len(self.dataTableRowHeaders))
#            self.dataTableWidget.setVerticalHeaderLabels(self.dataTableHeaders)
            self.dataTableWidget.setHorizontalHeaderLabels(
                self.dataTableRowHeaders)  # has to be called after setRowCount?

        #put data into table
        for col in xrange(len(self.dataTableColumnData)):
            for row in xrange(len(self.dataTableColumnData[col])):
                try:
                    value = self.dataTableColumnData[col][row]  # don't touch "values"; they could be pre-formatted strings
                    newItem = SortedTableWidgetItem()    # use custom item class
                    newItem.setData(Qt.DisplayRole, value)
                    newItem.setTextAlignment(Qt.AlignRight)
                    newItem.setFont(QFont("Fixed"))
                    if self.isColored:
                        if self._mode == MODE_DEFAULT or (self._mode == MODE_SUBCONDITIONS and row==2):
                            color = self._computeColor(value)
                            newItem.setBackground(QBrush(color))
                except Exception, e:
                    logging.debug("TableWidgetController._updateDataTable(): Could not put value into widget item: %s\nError: %s" % (value,e))
#                    newItem = SortedTableWidgetItem(str(self.dataTableColumnData[col][row]))
#                    newItem.setTextAlignment(Qt.AlignRight)
#                    newItem.setFont(QFont("Fixed"))
                if self.orientation == ORIENTATION_HORIZONTAL:
                    self.dataTableWidget.setItem(row, col, newItem)
                elif self.orientation == ORIENTATION_VERTICAL:
                    self.dataTableWidget.setItem(col, row, newItem)

        self.dataTableWidget.setSortingEnabled(True)

        if self.sortColumn != -1:
            self.dataTableWidget.sortItems(self.sortColumn)

        self.dataTableWidget.resizeColumnsToContents()



    def setOrientation(self, orientation):
        self.orientation = orientation
        if orientation == ORIENTATION_HORIZONTAL:
            self.checkBoxOrientation.setChecked(False)
        else:
            self.checkBoxOrientation.setChecked(True)


    def saveDataAsCsv(self, path):
        '''
        Save current data as CSV file.
        '''

        try:

            orientationBefore = self.orientation
            self.orientation = ORIENTATION_HORIZONTAL


            if self.data:
                self._updateDataTable(self.data)

            csv.register_dialect("SimulationData", delimiter='\t', quotechar='"', skipinitialspace=True)
            writer = csv.writer(open(path, "wb"), dialect="SimulationData")

#            header = ["Timepoint [%s]" % self.host.labelTimeUnit.text()]
#            header.extend(self.dataTableHeaders)
            header = self.dataTableHeaders
            writer.writerow(header)

            for row in xrange(self.dataTableRowCount):
                rowData = []
                #rowData.append(self.dataTableRowHeaders[row])   # adds the timepoint up front
                for col in xrange(len(self.dataTableHeaders)):
                    rowData.append(self.dataTableColumnData[col][row])
                writer.writerow(rowData)

            self.orientation = orientationBefore

        except Exception, e:
            logging.error("Error while trying to write CSV file: %s\nError: %s" % (path, e))


    def _updateThreshold(self):
        self.colorThreshold = self.colorThresholdBase * math.pow(10, self.colorThresholdExponent)
        if self._mode == MODE_SUBCONDITIONS:
        # value has to be between rtol and -1
        #            if value > 1:
        #                value = 1
        #            elif value < self.host.getRTol():
        #                value = self.host.getRTol()
            if self.colorThreshold == 0.0:
                self.colorThreshold = 0
            else:
                self.colorThreshold = 1 / self.colorThreshold
        #        else:
        #            self.colorThreshold = self.colorThreshold
        self._updateDataView()

            ############### SLOTS ################

    @Slot("")
    def on_actionSave_triggered(self):
        '''
        Show a dialog to save the currently shown plot to a png file.

        Overrides an "abstract" method in AbstractViewController.
        '''
        logging.debug("Saving data. Displaying file chooser...")
        #file_choices = "CSV (*.csv)|*.csv"
        file_choices = "Excel *.txt (*.txt);;CSV *.csv (*.csv)"

        path = unicode(QFileDialog.getSaveFileName(self,
                                                   'Save file', '',
                                                   file_choices)[0])
        if path:
            self.saveDataAsCsv(path)
            logging.info("Saved data to %s" % path)


    @Slot("")
    def on_actionSelectAll_triggered(self):
        self._selectAllSources(True)

    @Slot("")
    def on_actionDeselectAll_triggered(self):
        self._selectAllSources(False)

    @Slot("")
    def on_actionInvertSelection_triggered(self):
        self._invertSourceSelection()

    @Slot("bool")
    def on_checkBoxOrientation_toggled(self, isChecked):
        logging.info("Switching 'Switch rows vs. columns' to %s" % self.checkBoxOrientation.isChecked())
        if isChecked:
            self.orientation = ORIENTATION_VERTICAL
        else:
            self.orientation = ORIENTATION_HORIZONTAL
        self._updateView()

    @Slot("bool")
    def on_checkBoxShowUnits_toggled(self, isChecked):
        logging.info("Switching 'Show Table Header Units' to %s" % self.checkBoxShowUnits.isChecked())
        self.showUnits = isChecked
        self._updateView()


    @Slot("")
    def on_actionAddToExperimentalData_triggered(self):
        '''
        Adds the currently displayed data and adds it to the experimental data.
        This is usually only useful if you want to want to use simulation results (which can then be perturbed)
        as input for other tools like parameter value estimation.
        '''
        logging.info("Adding current data to Experimental Data...")
        dataService = DataService()
        expDataSet = DataSet(None)
        expDataSet.setId("Pseudo-Experimental Data")
        expDataSet.setType(services.dataservice.EXPERIMENTAL)
        expDataSet.setSelected(True)
        first = True
        for key, list in self.data.items():
            for oldItem in list:
                item = oldItem.copy()

                if type(item.getId()) != str:
                    logging.debug("TableWidgetController.on_actionAddToExperimentalData_triggered(): Encountered item with non-string as id: %s. Skipping." % str(item.getId()))
                    continue
#                item.setId(item.getId() + "_syn")
                item.setType(datamanagement.entitydata.TYPE_EXPERIMENTAL)
                item.setAssociatedDataSet(expDataSet)
                expDataSet.data[key] = item # TODO: Handle mutliple EntityData objects correctly
                if first:
                    expDataSet.dataDescriptors = item.dataDescriptors[:]
                    expDataSet.dataDescriptorUnit = item.dataDescriptorUnit
                    first = False
        dataService.add_data(expDataSet)
#        self.host.updateExpData()



    #### COLORING-RELATED METHODS ####

    @Slot("bool")
    def on_groupBox_Coloring_clicked(self, isSelected):
        self.isColored = isSelected
        self._updateDataView()

    @Slot("double")
    def on_doubleSpinBox_Coloring_Threshold_valueChanged(self, value):
        self.colorThresholdBase = value
        self._updateThreshold()


    @Slot("int")
    def on_spinBox_Coloring_Exponent_valueChanged(self, value):
        self.colorThresholdExponent = value
        self._updateThreshold()


