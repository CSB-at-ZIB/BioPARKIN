import logging
from PySide.QtCore import Signal, QSize, Slot, QModelIndex, Qt
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

    sectionSelectionChanged = Signal(int, Qt.CheckState)

    def __init__(self, orientation, parent = None):
        super(SelectableTableHeader, self).__init__(orientation, parent)

        self._selectionModel = None
        self._isSectionSelected = {} # maps logical indexes to Qt.Checked/Qt.Unchecked/Qt.PartiallyChecked
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
            if self._selectionModel:
                if self.orientation() == Qt.Horizontal:
                    self._isSectionSelected[logicalIndex] = self._selectionModel.getColSelectionState(logicalIndex)
                elif self.orientation() == Qt.Vertical:
                    self._isSectionSelected[logicalIndex] = self._selectionModel.getRowSelectionState(logicalIndex)
            else:
                self._isSectionSelected[logicalIndex] = Qt.Checked

        option = QStyleOptionButton()
        option.rect = rect
        if self._isSectionSelected[logicalIndex] == Qt.Checked:
            option.state = QStyle.State_On | QStyle.State_Enabled
        elif self._isSectionSelected[logicalIndex] == Qt.Unchecked:
            option.state = QStyle.State_Off | QStyle.State_Enabled
        elif self._isSectionSelected[logicalIndex] == Qt.PartiallyChecked:
            option.state = QStyle.State_NoChange | QStyle.State_Enabled
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


    def connectSelectionModel(self, selectionModel):
        """
        Note: The "selectionModel" is *not* a QSelectionModel. It just happens
        to be a QAbstractItemModel that handles selections.
        """
        if self._selectionModel:
            self._selectionModel.dataChanged.disconnect(self.on_selectionModelChanged)

        self._selectionModel = selectionModel

        if self._selectionModel:
            self._selectionModel.dataChanged.connect(self.on_selectionModelChanged)

    #### SLOTs ####

    def on_sectionClicked(self, logicalIndex):
        if logicalIndex in self._nonSelectableIndexes:
            return
            
        # swap the selection state
        if self._isSectionSelected[logicalIndex] == Qt.Checked:
            selected = Qt.Unchecked
        elif self._isSectionSelected[logicalIndex] == Qt.Unchecked:
            selected = Qt.Checked
        elif self._isSectionSelected[logicalIndex] == Qt.PartiallyChecked:
            selected = Qt.Checked # check partially checked cols/rows with the first click
            # Wikipedia says so! ;) http://en.wikipedia.org/wiki/Checkbox
            #  "The indeterminate state cannot usually be selected by the user, and switches to a checked state when activated."
        self._isSectionSelected[logicalIndex] = selected

        self.updateSection(logicalIndex)
        self.sectionSelectionChanged.emit(logicalIndex, selected)

    @Slot(QModelIndex, QModelIndex)
    def on_selectionModelChanged(self, topLeftIndex, bottomRightIndex):
        """
        Whenever some selection in the supplied "selection model"
        is changed, we have to check whether this change affects
        one of self._isSectionSelected. That depends on whether
        self has vertical or horizontal orientation.

        We also have to check the state within the given "selection
        model" to assess whether the internal sections are completely
        checked/unchecked or in an intermediate state.
        (To be able to do this, self._isSectionSelected has to store "more"
        than just a bool. We now use a the Qt.Checkstate enum which has
        Qt.PartiallyChecked.)

        The indices given by the two QModelIndex correspond to the internal
        sections by design.
        """
        if self.orientation() == Qt.Horizontal: # default orientation
            affectedColLeft = topLeftIndex.column()
            affectedColRight = bottomRightIndex.column()

            # Now, loop over this area of the "selection model"
            for affectedSection in xrange(affectedColLeft, affectedColRight+1):
                state = self._selectionModel.getColSelectionState(affectedSection)
                if state is not None: # check against None explicitely, as it might very well be 0
                    self._isSectionSelected[affectedSection] = state
                self.updateSection(affectedSection)

        elif self.orientation() == Qt.Vertical:
            affectedRowTop = topLeftIndex.row()
            affectedRowBottom = bottomRightIndex.row()

            # Now, loop over this area of the "selection model"
            for affectedSection in xrange(affectedRowTop, affectedRowBottom+1):
                state = self._selectionModel.getRowSelectionState(affectedSection)
                if state is not None: # check against None explicitely, as it might very well be 0
                    self._isSectionSelected[affectedSection] = state
                self.updateSection(affectedSection)
            





  