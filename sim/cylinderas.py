from abqimport import *
from sim.simclass import CylinderAs
import time
import cPickle

def init(overwrite=True):
    radii = np.array([17.5e-3])
    Gs = np.array([28.2e3, 56.9e3])
    heights = np.array((35e-3))
    cylinderAsList = []
    for radius in radii:
        for G in Gs:
            for height in heights:
                cylinderAsList.append(CylinderAs(radius=radius, G=G, height=height, overwrite=overwrite))
    with open('./sim/pickles/cylinderAsList.pkl', 'w+') as f:
        cPickle.dump(cylinderAsList, f)
    return cylinderAsList


def run(cylinderAsList):
    for cylinderAs in cylinderAsList:
        cylinderAs.runModel()
    time.sleep(5)
    for cylinderAs in cylinderAsList:
        cylinderAs.transferOdb()
        cylinderAs.deleteModel()
        cylinderAs.deleteJob()
    return


def analyze(cylinderAsList, keepOdb=True):
    for cylinderAs in cylinderAsList:
        cylinderAs.extractModelOutputs()
        if not keepOdb:
            cylinderAs.deleteOdb()
    return


def unittest(radius=17.5e-3, G=28.2e3, height=35e-3, fakeRun=False):
    cylinderAs = CylinderAs(radius=radius, G=G, height=height)
    if not fakeRun:
        cylinderAs.runModel()
        time.sleep(5)
        cylinderAs.transferOdb()
        cylinderAs.deleteModel()
        cylinderAs.deleteJob()
    cylinderAs.extractModelOutputs()
    return cylinderAs