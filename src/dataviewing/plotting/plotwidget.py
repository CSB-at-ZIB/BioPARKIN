'''
Created on Mar 9, 2010

@author: bzfwadem
'''
import logging

#from PySide.QtGui import *
#from PySide.QtCore import *
from PySide.QtGui import QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout

import matplotlib
import os
if os.name == "nt":
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    #from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
else:
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from matplotlib.figure import Figure
from datamanagement.entitydata import EntityData

OPTION_LABEL_X = "option_label_x"
OPTION_SHOW_LEGEND = "option_show_legend"
OPTION_LOG_Y_AXIS = "option_log_y_axis"
    
class PlotWidget(QWidget):
    '''
    A widget for plotting experimentalData.
    It's still in a rough state and will be improved over time.
    
    Internally, it uses matplotlib to easily draw plots. This is handy but
    probably rather performance-demanding. One future option for speeding
    things up could be to switch the plotting library (possibly Qwt).
    
    @param parent: Standard Qt UI parent
    @type parent: QWidget
    
    @param data: A StableDict of EntityData objects
    @type data: StableDict
    
    
    @param labels: Labels for data entities
    @type labels: []
    
    @param labels: A label for the simulation plot part
    @type labelSimulation: str 
    
    @param showLegend:If legend should be shown, set to True
    @type showLegend: bool
    
    @param logYAxis: If y axis should be log-scaled, set to True
    @type logYAxis: bool 
    
    @since: 2010-03-09
    
    '''
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"
    
    
    def __init__(self, parent=None, data=None, labels=None, options = {}):
        '''
        Rather large init method that does all the plotting directly.
        
        @todo: Put all the options (labels, showLegend, etc.) into properties.
        @todo: Refactor init, split into sub-methods, make everything cleaner.
        '''
        super(PlotWidget, self).__init__(parent)  # standard init call to Qt base class
        
        self.setMinimumSize(400, 300)  
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.data = data 
        self.labels = labels
        self.options = options
        
        
        self.dpi = self.logicalDpiX()
        logging.debug("Plotting at %s dpi." % self.dpi)
        #self.fig = Figure((4.0, 4.0), dpi=self.dpi)
        self.fig = Figure(dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        
        self.axes = self.fig.add_subplot(111)

        if os.name != "nt":
            self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        
        
        left_vbox = QVBoxLayout()
        left_vbox.addWidget(self.canvas)
        left_vbox.addWidget(self.mpl_toolbar)
        
        hbox = QHBoxLayout()
        hbox.addLayout(left_vbox)
        self.setLayout(hbox)
        
        self.setAxes()
        
        self.setData()
            
        self.canvas.draw()

    def setAxes(self):
        '''
        Defines the plot's axes.
        '''
        self.axes.clear()
        self.axes.grid(True)
        
        # set x label
        for entityData in self.data.values():
            yLabel = str(entityData.getAxisLabel())
            break
        self.axes.set_ylabel(yLabel)
        
        # set y label
        if OPTION_LABEL_X in self.options:
            self.axes.set_xlabel(str(self.options[OPTION_LABEL_X]))
        else:
            self.axes.set_xlabel("N/A")
        
        
        if OPTION_LOG_Y_AXIS in self.options and self.options[OPTION_LOG_Y_AXIS]:
            self.axes.set_yscale('log')
        
        if OPTION_SHOW_LEGEND in self.options and self.options[OPTION_SHOW_LEGEND]:
            self.axes.legend()

    def setData(self):
        if self.data:
            for j, entityData in enumerate(self.data.values()):
                timepoints = entityData.timepoints
                datapoints = entityData.datapoints
                label = entityData.getId()
                self.axes.plot(timepoints, datapoints, '-', label=label)


            
            
        #===========================================================================
        # using PyQwt directly
        #===========================================================================
        #    self.plot = Qwt.QwtPlot(self)
        #    self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #    
        #    
        #    # some testing code
        ##    curve = Qwt.QwtPlotCurve()
        ##    curve.setData(range(100), range(200,1,-2))
        ##    curve.attach(self.plot)
        ##    self.plot.replot()
        #
        #    if self.experimentalData is not None:
        #      try:
        #        curve = Qwt.QwtPlotCurve()
        #        pen = QPen(Qt.black, 5)
        #        curve.setPen(pen)
        #        curve.setStyle(Qwt.QwtPlotCurve.Dots)
        #        curve.setData(self.experimentalData[0], self.experimentalData[1]) # assume tuple structure
        #        curve.attach(self.plot)
        #        self.plot.replot()
        #      except Exception, e:
        #        logging.error("There was an error while trying to plot experimentalData: %s" % e)
        #    
        #    self.plot.show()
        
        #  def resizeEvent(self, e): #only called on creation?        
        #    QWidget.resizeEvent( self, e )
        #
        #    x = e.size().width()
        #    y = e.size().height()
        #    print x, y
        #    self.plot.resize(x, y)
        #    self.plot.move(0, 0)
        #    self.plot.replot()
