from abqimport import *
import setpe
import setas
from getgeom import XCALIB, XHAUSER

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
        setpe.setpe(xcontact=XCALIB)
    elif baseModelName=='as':
        setas.setas(xcontact=XHAUSER)
    elif baseModelName=='both':
        setpe.setpe(xcontact=XCALIB)
        setas.setas(xcontact=XHAUSER)
    for modelName in mdb.models.keys():
        if modelName.startswith('Model-'):
            del mdb.models[modelName]
    return
