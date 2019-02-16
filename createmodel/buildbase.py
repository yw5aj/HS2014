from abqimport import *
import setps
import setas

def buildBase(baseModelName='both'):
    """
    Build the plane strain model / axisymmetric model / both models, and 
    delete the original Model-1 or Model-2 etc.
    
    Parameters
    ----------
    baseModelName : str
        Name of the base model, either 'ps' or 'as', or 'both'.
    """
    if baseModelName == 'ps':
        setps.main()
    elif baseModelName=='as':
        setas.main()
    elif baseModelName=='both':
        setps.main()
        setas.main()
    for modelName in mdb.models.keys():
        if modelName.startswith('Model-'):
            del mdb.models[modelName]
    return
