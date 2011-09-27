from collections import OrderedDict
import logging
from PySide.QtCore import QFileInfo
from PySide.QtGui import QWidget

from sbml_views.ui_modelview import Ui_ModelView

class ModelView(QWidget, Ui_ModelView):
    """
    Provides a list widget that connects to the main BioPARKIN controller,
    displays all current models and allows to select any of them.
    It is hooked up to events of the BioPARKIN controller so it is only loosely
    coupled and not a necessary part of the UI at all (e.g. the NetworkView can also be used to
    show and select current models).

    @since: 2011-05-16
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    def __init__(self, parent, bioParkinController):
        if not parent or not bioParkinController:
            logging.debug("ModelView: Can't instantiate without parent and controller.")
            return
        super(ModelView, self).__init__(parent) # Qt wiring
        self.setupUi(self)

        self._models = OrderedDict() # stores models
        self._modelIndexes = OrderedDict()   # stores indexes
        
        self.bioParkinController = bioParkinController
        self.bioParkinController.activeModelChanged.connect(self.on_activeModelChanged)
        self.bioParkinController.modelClosed.connect(self.on_modelClosed)

        self._modelListWidget.currentItemChanged.connect(self.on_currentItemChanged)

    def on_activeModelChanged(self, modelController):
        if not modelController:
            self._modelListWidget.setCurrentIndex(None)    # deselect all
            return

        filename = QFileInfo(modelController.filename).fileName()
        if self._modelIndexes.has_key(filename):  # known model, just select it
            self._modelListWidget.item(self._modelIndexes[filename]).setSelected(True)
        else:   # new model, add it to the list
#            truncatedFilename = QFileInfo(filename).fileName()
            self._modelListWidget.addItem(filename)
            self._models[filename] = modelController
            index = self._modelListWidget.count() - 1
            self._modelIndexes[filename] = index
            self._modelListWidget.item(index).setSelected(True)

    def on_modelClosed(self, modelController):
        if not modelController:
            return

#        filename = modelController.filename
        filename = QFileInfo(modelController.filename).fileName()
        if self._modelIndexes.has_key(filename):
            index = self._modelIndexes[filename]
#            item = self._modelListWidget.item(index)
#            self._modelListWidget.removeItemWidget(item)
            item = self._modelListWidget.takeItem(index)
            del item
            self._models.pop(filename)  # remove the model
            self._modelIndexes.pop(filename)
            if len(self._modelListWidget) > 0:
                self._modelListWidget.item(0).setSelected(True)

    def on_currentItemChanged(self, newItem, previousItem):
        if newItem:
            filename = newItem.data(0)
            if self._models.has_key(filename):
                modelController = self._models[filename]
#                self.bioParkinController.on_activeModelChanged(modelController)
                self.bioParkinController.activeModelChanged.emit(modelController)