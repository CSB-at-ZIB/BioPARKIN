import logging
from PySide.QtCore import Slot, Qt
from PySide.QtGui import QDialog, QDialogButtonBox
from services.dataservice import DataService
from simulationworkbench.widgets.ui_timepointchooser import Ui_TimepointChooser

class TimepointChooser(QDialog, Ui_TimepointChooser):
    """
    A simple dialog that presents several ways to pick timepoints.

    @since: 2011-09-12
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    timepointsInvalidString = "The list of time points is invalid! (It may only contain digits, e.g. '12.5', delimited by white space.)"

    def __init__(self, parent):
        super(TimepointChooser, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # remove the "What's this" button in the title bar

        self.timepoints = []

        self.optionStartTime = 0
        self.optionEndTime = 100
        self.optionNumIntervals = 10
        self.optionIntervalSize = None

        self.lineEdit_StartTime.setText(str(self.optionStartTime))
        self.lineEdit_EndTime.setText(str(self.optionEndTime))
        self.lineEdit_NumIntervals.setText(str(self.optionNumIntervals))
        self._updateLineEditIntervalSize()

        self.labelTimepointsInvalid.setHidden(True)


    def getTimepoints(self):
        return self.timepoints


    #### internal methods ####

    def _updateLineEditIntervalSize(self):
        self.optionIntervalSize = (self.optionEndTime - self.optionStartTime) / float(self.optionNumIntervals)
        self.lineEdit_IntervalSize.setText(str(self.optionIntervalSize))

    def _updateLineEditNumIntervals(self):
        self.optionNumIntervals = int(
            0.5 + (self.optionEndTime - self.optionStartTime) / float(self.optionIntervalSize))
        self.lineEdit_NumIntervals.setText(str(self.optionNumIntervals))


    #### SLOTs ####

    @Slot("")
    def on_lineEdit_StartTime_editingFinished(self):
        """
        Ensures that only floats are entered into the start time field.
        """
        try:
            self.optionStartTime = float(self.lineEdit_StartTime.text())
        except:
            self.lineEdit_StartTime.setText(str(self.optionStartTime))   #set last valid value
            return

        self._updateLineEditIntervalSize()


    @Slot("")
    def on_lineEdit_EndTime_editingFinished(self):
        """
        Ensures that only floats are entered into the EndTime field.
        """
        try:
            self.optionEndTime = float(self.lineEdit_EndTime.text())
        except:
            self.lineEdit_EndTime.setText(str(self.optionEndTime))
            return

        self._updateLineEditIntervalSize()


    @Slot("")
    def on_lineEdit_NumIntervals_editingFinished(self):
        """
        Ensures that only integers are entered into the # intervals field.
        """
        try:
            self.optionNumIntervals = int(self.lineEdit_NumIntervals.text())
        except:
            self.lineEdit_NumIntervals.setText(
                str(self.optionNumIntervals)) # str(backend.settingsandvalues.DEFAULT_NUMBER_INTERVALS))
            return

        self._updateLineEditIntervalSize()

    @Slot("")
    def on_lineEdit_IntervalSize_editingFinished(self):
        """
        Ensures that only floats are entered into the interval size field.
        """
        try:
            self.optionIntervalSize = float(self.lineEdit_IntervalSize.text())
        except:
            self.lineEdit_IntervalSize.setText(str(self.optionIntervalSize))
            self._updateLineEditIntervalSize()
            return

        self._updateLineEditNumIntervals()
        self._updateLineEditIntervalSize()

    @Slot("")
    def on_button_Calculate_clicked(self):
        self._updateLineEditIntervalSize()
        self._updateLineEditNumIntervals()
        self.timepoints = [self.optionStartTime + self.optionIntervalSize * x for x in xrange(self.optionNumIntervals + 1)]
        timepointsStr = str(self.timepoints).replace(",", " ").strip("[").strip("]")

        self.plainTextEdit_Timepoints.clear()
        self.plainTextEdit_Timepoints.insertPlainText(timepointsStr)

    @Slot("")
    def on_button_FromData_clicked(self):
        try:
            dataService = DataService()
            expData = dataService.get_experimental_data()
            timepointSet = set()
            if expData:
                for dataSet in expData.values():
                    if not dataSet.isSelected():
                        continue
                    if dataSet.dataDescriptors:
                        for dataDescriptor in dataSet.dataDescriptors:
                            timepointSet.add(float(dataDescriptor))
                    for entityData in dataSet.getData().values():
                        if not entityData.isSelected():
                            continue
                        if entityData.dataDescriptors:
                            for dataDescriptor in entityData.dataDescriptors:
                                timepointSet.add(float(dataDescriptor))
            self.timepoints = list(timepointSet)
            self.timepoints.sort()
            timepointsStr = str(self.timepoints).replace(",", " ").strip("[").strip("]")

            if not timepointsStr:
                timepointsStr = "No timepoint data."

            self.plainTextEdit_Timepoints.clear()
            self.plainTextEdit_Timepoints.insertPlainText(timepointsStr)
        except Exception, e:
            logging.error("Could not get timepoints from data. Error: %s" % e)


    def on_plainTextEdit_Timepoints_textChanged(self):
        try:
            timepointsStr = self.plainTextEdit_Timepoints.toPlainText()
            self.timepoints = []
            for timepointStr in  timepointsStr.split(" "):
                if timepointStr:
                    self.timepoints.append(float(timepointStr))

            self.labelTimepointsInvalid.setHidden(True)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

        except:
            self.labelTimepointsInvalid.setHidden(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)