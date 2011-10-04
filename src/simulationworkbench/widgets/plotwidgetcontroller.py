import StringIO
import Image

import PySide.QtXml # as suggested in a forum to account for .svg icons
from PySide.QtGui import QWidget, QFileDialog, QVBoxLayout, QHBoxLayout
#from simulationworkbench.ui_plotwidget_v1 import Ui_PlotWidget
from PySide.QtCore import Qt, SIGNAL, Slot
import matplotlib
from services.dataservice import DataService
# from simulationworkbench.datasourcestablemodel import DataSourcesTableModel
import logging
from services.statusbarservice import StatusBarService
from simulationworkbench.widgets.abstractviewcontroller import AbstractViewController

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = "PySide"

import os

#if os.name == "nt":
#    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#else:
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

#import matplotlib.cm as colormaps
from matplotlib import cm
from matplotlib.colors import rgb2hex, Normalize, Colormap

from matplotlib.figure import Figure
from itertools import imap
from dataviewing.plotting.plotwidget import PlotWidget
from simulationworkbench.widgets.ui_plotwidget_v1 import Ui_PlotWidget

OPTION_LABEL_X = "option_label_x"
OPTION_SHOW_LEGEND = "option_show_legend"
OPTION_LOG_Y_AXIS = "option_log_y_axis"

PLOT_LINE = '-'
PLOT_POINT = '.'
PLOT_CIRCLE = "o"

DEFAULT_COLORMAP = "spectral" # also possible: Set1, hsv, spectral
# more: http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps

