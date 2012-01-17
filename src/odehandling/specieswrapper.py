import logging

class SpeciesWrapper(object):
    """
    A simple wrapper to handle libSBML Species
    objects for use in computation backends.
    """


    def __init__(self, speciesEntity, index):
        """
        Just gets some infos from the given libSBML
        Species object.
        """
        if speciesEntity is None:
            error = "Tried to create a wrapper Species object without supplying a libSBML Species."
            logging.error(error)
            return

        self.wrappedSpecies = speciesEntity.Item
        self.wrappedEntity = speciesEntity
        self.id = self.wrappedSpecies.getId()
        self.index = index
        
        self.initialValue = self.getInitialValue()
        
        
    def getInitialValue(self):
        if self.wrappedSpecies.isSetInitialAmount():
            return self.wrappedSpecies.getInitialAmount()
        elif self.wrappedSpecies.isSetInitialConcentration():
            return self.wrappedSpecies.getInitialConcentration()
        else:
            logging.warning("Encountered Species with neither Initial Amount nor Concentration: %s" % self.getId())
            return None
        

    def getId(self):
        return self.wrappedEntity.getId()

    def getThreshold(self):
        return self.wrappedEntity.getThreshold()