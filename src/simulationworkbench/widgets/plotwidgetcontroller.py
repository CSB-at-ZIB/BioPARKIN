import StringIO
import Image

import PySide.QtXml # as suggested in a forum to account for .svg icons
from PySide.QtGui import QFileDialog, QVBoxLayout
from PySide.QtCore import  Slot
import logging
from services.statusbarservice import StatusBarService
from simulationworkbench.widgets.abstractviewcontroller import AbstractViewController

from itertools import cycle, imap

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = "PySide"
 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from matplotlib import cm
from matplotlib.colors import rgb2hex, Normalize, Colormap

from matplotlib.figure import Figure
from simulationworkbench.widgets.Ui_plotwidget_v2 import Ui_PlotWidget

from plotstylemanager import PlotStyleManager
#from plotstyle import PlotStyleManager

OPTION_LABEL_X = "option_label_x"
OPTION_SHOW_LEGEND = "option_show_legend"
OPTION_LOG_Y_AXIS = "option_log_y_axis"

PLOT_LINE = '-'
PLOT_POINT = '.'
PLOT_CIRCLE = "o"

DEFAULT_COLORMAP = "spectral" # also possible: Set1, hsv, spectral
# more: http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps

MARKER_STYLES = ['.',',','o','v','^','<','>','1','2','3','4','s','p','*','h','H','+','x','D','d','|','_']

LINE_STYLES = ['-','--','-.',':']

COLOR_STYLES = ['spectral','gray']

def getColorMap(colorMap='spectral',numberOfItems=1,**norm_args):
    if not isinstance(colorMap,str): raise TypeError('\nIncorrect type: %s'%colorMap.__class__)
    if not isinstance(numberOfItems,int):raise TypeError('\nIncorrect type: %s'%colorMap.__class__)
    if numberOfItems<=0: raise ValueError('\nNon positive number of items!')
    if not norm_args: norm_args = {}
    try:
        #from matplotlib import cm
        minItems = min(numberOfItems,11)
        cmap = cm.get_cmap(colorMap, numberOfItems)
        colorM = cmap(Normalize(**norm_args)(range(minItems)))
        colorM1= colorM[:-2,:]
        return list(imap(tuple,colorM1))
    except Exception: raise TypeError ('\nNo such color map: %s'%colorMap)