class PlotWidgetController(QWidget, Ui_PlotWidget, AbstractViewController):
    """
    The controller part for a plotting widget. The UI part is declared
    in plotwidget_v1.ui and then converted to ui_plotwidget.py.

    This plot widget can be fed with data via set methods and has several
    options to adjust the visualization of that data.

    @since: 2010-11-08
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, parent=None, host=None, title="Plot"):
        """
        Constructor
        """
        super(PlotWidgetController, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)

        self._initialize()

        self.timeUnit = "a.u." #default ?
        if host:
            self.timeUnit = str(host.optionTimeUnit)

        self.options = {
            OPTION_LABEL_X: "Time [%s]" % (self.timeUnit), #default
            OPTION_LOG_Y_AXIS: self.checkBoxLogYAxis.isChecked(),
            OPTION_SHOW_LEGEND: self.checkBoxShowLegend.isChecked()
        }

        self.host = host

        self.data = None
        self.labels = None

        self.fig = None
        self.canvas = None
        self.axes = None
        self.mpl_toolbar = None
        self.dpi = None

        self.plotStyle = {
            0: PLOT_LINE} #default plot style; if there are more elements, each numbered element corresponds to one data source
        self.plotColors = {}    # will be filled with colors on the first plot


        #self.plotWidget = None


    def _updateView(self, data=None):

    #logging.debug("Updating the plot view!")
    #        plotWidget = PlotWidget(self.splitter, data= data)
    #        self.splitter.insertWidget(0, plotWidget)

        try:
            if data:
                self.data = data
                #        self.labels = None #labels
                #        self.options = {} #options

            if not self.fig:    # on first plot
                self.dpi = self.logicalDpiX()
                logging.debug("Plotting at %s dpi." % self.dpi)
                #self.fig = Figure((4.0, 4.0), dpi=self.dpi)
                self.fig = Figure(dpi=self.dpi)
                self.canvas = FigureCanvas(self.fig)

                self.axes = self.fig.add_subplot(111)
                #if os.name != "nt":
                #self.mpl_toolbar = NavigationToolbar(self.canvas, self)
                self.mpl_toolbar = NavigationToolbar(self.canvas, None)

                left_vbox = QVBoxLayout(self.plotWrapper)
                left_vbox.addWidget(self.canvas)
                #if os.name != "nt":
                left_vbox.addWidget(self.mpl_toolbar)

                self.setAxesAndData()
                self.canvas.draw()
            else:
                self.axes.clear()
                self.setAxesAndData()
                self.canvas.draw()
        except Exception as e:
            logging.debug("PlotWidgetController._updateView: Error occurred: %s" % e)

    def _clearView(self):
        if self.axes:
            self.axes.clear()
        if self.canvas:
            self.canvas.draw()


    def setAxesAndData(self):
        try:
            self.computeColors()
            # some of this has to be done before the data is set
            self.setAxes()

            self.setData()

            # has to be done after the data is set
            if OPTION_SHOW_LEGEND in self.options and self.options[OPTION_SHOW_LEGEND]:
                self.axes.legend()
                #        else:
                #            self.axes.h

        except Exception as e:
            logging.debug("PlotWidgetController.setAxesAndData: Error occurred: %s" % e)


    def setAxes(self):
        '''
        Defines the plot's axes.
        '''
        try:
            self.axes.clear()
            self.axes.grid(True)

            # set x label
            for entityDataList in self.data.values():
                for entityData in entityDataList:
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
                #
                #        if OPTION_SHOW_LEGEND in self.options and self.options[OPTION_SHOW_LEGEND]:
                #            self.axes.legend()
        except Exception as e:
            logging.debug("PlotWidgetController.setAxes: Error occurred: %s" % e)

    def setData(self):
        try:
            if self.data:
                for j, entityDataList in enumerate(self.data.values()):
                    for entityData in entityDataList:
                        timepoints = entityData.timepoints
                        datapoints = entityData.datapoints
                        label = entityData.getId()
                        
                        # logging.debug("PlotWidgetController.setData(): Plotting information for %s" % str(label))
                        # logging.debug("                              : x-axes (timepoints) dim %d" % len(timepoints))
                        # logging.debug("                              : y-axes (datapoints) dim %d" % len(datapoints))
                        # logging.debug("timepoints: %s" % timepoints)
                        # logging.debug("datapoints: %s" % datapoints)

                        # select correct plot style (points, lines) based
                        # on what has been set from the outside (e.g. SimulationWorkbench)
                        if entityData.getAssociatedDataSet():
                            originID = entityData.getAssociatedDataSet().getId()
                        else:
                            originID = None
                        if originID in self.dataSourceIDs:
                            dataIndex = self.dataSourceIDs.index(originID)
                            if dataIndex in self.plotStyle:
                                plotStyle = self.plotStyle[dataIndex]
                            else:
                                plotStyle = self.plotStyle[0]   # 0 as key always exists
                        else:
                            plotStyle = self.plotStyle[0]   # 0 as key always exists

                        # handle colour (prepend the colour code to style string)
                        if (originID, label) in self.plotColors:    # for string-based DataSet keys (e.g. loaded data file)
                            color = self.plotColors[(originID, label)]
                        elif entityData.sbmlEntity and (originID, entityData.sbmlEntity) in self.plotColors: # for sbmlEntity-based DataSet keys (e.g. simulation run)
                            color = self.plotColors[(originID, entityData.sbmlEntity)]
                        else:
                            color = "black" # default... should never happen :)
                            logging.debug("PlotWidgetController.setData(): Reverting to default line color. This should not happen. ID: %s" % label)

                        if len(entityDataList) > 1:
                            plotLabel = "%s (%s)" % (label, originID)
                        else:
                            plotLabel = label

                        if plotStyle == PLOT_LINE:
                            self.axes.plot(timepoints, datapoints, color=color, linestyle=plotStyle, label=plotLabel)
                        elif plotStyle == PLOT_POINT or plotStyle == PLOT_CIRCLE:
                            self.axes.plot(timepoints, datapoints, color=color, linestyle= "", marker=plotStyle, label=plotLabel)
        except Exception as e:
            logging.debug("PlotWidgetController.setData: Error occurred: %s" % e)

    def computeColors(self):
        '''
        Takes the number of data items (e.g. Species) and computes one color for each one.
        '''
        if not self.data:
            logging.error("PlotWidgetController: Can't compute colors without data.")
            return

#        if self.plotColors: # only compute once
#            return

        try:
#            numItems = self.getNumberOfDataItems()
#            if not numItems:
#                return
#
#            entityIDs = self.getSelectedEntityIDs()
#            if not entityIDs:
#                return
#
#            sourceIDs = self.getSelectedSourceIDs()
#            if not sourceIDs:
#                return

#            if len(entityIDs) != numItems:
#                logging.debug("PlotWidgetController.computeColors(): Error. Number of data items does not add up.")
#                return

            selectedSourceEntityTuples = self.getSelectedCombinations()

            numItems = len(selectedSourceEntityTuples)

            #colormap = colormaps.get_cmap("Set1")   # more default look would be "hsv"
            colors = self.map_colors(range(numItems), DEFAULT_COLORMAP)
            #logging.debug(colors)


            #if not type(self.plotColors) == dict:
            self.plotColors = {}

            for i, sourceEntityCombination in enumerate(selectedSourceEntityTuples):
                self.plotColors[sourceEntityCombination] = colors[i]

#            for i, entityID in enumerate(entityIDs):
#                for j, sourceID in enumerate(sourceIDs):
#                    self.plotColors[(entityID, sourceID)] = colors[i*j]

#            for i, entity in enumerate(dataList):
#                self.plotColors[entity[0].getId()] = colors[i]
#            dataList = self.data.values()
#            for i, entityDataList in enumerate(dataList):
#                for entityData in entityDataList:
#                    self.plotColors[entityData.getId()] = colors[i]
        except Exception, e:
            logging.debug("PlotWidgetController.computeColors(): Error while computing colors: %s" % e)

    def setPlotStyle(self, style, plotNumber=None):
        if not plotNumber:
            self.plotStyle = {0: style}
        else:
            self.plotStyle[plotNumber] = style



    # from: http://nullege.com/codes/show/src%40p%40y%40pycogent-HEAD%40cogent%40draw%40multivariate_plot.py/6/matplotlib.colors.Colormap/python
    def map_colors(self, colors, cmap=None, lut=None, mode='hexs', **norm_kw):
        """return a list of rgb tuples/hexs from color numbers.

            - colors: a seq of color numbers.
            - cmap: a Colormap or a name like 'jet' (passto cm.get_cmap(cmap, lut)
            - mode: one of  ['hexs', 'tuples', 'arrays']

        Ref: http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps
        """
        modes = ['hexs', 'tuples', 'arrays']
        if mode not in modes:
            raise ValueError('mode must be one of %s, but got %s'
            % (modes, mode))
        if not isinstance(cmap, Colormap):
            cmap = cm.get_cmap(cmap, lut=lut)
        rgba_arrays = cmap(Normalize(**norm_kw)(colors))
        rgb_arrays = rgba_arrays[:, :-1] #without alpha
        if mode == 'arrays':
            return rgb_arrays
        elif mode == 'tuples':
            return list(imap(tuple, rgb_arrays))
        else: # mode == 'hexs':
            return list(imap(rgb2hex, rgb_arrays))

    ############### SLOTS ################

    @Slot("")
    def on_actionSave_triggered(self):
        """
        Show a dialog to save the currently shown plot to a png file.

        Overrides an "abstract" method in AbstractViewController.
        """

        # get the supported formats
        formats = self.canvas.filetypes.keys()

        logging.debug("Saving plot. Displaying file chooser...")
        file_choices = "JPEG *.jpg (*.jpg);;"   # JPG is an option even if it's not natively supported
        if "png" in formats:    # if png is supported, make it the 2nd option
            file_choices += "PNG *.png (*.png);;"

        for format in formats:
            if format.lower() == "jpg" or format.lower() == "png": # we ignore this here, because it has been added already
                continue
            file_choices += "%s *.%s (*.%s);;" %(format.upper(), format, format)

        path = unicode(QFileDialog.getSaveFileName(self, 'Save file', '', file_choices)[0])
        
        frmt = path.split('.')[-1]

        if path:
            if "jpg" not in formats and frmt == "jpg":
                imgdata = StringIO.StringIO()
                self.fig.savefig(imgdata, format='png', dpi=self.dpi)
                imgdata.seek(0)  # rewind the data
                im = Image.open(imgdata)
                im.save(path)
            elif format:
                self.canvas.print_figure(path, format=frmt, dpi=self.dpi)
            else:    
                self.canvas.print_figure(path, dpi=self.dpi)

            statusBarService = StatusBarService()
            statusBarService.showMessage('Saved to %s' % path, 2000)
            
            logging.info("Saved plot to %s" % path)


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
    def on_checkBoxShowLegend_toggled(self, isChecked):
        logging.info("Switching 'Show Legend' to %s" % self.checkBoxShowLegend.isChecked())
        self.options[OPTION_SHOW_LEGEND] = isChecked
        self._updateView()


    @Slot("bool")
    def on_checkBoxLogYAxis_toggled(self, isChecked):
        logging.info("Switching 'Logarithmic Y Axis' to %s" % self.checkBoxLogYAxis.isChecked())
        self.options[OPTION_LOG_Y_AXIS] = self.checkBoxLogYAxis.isChecked()
        if isChecked:
            self.axes.set_yscale('log')
            self.canvas.draw()
        else:
            self.axes.set_yscale('linear')
            self.canvas.draw()
