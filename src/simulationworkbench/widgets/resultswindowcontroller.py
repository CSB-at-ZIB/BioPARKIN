from PySide.QtCore import Qt, Slot
from PySide.QtGui import  QMainWindow, QMdiArea, QMdiSubWindow
from simulationworkbench.widgets.Ui_resultswindow import Ui_ResultsWindow

class ResultsWindowController(QMainWindow, Ui_ResultsWindow):
    """
    This class provides a window in which to display several
    kinds of data (in plots and tables).

    @since: 2011-04-14
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"


    def __init__(self, parent):
        super(ResultsWindowController, self).__init__(parent)
        self.setupUi(self)

        if self.checkBoxTabMode.isChecked():
            self.buttonCascadeWindows.setHidden(True)
            self.buttonTileWindows.setHidden(True)
        else:
            self.buttonCascadeWindows.setHidden(False)
            self.buttonTileWindows.setHidden(False)

    def getMdiArea(self):
        return self.mdiArea


    def addResultSubWindow(self, plotWidget):
        subWindow = QMdiSubWindow(parent=self.getMdiArea())
        subWindow.setAttribute(Qt.WA_DeleteOnClose)
        subWindow.setWidget(plotWidget)
        subWindow.setOption(QMdiSubWindow.RubberBandResize, True)
        self.getMdiArea().addSubWindow(subWindow)
        subWindow.showMaximized()
        subWindow.activateWindow()
        subWindow.show()    # important!
        self.show()

    def hasResultforData(self, dataSet):
        for subWindow in self.getMdiArea().subWindowList():
            viewController = subWindow.widget()
            if viewController.hasData(dataSet):
                return True
        return False



    #### SLOTS ######

    @Slot("bool")
    def on_checkBoxTabMode_toggled(self, checked):
        if checked:
            self.getMdiArea().setViewMode(QMdiArea.TabbedView)
        else:
            self.getMdiArea().setViewMode(QMdiArea.SubWindowView)
