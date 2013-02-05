'''
Created on 11.12.2012

@author: bzfmuell
'''

from itertools import cycle


MARKER_STYLES = ['.',',','o','v','^','<','>','1','2','3','4','s','p','*','h','H','+','x','D','d','|','_']

LINE_STYLES = ['-','--','-.',':']

COLOR_STYLES = ['spectral','gray']

DATA_TYPES = ['Simulation','/']


class PlotStyleManager ():
    '''
    Class managing the all plot relevant details as
    - the color map
    - the line styles
    - the marker styles
    according to the data type and mode the manager has been set
    '''
    def __init__(self):
        '''
        Constructs an empty plot style manager
        the 
        '''
        self.items = 0
        self.colorMap = None
        self.isGray   = False
        self.dataType = None
        self.colorIt  = None
        self.lineIt   = None
        self.markerIt = None
        
    def __cmp__(self,other):
        if(isinstance(other,PlotStyleManager)):
            if(self.items<other.items): return -1
            if(self.items==other.items):return 0
            return 1
        else: raise TypeError('unknown type')
        
    def getColorIterator(self):
        '''
        Returns a cyclic iterator over all
        color values specified by the color map
        '''
        if self.colorMap:
            return cycle(self.colorMap)
        
    def getMarkerIterator(self):
        '''
        Returns a cyclic iterator over all 
        marker styles
        '''
        return cycle(MARKER_STYLES)
    
    def getLineIterator (self):
        return cycle(LINE_STYLES)
    
    def setColorMap(self,colorMap,**norm_args):
        if colorMap and isinstance(colorMap,str):
            if self.items<=0: raise ValueError('\nNon positive number of items!')
            if not norm_args: norm_args = {}
            try:
                from matplotlib import cm
                from matplotlib.colors import Normalize
                reduced = -1
                if colorMap=='gray':
                    self.isGray = True
                    minItems = 11
                    reduced = -2
                else: minItems = 23
                cmap = cm.get_cmap(colorMap, min(self.items+1,minItems+1))
                colorM = cmap(Normalize(**norm_args)(range(min(self.items+1,minItems+1))))
                from itertools import imap
                if self.items!=1:
                    self.colorMap = list(imap(tuple,colorM[:reduced,:]))
                else: self.colorMap = list(imap(tuple,colorM))
            except Exception: raise TypeError ('\nNo such color map: %s'%colorMap)
    def setDataType(self,dataType):
        if not isinstance(dataType,str): TypeError('\nUnexpected type: %s'%dataType)
        for dataStr in DATA_TYPES:
            if dataStr in dataType: self.dataType = dataStr
        if not self.dataType: ValueError('\nUnknown data type: %s'%dataType)
    def setItems(self,items=1):
        if not isinstance(items,int):raise TypeError('\nUnexpected type: %s'%items)
        if items>=1:
            if self.items!=items:
                self.items = items
                if self.isGray:self.setColorMap('gray')
                else: self.setColorMap('spectral')
        else: ValueError('\nNumber of items must be strictly positive!')
    
    
    
if __name__=='__main__':
    print min(12,25)
    plstman1 = PlotStyleManager()
    plstman1.items = 14
    plstman2 = PlotStyleManager()
    plstman2.items = 11
    if plstman1.__cmp__(plstman2)<0:
        print "plotManager1 < plotManager2"
    elif plstman1.__cmp__(plstman2)==0:
        print "plotManager1 == plotManager2"
    else: print "plotManager1 > plotManager2"
        