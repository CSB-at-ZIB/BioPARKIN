import logging
from PySide.QtCore import Signal, QSize
from PySide.QtGui import QHeaderView, QStyleOptionButton, QStyle

class SelectableTableHeader(QHeaderView):
    """
    A custom table header view that adds a QCheckBox
    to the left side of the header. It can be used
    to (logically) select columns.

    @since: 2011-09-09
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    sectionSelectionChanged = Signal(int, bool)

    def __init__(self, orientation, parent = None):
        super(SelectableTableHeader, self).__init__(orientation, parent)

        self._isSectionSelected = {} # maps logical indexes to bool
        self._nonSelectableIndexes = []
        self.setClickable(True)
        self.sectionClicked.connect(self.on_sectionClicked) #using base SIGNAL

    def setNonSelectableIndexes(self, indexes):
        if type(indexes) == list:
            self._nonSelectableIndexes = indexes

    #### Overridden base method ######

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(SelectableTableHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        if logicalIndex in self._nonSelectableIndexes:
            return

        # check if boolean for this section exists
        if not self._isSectionSelected.has_key(logicalIndex):
            self._isSectionSelected[logicalIndex] = True # by default, sections are selected

        option = QStyleOptionButton()
        option.rect = rect
        if self._isSectionSelected[logicalIndex]:
            option.state = QStyle.State_On | QStyle.State_Enabled
        else:
            option.state = QStyle.State_Off | QStyle.State_Enabled
        self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def sizeHint(self):
        orgSize = super(SelectableTableHeader, self).sizeHint()
        return orgSize+QSize(15,0)  # add 15 horizontal pixels to account for the checkbox

#    def minimumSizeHint(self):
#        return self.sizeHint()
#
#    def sectionSizeHint(self, section):
#        orgWidth = super(SelectableTableHeader, self).sectionSizeHint(section)
#        logging.debug("Original column width: %s" % orgWidth)
#        return orgWidth+15  # add 15 horizontal pixels to account for the checkbox


#    def sizeHintForColumn(self, column):
#        orgWidth = super(SelectableTableHeader, self).sizeHintForColumn(column)
#        logging.debug("Original column width: %s" % orgWidth)
#        return orgWidth+15  # add 15 horizontal pixels to account for the checkbox
#
#    def sizeHintForRow(self, row):
#        orgHeight = super(SelectableTableHeader, self).sizeHintForColumn(row)
#        logging.debug("Original row height: %s" % orgHeight)
#        return orgHeight+15  # add 15 horizontal pixels to account for the checkbox


    #### SLOTs ####

    def on_sectionClicked(self, logicalIndex):
        if logicalIndex in self._nonSelectableIndexes:
            return
            
        # swap the selection state
        if self._isSectionSelected[logicalIndex]:
          selected = False
        else:
          selected = True
        self._isSectionSelected[logicalIndex] = selected

        self.updateSection(logicalIndex)
        self.sectionSelectionChanged.emit(logicalIndex, selected)


  