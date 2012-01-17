
import logging

class CompartmentWrapper(object):
    """
    Simple wrapper for a libSBML Compartment. It enables easy use
    in computation backends.

    @param compartment: A libSBML Compartment object
    @type compartment: libSBML Compartment

    @since: 2010-08-06
    """
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, compartment, index):
        """
        Just gets some infos from the given libSBML
        Compartment object.
        """
        if compartment is None:
            error = "Tried to create a wrapper Compartment object without supplying a libSBML Compartment."
            logging.error(error)
            return

        self.wrappedCompartment = compartment
        self.id = self.wrappedCompartment.getId()
        self.size = self.wrappedCompartment.getSize()
        self.index = index

    def getId(self):
        return self.id

    def getSize(self):
        return self.size