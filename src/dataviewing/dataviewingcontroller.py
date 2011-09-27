'''
Created on Mar 10, 2010

@author: bzfwadem
'''
from collections import OrderedDict

import logging

#from PySide.QtGui import *
#from PySide.QtCore import *
#from _ordereddict import ordereddict
from PySide.QtCore import SIGNAL, Qt, Slot
from PySide.QtGui import QDialog, QMdiSubWindow, QMdiArea


from ui_DataView2 import Ui_DataViewWidget
from plotting.plotwidget import PlotWidget
from services.dataservice import DataService
from sourcestablemodel import SourcesTableModel

class DataViewingController(QDialog, Ui_DataViewWidget):
    '''
    A experimentalData view window (implemented as DockWidget, so it 
    can be docked inside the main application potentially)
    to display plots, etc. (Maybe more than just plots in a future release?)
    
    In MVC-naming this is the Controller. The View is in Ui_dataViewWidget.
    
    @param parent: Standard Qt UI parent
    @type parent: QWidget
    
    @since: 2010-03-10
    '''
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, parent = None):
        '''
        Creates a data model from the data (so that changes in the data
        are reflected in the View).
        
        '''
        super(DataViewingController, self).__init__(parent)
        self.setupUi(self)

        self.dataService = DataService()
        experimentalData = self.dataService.get_experimental_data()
        simulationData = self.dataService.get_simulation_data()
        
        #data = ordereddict()
        self.data = OrderedDict()
        if simulationData is not None and len(simulationData) > 0:
            self.simulationData = simulationData
            for (sbmlEntity, entityData) in self.simulationData.items():
                #sbmlRef = entityData.sbmlEntity
                dataTuple = (entityData, None)
                self.data[sbmlEntity] = dataTuple
        else:
            self.simulationData = None

        if experimentalData is not None:
            self.experimentalData = experimentalData
            for (sbmlEntity, entityData) in experimentalData.items():
                #sbmlRef = entityData.sbmlEntity
                if sbmlEntity in self.data:
                    dataTuple = self.data[sbmlEntity]
                    dataTuple = (dataTuple[0], entityData)
                    self.data[sbmlEntity] = dataTuple
                else:
                    dataTuple = (entityData, None)
                    self.data[sbmlEntity] = dataTuple
        else:
            self.experimentalData = None
            
        if self.experimentalData or self.simulationData:
            self.dataModel = SourcesTableModel(combinedData = self.data
                                               #experimentalData = self.experimentalData, 
                                               #simulationData = self.simulationData
                                               )
            self.connect(self.dataModel,
                         SIGNAL("dataChanged(QModelIndex, QModelIndex)"),
                         self.update_plots)
        
        #self.data = []  # create single list with all data entities
#        for item in self.experimentalData:
#            self.data.append(item)
#        for item in self.simulationData:
#            if item in self.data:
#                continue
#            self.data.append(item)

        self.populate_sources_table()

#        self.plotWindows = {}
#        self.flatListOfPlotWidgets = []
        self.existingPlotWindows = {}
        self.update_plots()  # testing
        #QTimer.singleShot(0, self.update_plots)



    def populate_sources_table(self):
        '''
        Sets the "sources" data model to the source table view.
        '''
        if self.dataModel is None:
            logging.error("There is no model to populate with experimental Data.")
            return

        table = self.tableSources
        table.setModel(self.dataModel)


    def update_plots(self):
        '''
        Create all the plots based on the selection in the list widget 
        self.tableSources
        
        This is rather complicated and should be refactored + broken
        down.
        '''

        # gather information about what to show
        windowTitlesToShow = {}
        #for (dataID, dataItem) in self.experimentalData.items():
        for (entity, dataTuple) in self.data.items():
            dataID = entity.id
            if self.dataModel.does_show_experimental_data_of(dataID) and self.dataModel.does_show_simulation_data_of(dataID):
                windowTitle = "Experimental and simulation values of %s" % dataID
            elif self.dataModel.does_show_experimental_data_of(dataID):
                windowTitle = "Experimental values of %s" % dataID
            elif self.dataModel.does_show_simulation_data_of(dataID):
                windowTitle = "Simulation values of %s" % dataID
            else:
                windowTitle = None

            if windowTitle is not None:
                windowTitlesToShow[windowTitle] = (entity, dataTuple)


        # close previous windows that show information we don't want now
        for existingWindowTitle in self.existingPlotWindows.keys():
            if not windowTitlesToShow.has_key(existingWindowTitle):
                self.existingPlotWindows.pop(existingWindowTitle).close()


        # create missing windows
        #for (dataID, dataItem) in self.experimentalData.items():
        for (windowTitle, (entity, dataTuple)) in windowTitlesToShow.items():
            
            dataID = entity.id

            if self.existingPlotWindows.has_key(windowTitle):  # dont' create windows that are already there
                continue

            labelExperimental = "Experimental values of %s" % dataID
            labelSimulation = "Simulation values of %s" % dataID

            subWindow = QMdiSubWindow(parent = self.plotWindowsArea)
            subWindow.setAttribute(Qt.WA_DeleteOnClose)
            subWindow.setOption(QMdiSubWindow.RubberBandResize, True)
            self.existingPlotWindows[windowTitle] = subWindow


#            if self.dataModel.does_show_experimental_data_of(dataID):
#                if self.simulationData.has_key(dataID):
#                    experimentalData = {dataID:dataItem}
#                else:
#                    experimentalData = None
#            else:
#                experimentalData = None
#
#            if self.dataModel.does_show_simulation_data_of(dataID):
#                if self.simulationData.has_key(dataID):
#                    simulationData = {dataID + "_sim" : self.simulationData[dataID]}
#                else:
#                    simulationData = None
#            else:
#                simulationData = None

            if self.dataModel.does_show_experimental_data_of(dataID):
                experimentalData = dataTuple[1]
            else:
                experimentalData = None

            if self.dataModel.does_show_simulation_data_of(dataID):
                simulationData = dataTuple[0]
            else:
                simulationData = None

            plotWidget = PlotWidget(parent = subWindow,
                                    experimentalData = experimentalData,
                                    simulationData = simulationData,
                                    labelExperimental = labelExperimental,
                                    labelSimulation = labelSimulation,
                                    showLegend = self.checkBoxShowLegend.isChecked(),
                                    logYAxis = self.checkBoxLogYAxis.isChecked())

            subWindow.setWindowTitle(windowTitle)
            subWindow.setWidget(plotWidget)
            subWindow.show()    # important!




    @Slot("bool")
    def on_checkBoxPlotGroupsAsTabs_toggled(self, isChecked):
        '''
        This is a slot for toggling a tab UI for the plots,
        '''
        logging.info("Plot Groups are shown as Tabs: %s" % isChecked)
        if isChecked:
            self.plotGroupsArea.setViewMode(QMdiArea.TabbedView)
        else:
            self.plotGroupsArea.setViewMode(QMdiArea.SubWindowView)

    @Slot("QTableWidgetItem")
    def on_tableSources_itemChanged(self, item):
        '''
        This is a slot. Whenever some item changes in the list view 
        (e.g. some data gets checked/unchecked), the plots are updated.
        '''
        self.update_plots()

    @Slot("")
    def on_pushButtonReplot_clicked(self):
        '''
        This is a slot. It causes the plots to be replotted.
        '''
        for existingWindowTitle in self.existingPlotWindows.keys():
            self.existingPlotWindows.pop(existingWindowTitle).close()
        self.update_plots()
