import numpy as np


def _getGListFromDeflectionFit(deflectionFitResult):
    hypodermisG = 1e3
    dermisG = hypodermisG * 10**deflectionFitResult[0]
    epidermisG = dermisG * 10**deflectionFitResult[1]
    GList = [epidermisG, dermisG, hypodermisG]
    return GList


def _getGArrayFromMagnitudeFit(GListFromDeflection, _magnitudeFitResult):
    GListAll = []
    for k in _magnitudeFitResult:
        GListAll.append(np.array(GListFromDeflection) * k)
    GArrayAll = np.array(GListAll)
    GArrayAverage = GArrayAll.mean(axis=0)
    return (GArrayAll, GArrayAverage)



# Define material properties used for fitting magnitude, from deflection fit
_deflectionFitResult = [1.32972973, 1.378378378]
GListFromDeflection = _getGListFromDeflectionFit(_deflectionFitResult)

# Define the material property from fitting after magnitude fit (and also 
#    deflection fit before that)
_magnitudeFitResult = [3.404559926, 1.620008475, 2.572149122, 1.894603893]
GArrayAll, GArrayAverage = _getGArrayFromMagnitudeFit(GListFromDeflection,
                                                      _magnitudeFitResult)