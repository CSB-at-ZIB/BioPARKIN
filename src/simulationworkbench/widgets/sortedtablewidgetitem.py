import logging
from PySide.QtCore import Qt
from PySide.QtGui import QTableWidgetItem

class SortedTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            float(self.data(Qt.DisplayRole))
            selfIsFloat = True
        except :
            selfIsFloat = False

        try:
            float(other.data(Qt.DisplayRole))
            otherIsFloat = True
        except :
            otherIsFloat = False


        if selfIsFloat and otherIsFloat:
            return float(self.data(Qt.DisplayRole)) < float(other.data(Qt.DisplayRole))
        elif not selfIsFloat and not otherIsFloat:
            return self.data(Qt.DisplayRole) < other.data(Qt.DisplayRole)
        elif selfIsFloat:
            return True
        else:
            return False


#    def data(self, role):
#        if role != Qt.DisplayRole:
#            return super(SortedTableWidgetItem, self).data(role)
#
#        data = super(SortedTableWidgetItem, self).data(role)
#        try:
#            floatData = float(data)
#            floatData = '{0:-.4f}'.format(floatData)
#            return floatData
#        except :
#            return data

