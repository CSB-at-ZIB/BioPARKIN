import logging
from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex
from basics.helpers import enum
from datamanagement.entitydata import EntityData

STATE = enum.enum("STATE", "CHECKED, UNCHECKED, NODATA")

class DataBrowserModel(QAbstractTableModel):
    """
    This class provides a table-based, Excel-like
    "view" at a DataSet object (that holds tabular, numerical
    data).
    It inherits from QAbstractTableModel, so that Qt Views,
    especially a QTableView, can easily use this model.

    What makes this QTableModel different from almost all other
    table models in BioParkin is the circumstance that the number of
    columns is not fixed. It has to be handled dynamically depending
    on the actual data.

    @since: 2011-08-26
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    def __init__(self, parent, id, dataSet):
        super(DataBrowserModel, self).__init__(parent)

        self.id = id
        self.dataSet = dataSet

        self.Dirty = False
        self.dataEntityIds = []
        self.dataDescriptors = []

        # connect to SIGNALs
        self.dataSet.dataChanged.connect(self.on_dataChanged)

        self._initData()


    # methods necessary for read-only models
    # experimentalData()
    # rowCount()
    # columnCount()
    # headerData() (almost always)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() <= len(self.dataDescriptors)) or not (
            0 <= index.column() <= len(self.dataEntityIds)):
            return

        row = index.row()
        column = index.column()

        if role == Qt.TextAlignmentRole:
            if column == 0:
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignCenter

        if role == Qt.DisplayRole or role == Qt.EditRole:
            value = self._getData(column, row)
            return value # just display the data of this cell

        return

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Will simply return the (1-based) number of the row/column.
        Actual headers (both vertical and horizontal) will be given
        in the first row/column, so that they can be edited.
        This is similar to how any spreadsheet software works.
        """
        if role != Qt.DisplayRole:
            return None
        return section + 1 # just number the rows and columns (almost like in Excel)


    def rowCount(self, index=QModelIndex()):
        return len(self.dataDescriptors) + 1 # +1, because we need one additional row at the top

    def columnCount(self, index=QModelIndex()):
        return len(self.dataEntityIds) + 1 # +1, because we need one additional column to the left


    # methods necessary for editable models
    # flags()
    # setData()

    def flags(self, index):
        if not index.isValid() or not (0 <= index.row() <= len(self.dataDescriptors)) or not (
            0 <= index.column() <= len(self.dataEntityIds)):
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled


    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.dataDescriptors) and 0 <= index.column() <= len(
            self.dataEntityIds):
            row = index.row()
            column = index.column()

            if role == Qt.EditRole:
                self._setData(row, column, value)
                self.dataChanged.emit(index, index)
                return True

        return False

    #### PUBLIC METHODS ####

    def getEntityData(self, columnIndex):
        if columnIndex - 1 < 0:
            return
        
        try:
            dataId = self.dataEntityIds[columnIndex - 1] # self.dataEntityIds starts in column 1
            return self.dataSet.getData(dataId)
        except:
            return


    ##### INTERNAL METHODS ######

    def _initData(self):
        """
        Goes through the data and extracts key info
        like number of rows and columns.

        Also has to check if every
        row (e.g. for timepoint xy) is available for every entity (e.g. Species).
        If not, this has to be managed intelligently (e.g. conveying to the user
        that there is no information for this cell).
        This can happen because the data-approach is not really a table-based one
        but has to be mapped to a table.

        Every entity (e.g. Species) can have any number of data descriptors (e.g.
        Timepoints). But these descriptors need not be identical (though, in
        most cases, they are).
        Note: The data descriptors also need *not* be in the same order inside the
        different EntityData objects. This has to be handled as well.
        """

        self.dataEntityIds = self.dataSet.getDataIds()

        if self.dataSet.dataDescriptors:    # DataSet defines global descriptors (e.g. list of timepoints)
            self.dataDescriptors = self.dataSet.dataDescriptors
        else:
            for id in self.dataEntityIds:
                entityData = self.dataSet.getData(id)
                for dataDescriptor in enumerate(entityData.dataDescriptors):
                    if dataDescriptor not in self.dataDescriptors:
                        self.dataDescriptors.append(dataDescriptor[1])


    def _getData(self, column, row):
        if column == 0:
            # get the appropriate data descriptor
            if row == 0:
                return self.dataSet.descriptorHeader
            return self.dataDescriptors[row - 1]
        elif row == 0:
            # get the appropriate data ID
            dataId = self.dataEntityIds[column - 1]
            return self.dataSet.getData(dataId).getHeader()


        # Attention! We decrease both row and column by 1,
        # so that they now correspond to actual indexes within
        # the data
        row -= 1
        column -= 1

        dataId = self.dataEntityIds[column]
        return self.dataSet.getData(dataId).getDataPointAtIndex(row)


    def _setData(self, row, column, value):
        if column == 0:
            # get the appropriate data descriptor
            if row == 0:
                self.dataSet.setDescriptorHeader(value)
                return

            self.dataSet.setDescriptor(row - 1, value)
            return
        elif row == 0:
            # get the appropriate data ID
            dataId = self.dataEntityIds[column - 1]
            self.dataSet.getData(dataId).setHeader(value)
            return


        # Attention! We decrease both row and column by 1,
        # so that they now correspond to actual indexes within
        # the data
        row -= 1
        column -= 1

        dataId = self.dataEntityIds[column]
        self.dataSet.getData(dataId).setDatapoint(row, value)

    def doTimeshift(self, shift):

        try:
            self.modelAboutToBeReset.emit()
            

            logging.info("Timeshifting data of DataSet: %s" % self.dataSet.getId())
            self.dataSet.dataDescriptors = [float(x) + shift for x in self.dataSet.dataDescriptors]  # only works on non-text descriptors

            for entity, entityData in self.dataSet.getData().items():
                id = entity.getId() if type(entity) == EntityData else str(entity)
                logging.debug("Timeshifting data of EntityData: %s" % id)
                entityData.dataDescriptors = [float(x) + shift for x in entityData.dataDescriptors]

            self._initData()
            self.modelReset.emit()
        except Exception, e:
            logging.error("DataBrowserModel.doTimeshift(): Error while timeshifting the data: %s" % e)

        ###### SLOTS #######

    def on_dataChanged(self, dataSet, entityData):
        # TODO: Use the given information to update only the right part of the model.
        self.dataChanged.emit(QModelIndex(), QModelIndex())