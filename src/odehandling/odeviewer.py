'''
Created on Jul 27, 2010

@author: bzfwadem
'''

#from PySide.QtCore import *
#from PySide.QtGui import *
from PySide.QtCore import Slot
from PySide.QtGui import QDialog
import libsbml

from odehandling.odegenerator import ODEGenerator
#from odehandling.Ui_ODEViewer_v2 import Ui_ODEViewer
import logging
from odehandling.Ui_ODEViewer_v2 import Ui_ODEViewer

class ODEViewer(QDialog, Ui_ODEViewer):
    '''
    
    '''
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"
    
    def __init__(self, parent, model):
        super(ODEViewer, self).__init__(parent)
        self.setupUi(self)
        self.model = model
        
        # self.plainTextEdit.setFont()
        
        self.actionGenerateODEs.trigger()



    @Slot("")
    def on_actionGenerateODEs_triggered(self):
        '''
        Open the ODE Generator information dialog.
        '''
        
        self._printODEsWithIDs()
        self._printODEsWithNames()


    def _printODEsWithIDs(self):
        '''
        Print all equations/definitions with IDs in read-only edit widget
        '''
        
        reactions = {}
        
        # for now, only try to print the results to the command line
        #text = "Overview of Reactions and ODEs\n\n"
        text=""
        text+= "Individual Rate Equations:\n"
        text+= "--------------------------\n\n"
        self.plainTextEdit.insertPlainText(text)
        
        for reactionWrapper in self.model.SbmlReactions:
            kineticLaw = reactionWrapper[0].Item.getKineticLaw() 
            id = reactionWrapper[0].Item.getId()
            if kineticLaw is not None:
                math = libsbml.formulaToString(kineticLaw.getMath())
                reactionText = "%s: %s" % (id,math)
                logging.info(reactionText)
                self.plainTextEdit.insertPlainText(reactionText + "\n")
                reactions[id] = math
            else:
                logging.error("Reaction %s has no kinetic Law." % id)
        
        text = "\n\n"
        text+= "ODEs:\n"
        text+= "-----\n\n"
        self.plainTextEdit.insertPlainText(text)
        odeGenerator = ODEGenerator(self.model)
        for wrappedODE in odeGenerator.wrappedODEs:
            odeText = "d %s /dt  =  %s" % (wrappedODE.getId(), libsbml.formulaToString(wrappedODE.mathNode))
            logging.info(odeText)
            self.plainTextEdit.insertPlainText(odeText+"\n")
            
            
        # create ODEs with reaction IDs replaced with actual reaction for convenience
        text = "\n\n"
        text+= "ODEs (reaction IDs replaced with actual equations):\n"
        text+= "---------------------------------------------------\n\n"
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
            
            odeText = "d %s /dt  =  %s" % (odeID, odeMath)
            logging.info(odeText)
            self.plainTextEdit.insertPlainText(odeText+"\n\n")




    def _printODEsWithNames(self):
        '''
        Print all equations/definitions with Names (for convenience convenience!) 
        in read-only edit widget
        '''
        
        reactions = {}
        names = self._getIdToNamesMap(self.model)
        
        # for now, only try to print the results to the command line
        #text = "Overview of Reactions and ODEs\n\n"
        text=""
        text+= "\n\n\n\n"
        text+= "   **************************************************************\n"
        text+= "   * !!!                 ODE View (by Names)                !!! *\n"
        text+= "   *                                                            *\n"
        text+= "   * Same output as above; but now unique IDs replaced by Names *\n"
        text+= "   *                                                            *\n"
        text+= "   * !!! Output may NOT be consistent with given SBML model !!! *\n"
        text+= "   **************************************************************\n"
        text+= "\n\n\n"

        dmap={}
        notxt=""
        for (ID, val) in names.items():
            if val[0]=="noname":
                notxt+="ID '%s' is unnamed / has no label.\n" % (ID)
            if dmap.has_key(val[0]):
                dmap[val[0]] += (ID, )
            else:
               dmap[val[0]]=(ID, ) 
               
        dotxt=""
        for (name, IDs) in dmap.items():
            if len(IDs) > 1:
                dotxt+="Name '%s' is used by %s.\n" % (name, IDs)
        
        if len(notxt) > 0:
            text+="*** Note: There are unnamed ID(s) ***\n\n"
            text+=notxt
            text+="\n\n"
        
        if len(dotxt) > 0:
            text+="*** Note: There are ID(s) mapping to the same Name ***\n\n"
            text+=dotxt
            text+="\n\n"
        
        text+="\n\n"
        
        entityIdList = []
        for entityID in names.keys():
            entityIdList.append(entityID)
            
        #sort IDs by length descending
        entityIdList.sort(cmp=self._bylength)
        entityIdList.reverse()
        
        text+= "Individual Rate Equations:\n"
        text+= "--------------------------\n\n"
        self.plainTextEdit.insertPlainText(text)
        
        for reactionWrapper in self.model.SbmlReactions:
            kineticLaw = reactionWrapper[0].Item.getKineticLaw() 
            id = reactionWrapper[0].Item.getId()
            # name_count = names[id]
            if kineticLaw is not None:
                math = libsbml.formulaToString(kineticLaw.getMath())
                
                for entityID in entityIdList:
                    if entityID in math:
                        math = math.replace( entityID, "'%s{%d}'" % (names[entityID]) )
                
                reactionText = "'%s{%d}': %s" % (names[id] + (math, ))
                logging.info(reactionText)
                self.plainTextEdit.insertPlainText(reactionText + "\n")
                reactions[id] = math
            else:
                logging.error("Reaction '%s{%d}' has no kinetic Law." % (names[id]))
        
        # text = "\n\nODEs:\n\n"
        # self.plainTextEdit.insertPlainText(text)
        odeGenerator = ODEGenerator(self.model)
        # for wrappedODE in odeGenerator.wrappedODEs:
        #     odeText = "%s: %s" %(wrappedODE.getName(),libsbml.formulaToString(wrappedODE.mathNode) + "\n")
        #     logging.info(odeText)
        #     self.plainTextEdit.insertPlainText(odeText)
        
        reactionIdList = []
        for reactionID in reactions.keys():
            reactionIdList.append(reactionID)

        #sort IDs by length descending
        reactionIdList.sort(cmp=self._bylength)
        reactionIdList.reverse()
            
        # create ODEs with reaction IDs replaced with actual reaction for convenience
        text = "\n\n"
        text+= "ODEs (IDs replaced by Names):\n"
        text+= "-----------------------------\n\n"
        self.plainTextEdit.insertPlainText(text)
        
        for wrappedODE in odeGenerator.wrappedODEs:
            odeID = wrappedODE.getId()
            # odeNameCount = names[odeID]
            odeMath = libsbml.formulaToString(wrappedODE.mathNode)

            for reactionID in reactionIdList:
                if reactionID in odeMath:
                    odeMath = odeMath.replace( reactionID, "(%s)" % (reactions[reactionID]) )
            
            odeText = "d '%s{%d}' /dt  =  %s" % (names[odeID] + (odeMath,))
            logging.info(odeText)
            self.plainTextEdit.insertPlainText(odeText+"\n\n")


    def _getIdToNamesMap(self, sbmlMainModel):
        
        map = {}
        
        entityTypes = [sbmlMainModel.SbmlSpecies, 
                       # sbmlMainModel.SbmlCompartments, 
                       sbmlMainModel.SbmlParameters, 
                       sbmlMainModel.SbmlReactions]
                       
        for entityType in entityTypes:
            if not entityType:
                continue
            for entity in entityType:
                id = None
                if type(entity)==tuple:
                    entity = entity[0]
                try:
                    id = entity.getId()
                    name = entity.Item.getName()
                except:
                    if id:
                        name = "noname"
                        namesSoFar = [value[0] for value in map.values()]
                        j = namesSoFar.count(name)
                        map[id] = (name, j+1)
                    logging.debug("sbmlhelpers: Problem with SBMLEntity '%s'; continuing anyway." % entity)
                    continue
                
                if len(name) < 1:
                    name = "noname"
                
                namesSoFar = [value[0] for value in map.values()]
                j = namesSoFar.count(name)
                
                map[id] = (name, j+1)
        
        return map
        

    def _bylength(self, word1, word2):
        """
        write your own compare function:
        returns value > 0 of word1 longer then word2
        returns value = 0 if the same length
        returns value < 0 of word2 longer than word1
        """
        return len(word1) - len(word2)
