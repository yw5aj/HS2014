import numpy as np
from analysisclass import SphereAs
import cPickle
import os
from createmodel.softtipnaming import getSphereModelNameFromRadiusAndG

def init(radii, Gs):
    modelNames = []
    for radius in radii:
        for G in Gs:
            modelNames.append(getSphereModelNameFromRadiusAndG(radius, G))
    sphereAsList = []
    for modelName in modelNames:
        sphereAs = SphereAs(jobName=modelName)
        sphereAs.row = np.isclose(radii, sphereAs.radius).nonzero()[0][0]
        sphereAs.col = np.isclose(Gs, sphereAs.G).nonzero()[0][0]
        sphereAsList.append(sphereAs)
    with open('./pickles/sphereAsList.pkl', 'w+') as f:
        cPickle.dump(sphereAsList, f)
    return sphereAsList