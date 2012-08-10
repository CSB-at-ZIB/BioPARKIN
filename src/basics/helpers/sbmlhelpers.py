"""
Created on Jun 7, 2010

@author: Moritz Wade
"""
import logging

def findSbmlEntity(id, sbmlMainModel):
    """
    Tries to find a SBML entity given a SBMLMainModel
    and an ID.

    @param id: ID to search for
    @type id: str

    @param sbmlMainModel: A BioParkin SBMLMainModel
    @type sbmlMainModel: SBMLMainModel

    @since: 2010-06-07
    """
    
    entityTypes = [sbmlMainModel.SbmlSpecies,
                 sbmlMainModel.SbmlCompartments,
                 sbmlMainModel.SbmlReactions,
                 sbmlMainModel.SbmlParameters,
                 # sbmlMainModel.SbmlAlgebraicRules,  #  09.08.12 td: SbmlAlgebraicRules do not have an ID at all...
                 sbmlMainModel.SbmlAssignmentRules,
                 sbmlMainModel.SbmlRateRules,
                 sbmlMainModel.SbmlEvents]
    
    for type in entityTypes:
        if not type:
            continue
        for entity in type:
            try:
                if id == entity.getId():
                    return entity
            except:
                pass

    logging.debug("sbmlhelpers: Can't get SBMLEntity with ID %s." % id)
     
    return None
