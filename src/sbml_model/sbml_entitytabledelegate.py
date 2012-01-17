from PySide.QtGui import QStyledItemDelegate, QComboBox, QListView, QAbstractItemView
import sbml_entitytablemodel
import sbml_entities
from PySide.QtCore import Qt


class SBMLEntityTableDelegate(QStyledItemDelegate):
    """
    This Delegate is not used right now!

    Provides a delegate to style the display and editing
    of the SBMLEntityTableModle.

    In particular, there are dropdowns for relevant options like
    assigning Reactants and Products to a Reaction (choosing from the list
    of existing Species IDs).
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"

# We can omit the init, because it does nothing than calling super().
#    def __init__(self, parent=None):
#        super(SBMLEntityTableDelegate, self).__init__(parent)


# We don't have to reimplement paint
#    def paint(self, painter, option, index):
#        if index.column() == DESCRIPTION:
#            text = index.model().data(index).toString()
#            palette = QApplication.palette()
#            document = QTextDocument()
#            document.setDefaultFont(option.font)
#            if option.state & QStyle.State_Selected:
#                document.setHtml(QString("<font color=%1>%2</font>")
#                        .arg(palette.highlightedText().color().name())
#                        .arg(text))
#            else:
#                document.setHtml(text)
#            color = (palette.highlight().color()
#                     if option.state & QStyle.State_Selected
#                     else QColor(index.model().data(index,
#                                 Qt.BackgroundColorRole)))
#            painter.save()
#            painter.fillRect(option.rect, color)
#            painter.translate(option.rect.x(), option.rect.y())
#            document.drawContents(painter)
#            painter.restore()
#        else:
#            QStyledItemDelegate.paint(self, painter, option, index)


# Currently, we don't need a size hint. Standard sizes are fine.
#    def sizeHint(self, option, index):
#        fm = option.fontMetrics
#        if index.column() == TEU:
#            return QSize(fm.width("9,999,999"), fm.height())
#        if index.column() == DESCRIPTION:
#            text = index.model().data(index).toString()
#            document = QTextDocument()
#            document.setDefaultFont(option.font)
#            document.setHtml(text)
#            return QSize(document.idealWidth() + 5, fm.height())
#        return QStyledItemDelegate.sizeHint(self, option, index)


    def createEditor(self, parent, option, index):
#        if index.model().dataMode == sbml_entities.TYPE.COMPARTMENT:
#            return self.dataCompartment(index, role)
#        elif self.dataMode == sbml_entities.TYPE.SPECIES:
#            return self.dataSpecies(index, role)
        #el
        if index.model().dataMode == sbml_entities.TYPE.REACTION:
            return self.createEditorReaction(parent, option, index)
#        elif self.dataMode == sbml_entities.TYPE.PARAMETER:
#            return self.dataParameter(index, role)
#        elif self.dataMode == sbml_entities.TYPE.RULE:
#            return self.dataRule(index, role)

#        if index.column() == TEU:
#            spinbox = QSpinBox(parent)
#            spinbox.setRange(0, 200000)
#            spinbox.setSingleStep(1000)
#            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
#            return spinbox
#        elif index.column() == OWNER:
#            combobox = QComboBox(parent)
#            combobox.addItems(sorted(index.model().owners))
#            combobox.setEditable(True)
#            return combobox
#        elif index.column() == COUNTRY:
#            combobox = QComboBox(parent)
#            combobox.addItems(sorted(index.model().countries))
#            combobox.setEditable(True)
#            return combobox
#        elif index.column() == NAME:
#            editor = QLineEdit(parent)
#            self.connect(editor, SIGNAL("returnPressed()"),
#                         self.commitAndCloseEditor)
#            return editor
#        elif index.column() == DESCRIPTION:
#            editor = richtextlineedit.RichTextLineEdit(parent)
#            self.connect(editor, SIGNAL("returnPressed()"),
#                         self.commitAndCloseEditor)
#            return editor
        else:
            return QStyledItemDelegate.createEditor(self, parent, option,
                                                    index)

    def createEditorReaction(self, parent, option, index):
        '''
        Creates the editor if a Reaction is shown.
        '''
        if index.column() == sbml_entitytablemodel.REACTION_ROW.REACTANTS:
            list = QListView(parent)
            list.setSelectionMode(QAbstractItemView.MultiSelection)

#            combobox = QComboBox(parent)
            speciesIDs = []
            for speciesWrapper in index.model().mainModel.SbmlSpecies:
                speciesIDs.append(speciesWrapper.getId())

            #list. #adding the species...
#

#            combobox.addItems(sorted(speciesIDs))
#            #combobox.setEditable(True)
#            return combobox

        else:
            return QStyledItemDelegate.createEditor(self, parent, option,
                                                    index)

#    def commitAndCloseEditor(self):
#        editor = self.sender()
#        if isinstance(editor, (QTextEdit, QLineEdit)):
#            self.emit(SIGNAL("commitData(QWidget*)"), editor)
#            self.emit(SIGNAL("closeEditor(QWidget*)"), editor)


    def setEditorData(self, editor, index):
#        text = index.model().data(index, Qt.DisplayRole).toString()
#        if index.column() == TEU:
#            value = text.replace(QRegExp("[., ]"), "").toInt()[0]
#            editor.setValue(value)
#        elif index.column() in (OWNER, COUNTRY):
#            i = editor.findText(text)
#            if i == -1:
#                i = 0
#            editor.setCurrentIndex(i)
#        elif index.column() == NAME:
#            editor.setText(text)
#        elif index.column() == DESCRIPTION:
#            editor.setHtml(text)
        if index.model().dataMode == sbml_entities.TYPE.REACTION:
            self.setEditorDataReaction(editor, index)
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    def setEditorData(self, editor, index):
        if index.column() == sbml_entitytablemodel.REACTION_ROW.REACTANTS:
            text = index.model().data(index, Qt.DisplayRole).toString()
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
#        if index.column() == TEU:
#            model.setData(index, QVariant(editor.value()))
#        elif index.column() in (OWNER, COUNTRY):
#            model.setData(index, QVariant(editor.currentText()))
#        elif index.column() == NAME:
#            model.setData(index, QVariant(editor.text()))
#        elif index.column() == DESCRIPTION:
#            model.setData(index, QVariant(editor.toSimpleHtml()))
        if index.model().dataMode == sbml_entities.TYPE.REACTION:
            self.setModelDataReaction(editor, model, index)
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)

    def setModelDataReaction(self, editor, model, index):
        if index.column() == sbml_entitytablemodel.REACTION_ROW.REACTANTS:
            model.setData(index, editor.currentText())
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)