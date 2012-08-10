
from PySide.QtCore import Slot
from PySide.QtGui import QDialog, QFont
import libsbml
from odehandling.odegenerator import ODEGenerator
import logging
from odehandling.Ui_ODEViewer_v2 import Ui_ODEViewer

class ODEViewer(QDialog, Ui_ODEViewer):
    """
    GUI class for activating the ODE generation machinery and displaying the
    results in a text widget.
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    def __init__(self, parent, model):
        super(ODEViewer, self).__init__(parent)
        self.setupUi(self)
        self.model = model

        try:
            font = QFont("Courier", 10)
            self.plainTextEdit.setFont(font)
        except:
            logging.error("Could not set 'Courier' font for ODE Viewer window.")

        self.actionGenerateODEs.trigger()


    @Slot("")
    def on_actionGenerateODEs_triggered(self):
        """
        Open the ODE Generator information dialog.
        """
        self._printODEsWithIDs()
        self._printODEsWithNames()


    def _printODEsWithIDs(self):
        """
        Print all equations/definitions with IDs in read-only edit widget
        """
        reactions = {}

        # for now, only try to print the results to the command line
        #text = "Overview of Reactions and ODEs\n\n"
        text = ""
        text += "Individual Rate Equations:\n"
        text += "--------------------------\n\n"
        self.plainTextEdit.insertPlainText(text)

        for reactionWrapper in self.model.SbmlReactions:
            kineticLaw = reactionWrapper[0].Item.getKineticLaw()
            id = reactionWrapper[0].Item.getId()
            if kineticLaw is not None:
                mathString = libsbml.formulaToString(kineticLaw.getMath())
                reactionText = "%s: %s" % (id, mathString)
                logging.info(reactionText)
                self.plainTextEdit.insertPlainText(reactionText + "\n")
                reactions[id] = mathString
            else:
                logging.error("Reaction %s has no kinetic Law." % id)


        text = "\n\n"
        text += "ODE / DAE system:\n"
        text += "-----------------\n\n"
        self.plainTextEdit.insertPlainText(text)
        odeGenerator = ODEGenerator(self.model)
        for wrappedODE in odeGenerator.wrappedODEs:
            # 10.08.12 td: added DAE handling
            if wrappedODE.isDAE():
                odeText = "0  =  %s" % (libsbml.formulaToString(wrappedODE.mathNode))
            else:
                odeText = "d %s /dt  =  %s" % (wrappedODE.getId(), libsbml.formulaToString(wrappedODE.mathNode))
            logging.info(odeText)
            self.plainTextEdit.insertPlainText(odeText + "\n")


        # create ODEs with reaction IDs replaced with actual reaction for convenience
        text = "\n\n"
        text += "ODE/DAE (Reaction IDs replaced with actual equations)\n"
        text += "        (Assignment Rules are NOT applied here      ):\n"
        text += "------------------------------------------------------\n\n"
        self.plainTextEdit.insertPlainText(text)

        reactionIdList = []
        for reactionID in reactions.keys():
            reactionIdList.append(reactionID)

        #sort IDs by length descending
        reactionIdList.sort(cmp=self._bylength)
        reactionIdList.reverse()

        for wrappedODE in odeGenerator.wrappedODEs:
            odeID = wrappedODE.getId()
            odeMath = libsbml.formulaToString(wrappedODE.mathNode)

            for reactionID in reactionIdList:
                if reactionID in odeMath:
                    odeMath = odeMath.replace(reactionID, "(%s)" % (reactions[reactionID]))

            # 10.08.12 td: added DAE handling
            if wrappedODE.isDAE():
                odeText = "0  =  %s" % (odeMath)
            else:
                odeText = "d %s /dt  =  %s" % (odeID, odeMath)
            logging.info(odeText)
            self.plainTextEdit.insertPlainText(odeText + "\n\n")


        text = "\n\n"
        text += "Assignment Rules:\n"
        text += "-----------------\n\n"
        self.plainTextEdit.insertPlainText(text)

        assignmentRules = {}
        for assignmentRule in self.model.SbmlAssignmentRules:
            target = assignmentRule.getTarget()
            mathString = libsbml.formulaToString(assignmentRule.getMath())
            assignmentRules[target] = mathString
            ruleText = "%s = %s\n" % (target, mathString)
            self.plainTextEdit.insertPlainText(ruleText)


        text = "\n\n"
        text += "ODE/DAE (Reaction IDs replaced with actual equations)\n"
        text += "        (Assignment Rules ARE applied here          ):\n"
        text += "------------------------------------------------------\n\n"
        self.plainTextEdit.insertPlainText(text)

        reactionsWithRules = {}
        for reactionID in reactionIdList:
            reactionsWithRules[reactionID] = reactions[reactionID]
            for target, ruleMath in assignmentRules.items():
                # by checking only with the original reactions[reactionID], we don't replace targets that have been introduced by previous rule replacements
                if target in reactions[reactionID]:
                    reactionsWithRules[reactionID] = reactionsWithRules[reactionID].replace(target, ruleMath)
        for wrappedODE in odeGenerator.wrappedODEs:
            odeID = wrappedODE.getId()
            odeMath = libsbml.formulaToString(wrappedODE.mathNode)

            for reactionID in reactionIdList:
                if reactionID in odeMath:
                    odeMath = odeMath.replace(reactionID, "(%s)" % (reactionsWithRules[reactionID]))

            # 10.08.12 td: added DAE handling
            if wrappedODE.isDAE():
                odeText = "0  =  %s" % (odeMath)
            else:
                odeText = "d %s /dt  =  %s" % (odeID, odeMath)
            logging.info(odeText)
            self.plainTextEdit.insertPlainText(odeText + "\n\n")


    def _printODEsWithNames(self):
        """
        Print all equations/definitions with Names (for convenience convenience!)
        in read-only edit widget
        """

        reactions = {}
        names = self._getIdToNamesMap(self.model)

        # for now, only try to print the results to the command line
        #text = "Overview of Reactions and ODEs\n\n"
        text = ""
        text += "\n\n\n\n"
        text += "   **************************************************************\n"
        text += "   * !!!               ODE/DAE View (by Names)              !!! *\n"
        text += "   *                                                            *\n"
        text += "   * Same output as above; but now unique IDs replaced by Names *\n"
        text += "   *                                                            *\n"
        text += "   * !!! Output may NOT be consistent with given SBML model !!! *\n"
        text += "   **************************************************************\n"
        text += "\n\n\n"

        dmap = {}
        notxt = ""
        for (ID, val) in names.items():
            if val[0] == "noname":
                notxt += "ID '%s' is unnamed / has no label.\n" % (ID)
            if dmap.has_key(val[0]):
                dmap[val[0]] += (ID, )
            else:
                dmap[val[0]] = (ID, )

        dotxt = ""
        for (name, IDs) in dmap.items():
            if len(IDs) > 1:
                dotxt += "Name '%s' is used by %s.\n" % (name, IDs)

        if len(notxt) > 0:
            text += "*** Note: There are unnamed ID(s) ***\n\n"
            text += notxt
            text += "\n\n"

        if len(dotxt) > 0:
            text += "*** Note: There are ID(s) mapping to the same Name ***\n\n"
            text += dotxt
            text += "\n\n"

        text += "\n\n"

        entityIdList = []
        for entityID in names.keys():
            entityIdList.append(entityID)

        #sort IDs by length descending
        entityIdList.sort(cmp=self._bylength)
        entityIdList.reverse()

        text += "Individual Rate Equations:\n"
        text += "--------------------------\n\n"
        self.plainTextEdit.insertPlainText(text)

        for reactionWrapper in self.model.SbmlReactions:
            kineticLaw = reactionWrapper[0].Item.getKineticLaw()
            ID = reactionWrapper[0].Item.getId()
            if kineticLaw is not None:
                math = libsbml.formulaToString(kineticLaw.getMath())

                for entityID in entityIdList:
                    if entityID in math:
                        math = math.replace( entityID, "#%d#" % (names[entityID][2]) )

                for entityID in entityIdList:
                    key = "#%d#" % (names[entityID][2])
                    if key in math:
                        math = math.replace( key, "'%s{%d}'" % (names[entityID][:2]) )

                reactionText = "'%s{%d}': %s" % (names[ID][:2] + (math, ))
                logging.info(reactionText)
                self.plainTextEdit.insertPlainText(reactionText + "\n")
                reactions[ID] = math
            else:
                logging.error("Reaction '%s{%d}' has no kinetic Law." % (names[ID][:2]))

        odeGenerator = ODEGenerator(self.model)

        reactionIdList = []
        for reactionID in reactions.keys():
            reactionIdList.append(reactionID)

        #sort IDs by length descending
        reactionIdList.sort(cmp=self._bylength)
        reactionIdList.reverse()

        # create ODEs with reaction IDs replaced with actual reaction for convenience
        text = "\n\n"
        text += "ODE / DAE system (IDs replaced by Names):\n"
        text += "-----------------------------------------\n\n"
        self.plainTextEdit.insertPlainText(text)

        for wrappedODE in odeGenerator.wrappedODEs:
            odeID = wrappedODE.getId()
            # odeNameCount = names[odeID]
            odeMath = libsbml.formulaToString(wrappedODE.mathNode)

            for reactionID in reactionIdList:
                if reactionID in odeMath:
                    odeMath = odeMath.replace(reactionID, "(%s)" % (reactions[reactionID]))

            # 10.08.12 td: added DAE handling
            if wrappedODE.isDAE():
                for entityID in entityIdList:
                    if entityID in odeMath:
                        odeMath = odeMath.replace( entityID, "#%d#" % (names[entityID][2]) )

                for entityID in entityIdList:
                    key = "#%d#" % (names[entityID][2])
                    if key in odeMath:
                        odeMath = odeMath.replace( key, "'%s{%d}'" % (names[entityID][:2]) )

                odeText = "0  =  %s" % (odeMath)
            else:
                odeText = "d '%s{%d}' /dt  =  %s" % (names[odeID][:2] + (odeMath,))
            logging.info(odeText)
            self.plainTextEdit.insertPlainText(odeText + "\n\n")


    def _getIdToNamesMap(self, sbmlMainModel):
        namesMap = {}
        hashval = 0

        entityTypes = [sbmlMainModel.SbmlCompartments,
                       sbmlMainModel.SbmlSpecies,
                       sbmlMainModel.SbmlParameters,
                       sbmlMainModel.SbmlReactions]

        for entityType in entityTypes:
            if not entityType:
                continue
            for entity in entityType:
                ID = None
                if type(entity) == tuple:
                    entity = entity[0]
                try:
                    ID = entity.getId()
                    name = entity.Item.getName()
                except:
                    if ID:
                        name = "noname"
                        namesSoFar = [value[0] for value in namesMap.values()]
                        j = namesSoFar.count(name)
                        hashval = hashval + 1
                        namesMap[ID] = (name, j + 1, hashval)
                    logging.debug("sbmlhelpers: Problem with SBMLEntity '%s'; continuing anyway." % entity)
                    continue

                if len(name) < 1:
                    name = "noname"

                namesSoFar = [value[0] for value in namesMap.values()]
                j = namesSoFar.count(name)
                hashval = hashval + 1

                namesMap[ID] = (name, j + 1, hashval)

        return namesMap


    def _bylength(self, word1, word2):
        """
        write your own compare function:
        returns value > 0 of word1 longer then word2
        returns value = 0 if the same length
        returns value < 0 of word2 longer than word1
        """
        return len(word1) - len(word2)
