import re

def getSphereModelNameFromRadiusAndG(radius, G):
    GStr = ('%.3e'%G).replace('.','').replace('+','')
    radiusStr = str(int(radius * 1e5))
    modelName = 'as_g'+GStr+'_r'+radiusStr+'_stip'
    return modelName


def getCylinderModelNameFromRGH(radius, G, height):
    """
    Height is integer mm, but in SI unit.
    """
    GStr = ('%.3e'%G).replace('.','').replace('+','')
    radiusStr = str(int(radius * 1e5))
    heightStr = str(int(height * 1e3))
    modelName = 'ac_g%s_r%s_h%s_stip' % (GStr, radiusStr, heightStr)
    return modelName


def getRadiusFromModelName(modelName):
    radius = int(re.findall(r'\d+', modelName)[2]) * 1e-5
    return radius


def getGFromModelName(modelName):
    intStrs = re.findall(r'\d+', modelName)
    G = float(intStrs[0]+'e'+intStrs[1]) * 1e-3
    return G


def getHeightFromModelName(modelName):
    height = int(re.findall(r'\d+', modelName)[3]) * 1e-3
    return height


def getTipNamesFromModelName(modelName):
    tipBaseName = modelName+'_base'
    tipTipName = modelName+'_tip'
    return (tipBaseName, tipTipName)


def getJimModelName(softLevel=0, noduleSize=0, noduleDepth=0):
    """
    Get the model name for Jim's experiment data.
    
    Parameters
    ----------
    softLevel : {0, 1}
        0 for H10, 1 for H30.
    noduleSize : {0, 1, 2}
        0 is xxx, 1 is yyy.
    noduleDepth : {0, 1, 2}
        0 is xxx, 1 is yyy.
    """
    modelName = 'as' + str(softLevel) + str(noduleSize) + str(noduleDepth)
    return modelName


def getJimPropertiesFromModelName(modelName):
    """
    return the property tuple for Jim's experiment tip.
    
    Returns
    -------
    G : float
        The G for substrate.
    noduleRadius : float
        Radius of the hard nodule.
    noduleDepth : float
        Depth of the hard nodule.
    """
    
    return properties