from PySide.QtCore import Qt
from PySide.QtGui import QTableWidgetItem

class SortedTableWidgetItem(QTableWidgetItem):
    """
    A simple wrapper for QTableWidgetItem that overrides __lt__
    for custom sorting.
    If both wrapped items are floats, they are compared normally.
    Floats are defined to be smaller than non-floats.
    It both are non-floats, they are compared simply via < which
    works great for e.g. strings.
    """
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



