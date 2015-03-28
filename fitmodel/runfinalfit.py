from abqimport import *
from constants import GListFromDeflection, GArrayAll
import magnitude
import deflection
from createmodel import setfit

def runMagnitudeFit():
    setfit.buildAll()
    for sub_n in range(1, 5):
        GList = GArrayAll[sub_n-1]
        magnitude.mat2r2magnitude(GList, sub_n, save_data=True)
    return


def runDeflectionFit():
    setfit.buildAll()
    GList = GListFromDeflection
    deflection.mat2r2deflection(GList, 'pe_rigid_d317_tip', save_data=True)
    deflection.mat2r2deflection(GList, 'pe_rigid_d952_tip', save_data=True)
    return
    
    