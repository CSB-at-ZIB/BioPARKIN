from PySide.QtCore import Slot, Qt
from PySide.QtGui import QDialog, QListWidgetItem, QFileDialog, QDialogButtonBox
from ui_DataManagementView import Ui_DataManagementView

class DataManagementController(QDialog, Ui_DataManagementView):
    """
    This is the controller for the Data Manager View (designed in Qt
    Designer).

    It facilitates the selection of various data sources (e.g.
    experimental and simulation data).

    There's no clear MVC distinction here. The UI is defined in
    Ui_DataManagementView and thereby separated from the logic which
    is defined here. For ease of use, the logic is in this QDialog child
    so that it can directly be added to the UI.

    @param parent: The standard Qt UI parent
    @type parent: QWidget (QObject?)

    @param dataservice: A data service that can be queried for data
    @type dataservice: DataService

    @since: 2010-03-15
    """
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    def __init__(self, parent=None, dataservice=None):
        """
        Construct the UI, reset the list widgets.
        """
        super(DataManagementController, self).__init__(parent)
        self.setupUi(self)
        
        self.Parent = parent
        self.DataService = dataservice
        
        self.resetListWidgets() 
        
    
    def resetListWidgets(self):
        """
        Clears the list widgets and (re)adds the items from the data
        service.
        """
        self.listWidget_Experimental.clear()
        self.listWidget_Simulation.clear()
        
        if self.DataService is not None:
            if self.DataService.ExperimentalDataFiles is not None:
                self.listWidget_Experimental.addItems(self.DataService.ExperimentalDataFiles)
            if self.DataService.SimulationDataFiles is not None:
                self.listWidget_Simulation.addItems(self.DataService.SimulationDataFiles)
            
    @Slot("")
    def on_pushButton_RemoveExperimental_clicked(self):
        """
        This is a slot activated when the "remove experimental entry" button
        is clicked.
        """
        selectedIndex = self.listWidget_Experimental.selectedIndexes()[0]
        self.listWidget_Experimental.takeItem(selectedIndex.row())
        
    @Slot("")
    def on_pushButton_RemoveSimulation_clicked(self):
        """
        This is a slot activated when the "remove simulation entry" button
        is clicked.
        """
        selectedIndex = self.listWidget_Simulation.selectedIndexes()[0]
        self.listWidget_Simulation.takeItem(selectedIndex.row())
        

    @Slot("")
    def on_pushButton_BrowseExperimental_clicked(self):
        """
        This is a slot activated when the "browse for experimental entry" button
        is clicked.
        An open-file dialog is shown.
        """
        filenames = QFileDialog.getOpenFileNames(self, caption='Select experimental data files')
        for filename in filenames:
            self.listWidget_Experimental.addItem(QListWidgetItem(filename))    
               
    @Slot("")
    def on_pushButton_BrowseSimulation_clicked(self):
        """
        This is a slot activated when the "browse for simulation entry" button
        is clicked.
        An open-file dialog is shown.
        """
        filenames = QFileDialog.getOpenFileNames(self, caption='Select experimental data files')
        for filename in filenames:
            self.listWidget_Simulation.addItem(QListWidgetItem(filename))
            

    def saveListItems(self):
        """
        Takes the current state of both lists and "saves" it to the data
        service (so that other components will now use these new data).
        """
        listOfFilenames = []
        for index in xrange(self.listWidget_Experimental.count()):
            listWidgetItem = self.listWidget_Experimental.item(index)
            item = listWidgetItem.data(Qt.DisplayRole) # use display role, because we want only the string
            listOfFilenames.append(item)
        
        self.DataService.set_experimental_data_files(listOfFilenames)

    def accept(self):
        """
        Overrides the accept method of this QDialog. Saves the lists.
        super.accept() is called, too.
        """
        super(DataManagementController, self).accept()
        self.saveListItems()

    def on_buttonBox_OkCancelResetApply_clicked(self, button):
        """
        This is a slot. It detects which button (OK, Cancel, Reset, Apply) was
        clicked and invokes the correct actions.

        @param button: The clicked button
        @type button: QPushButton (I think)
        """
        if button == self.buttonBox_OkCancelResetApply.button(QDialogButtonBox.Reset):
            self.resetListWidgets()
        if button == self.buttonBox_OkCancelResetApply.button(QDialogButtonBox.Apply):
            self.saveListItems()
        
        
