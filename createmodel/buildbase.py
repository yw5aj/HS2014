from abqimport import *
import setpe
import setas

def buildBase(baseModelName='both'):
    """
    Build the plane strain model / axisymmetric model / both models, and 
    delete the original Model-1 or Model-2 etc.
    
    Parameters
    ----------
    baseModelName : str
        Name of the base model, either 'pe' or 'as', or 'both'.
    """
    if baseModelName == 'pe':
        setpe.main()
    elif baseModelName=='as':
        setas.main()
    elif baseModelName=='both':
        setpe.main()
        setas.main()
    for modelName in mdb.models.keys():
        if modelName.startswith('Model-'):
            del mdb.models[modelName]
    return