class PlotWidgetController(AbstractViewController, Ui_PlotWidget):
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
        #super class constructor
        super(PlotWidgetController, self).__init__(parent)
        
        
        self.setupUi(self)
        self.setWindowTitle(title)

        self._initialize()

        self.timeUnit = "a.u." #default ?
        if host:
            self.timeUnit = str(host.optionTimeUnit)

        #options: time unit, logarithmic y-axis and 'show legend'
        self.options = {
            OPTION_LABEL_X: "Time [%s]" % (self.timeUnit), #default
            OPTION_LOG_Y_AXIS: self.checkBoxLogYAxis.isChecked(),
            OPTION_SHOW_LEGEND: self.checkBoxShowLegend.isChecked()
        }

        self.host = host
        self.title = title

        self.data = None
        self.labels = None

        self.fig = None
        self.canvas = None
        self.axes = None
        self.mpl_toolbar = None
        self.dpi = None
        
        self.useGrayColor = False
        
        self.plotStyleManager = PlotStyleManager()
        if self.title!='Plot': self.plotStyleManager.setDataType(self.title)

        self.plotStyle = {
            0: PLOT_LINE} #default plot style; if there are more elements, each numbered element corresponds to one data source
        self.plotColors = {}    # will be filled with colors on the first plot



    def _updateView(self, data=None):
        '''
        '''
        #wrap it in a try-catch
        try:
            
            #if the data argument is not None
            #assign it to the instance var data
            if data:
                self.data = data

            if not self.fig:    # on first plot
                self.dpi = self.logicalDpiX()
                logging.info("Plotting at %s dpi." % self.dpi)
                self.fig = Figure(dpi=self.dpi)
                self.canvas = FigureCanvas(self.fig)

                self.axes = self.fig.add_subplot(111)
                self.mpl_toolbar = NavigationToolbar(self.canvas, None)

                left_vbox = QVBoxLayout(self.plotWrapper)
                left_vbox.addWidget(self.canvas)
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
            #TODO: deprecated since a new plot style manager class!!!
            #if not self.plotStyleManager.colorMap: self.plotStyleManager.setColorMap('spectral')
            self.computeColors()
            
            #if no color map specified yet - set default to spectral
            
            from plotstylemanager import DATA_TYPES
            if not self.plotStyleManager.dataType and self.title in DATA_TYPES:self.plotStyleManager.dataType = self.title
            # some of this has to be done before the data is set
            self.setAxes()
            self.setData()

            # has to be done after the data is set
            if OPTION_SHOW_LEGEND in self.options and self.options[OPTION_SHOW_LEGEND]:
                self.axes.legend()

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

        except Exception as e:
            logging.debug("PlotWidgetController.setAxes: Error occurred: %s" % e)

    def setData(self):
        try:#wrap it in a try-catch close
            
            #BEGIN if-if there's some data
            if self.data:

                #get new cyclic iterators over the marker styles, line style and color                
                markerIt, lineIt= self.plotStyleManager.getMarkerIterator(), self.plotStyleManager.getLineIterator()
                expPlot = True
                markr = None
                
                #BEGIN for-iterating over the data values
                for j, entityDataList in enumerate(sorted(self.data.values())):
                    
                    #BEGIN for-iterating over the data entities
                    for entityData in entityDataList:
                        timepoints = entityData.timepoints
                        datapoints = entityData.datapoints
                        label = entityData.getId()

                        #first, get the right plotting style info for
                        #the current data entity:
                        #
                        #1. getting the associated entity id
                        if entityData.getAssociatedDataSet():
                            originID = entityData.getAssociatedDataSet().getId()
                            
                        #if no such id
                        else:
                            originID = None
                        #TODO: deprecated!!!
                        #2. check if there is some data source id associated
                        #   with data entity id
                        #if originID in self.dataSourceIDs:
                        #    dataIndex = self.dataSourceIDs.index(originID)
                        #    
                        #    #2a. if there is, get the corresponding plotting style
                        #    if dataIndex in self.plotStyle:
                        #        plotStyle = self.plotStyle[dataIndex]
                            #2b. if no such style is there, take the default plotting
                        #    #    style always associated with 0-key,
                        #    else:
                        #        plotStyle = self.plotStyle[0]
                                
                        #2c. if no such source id found, use default plotting style    
                        #else:
                        #    plotStyle = self.plotStyle[0]

                        # handle colour (prepend the colour code to style string)
                        if self.checkBoxOneColorPerRow.isChecked():
                            if label in self.plotColors:    # for string-based DataSet keys (e.g. loaded data file)
                                color = self.plotColors[label]
                            elif entityData.sbmlEntity and entityData.sbmlEntity in self.plotColors: # for sbmlEntity-based DataSet keys (e.g. simulation run)
                                color = self.plotColors[entityData.sbmlEntity]
                            else:
                                color = "black" # default... should never happen :)
                                logging.debug("PlotWidgetController.setData(): Reverting to default line color. This should not happen. ID: %s" % label)
                        else:
                            if (originID, label) in self.plotColors:    # for string-based DataSet keys (e.g. loaded data file)
                                color = self.plotColors[(originID, label)]
                            elif entityData.sbmlEntity and (originID, entityData.sbmlEntity) in self.plotColors: # for sbmlEntity-based DataSet keys (e.g. simulation run)
                                color = self.plotColors[(originID, entityData.sbmlEntity)]
                            else:
                                color = "black" # default... should never happen :)
                                logging.debug("PlotWidgetController.setData(): Reverting to default line color. This should not happen. ID: %s" % label)
                        #print 'data type: '+str((originID,label,self.title))
                        # 31.07.12 td
                        #   inserted an additional space in front of plotLabel 
                        #   (in case of IDs with underscore as first character)
                        # 26.07.12 td
                        #   the following line yields no originID in plot label if only one column 
                        #   is selected in sens overview...
                        # if len(entityDataList) > 1:
                        if not self.useGrayColor:
                            if originID and ("Sensitivity (Plot)" in self.title):  # awful hack
                                plotLabel = " %s (%s) " % (label, originID)
                            else:
                                plotLabel = " %s " % (label)
                            if expPlot: markr = markerIt.next()
                            if 'Simulation' in self.title:
                                if 'Simulation' in originID:
                                    self.axes.plot(timepoints,datapoints,color=color,linestyle='-',label=plotLabel)#,marker=markr,markeredgecolor='black',markerfacecolor=color,label=plotLabel)
                                    expPlot = True
                                else:
                                    self.axes.plot(timepoints,datapoints,color=color,linestyle='-',marker='o',markeredgecolor='black',markerfacecolor=color,label=plotLabel)#,marker=markr,markeredgecolor='black',markerfacecolor=color,label=plotLabel)
                                    expPlot = False
                            elif 'Sensitivity' in self.title:
                                self.axes.plot(timepoints,datapoints,color=color,linestyle='-',label=plotLabel)#,marker=markr,markeredgecolor='black',markerfacecolor=color,label=plotLabel)
                                expPlot = False
                            else:    #while markr=='o': markr = markerIt.next()
                                self.axes.plot(timepoints,datapoints,color=color,linestyle=lineIt.next(),marker='o',markeredgecolor='black',markerfacecolor=color,label=plotLabel)
                                expPlot = True
                            #if plotStyle == PLOT_LINE:
                            #    self.axes.plot(timepoints, datapoints, color=color, linestyle=lineIt.next(), label=plotLabel)
                            #elif plotStyle == PLOT_POINT or plotStyle == PLOT_CIRCLE:
                            #    self.axes.plot(timepoints, datapoints, color=color, linestyle= "", marker=plotStyle, label=plotLabel)
                        else:
                            if originID and ("Sensitivity (Plot)" in self.title):  # awful hack
                                plotLabel = " %s (%s) " % (label, originID)
                            else:
                                plotLabel = " %s " % (label)
                            if not expPlot: markr = markerIt.next()
                            if 'Simulation' in self.title:
                                if expPlot: markr = markerIt.next()
                                if 'Simulation' in originID:
                                    if markr=='o': markr = markerIt.next()                           
                                    self.axes.plot(timepoints,datapoints,color=color,linestyle=lineIt.next(),marker=markr,markeredgecolor='black',markerfacecolor=color,label=plotLabel)
                                    expPlot = True
                                else:
                                    self.axes.plot(timepoints,datapoints,color=color,linestyle=lineIt.next(),marker='o',markeredgecolor='black',markerfacecolor=color,label=plotLabel)
                                    expPlot = False
                            elif 'Sensitivity' in self.title:
                                self.axes.plot(timepoints,datapoints,color=color,linestyle=lineIt.next(),marker=markr,markeredgecolor='black',markerfacecolor=color,label=plotLabel)#,marker=markr,markeredgecolor='black',markerfacecolor=color,label=plotLabel)
                                expPlot = False
                            else:
                                if markr in 'o': markr = markerIt.next()
                                self.axes.plot(timepoints,datapoints,color=color,linestyle=lineIt.next(),marker='o',markeredgecolor='black',markerfacecolor=color,label=plotLabel)
                                expPlot = True
                    #END for
                    
                #END for
                
            #END if
            
        #catch exception and write to the debug logger
        except Exception as e:
            logging.debug("PlotWidgetController.setData: Error occurred: %s" % e)

    def computeColors(self):
        """
        Takes the number of data items (e.g. Species) and computes one color for each one.
        """
        #check data object present
        if not self.data:
            
            #error - info: no data source to color
            logging.error("PlotWidgetController: Can't compute colors without data.")
            
            return

        try:
            
            #check, whether the color per row checkbox is activated
            if self.checkBoxOneColorPerRow.isChecked():
                
                
                entityIDs = self.getEntityIDs()
                
                #no entries - nothing to color
                if not entityIDs:
                    return
                
                #number of entity ids determines the number of color object to construct
                #numItems = len(entityIDs)
            else:
                
                selectedSourceEntityTuples = self.getSelectedCombinations()
                #numItems = len(selectedSourceEntityTuples)
            #TODO: fix color item issue - only 10 items in 'spectral' though should
            #TODO: be 22 ?!
            #
            #get the color map - one color object per item (entity)
            #colors = self.map_colors(range(numItems), DEFAULT_COLORMAP)
            #if self.plotStyleManager.items<numItems:
            if self.checkBoxOneColorPerRow.isChecked() and entityIDs: self.plotStyleManager.setItems(len(entityIDs))
            elif selectedSourceEntityTuples:self.plotStyleManager.setItems(len(selectedSourceEntityTuples))
            colorIt = self.plotStyleManager.getColorIterator()
            self.plotColors = {}

            if self.checkBoxOneColorPerRow.isChecked():
                for j, entityID in enumerate(entityIDs):
                    self.plotColors[entityID] = colorIt.next()
            else:
                for j, sourceEntityCombination in enumerate(selectedSourceEntityTuples):
                    self.plotColors[sourceEntityCombination] = colorIt.next()

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

        from: http://nullege.com/codes/show/src%40p%40y%40pycogent-HEAD%40cogent%40draw%40multivariate_plot.py/6/matplotlib.colors.Colormap/python
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

        logging.info("Saving plot. Displaying file chooser...")
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
            elif frmt:
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

    @Slot("bool")
    def on_checkBoxOneColorPerRow_toggled(self, isChecked):
        logging.info("Switching plot coloring mode.")
        self._updateDataView()
    @Slot("bool")
    def on_checkBoxGrayColor_toggled(self, isChecked):
        if isChecked:
            logging.info("Switching plot coloring mode to gray")
            self.plotStyleManager.isGray = True
            #self.plotStyleManager.setItems(11)
            self.plotStyleManager.setColorMap('gray')
        else:
            logging.info("Switching plot coloring mode to spectral")
            self.plotStyleManager.isGray = False
            if self.plotStyleManager.items==1: self.plotStyleManager.setItems(len(self.allData.keys()))
            self.plotStyleManager.setColorMap('spectral')
        self.useGrayColor = isChecked
        self._updateDataView()