from abqimport import *
from sim.simclass import SphereAs
import time
import cPickle

def init(overwrite=True):
    # radii = np.arange(2e-3, 11e-3, 1e-3)
    # Gs = np.arange(1e4, 10e4, 1e4)
    radii = np.arange(4e-3, 10e-3, 2e-3)
    Gs = np.arange(1e4, 10e4, 4e4)
    sphereAsList = []
    for radius in radii:
        for G in Gs:
            sphereAsList.append(SphereAs(radius=radius, G=G, overwrite=overwrite))
    with open('./sim/pickles/sphereAsList.pkl', 'w+') as f:
        cPickle.dump(sphereAsList, f)
    return sphereAsList


def run(sphereAsList):
    for sphereAs in sphereAsList:
        sphereAs.runModel()
    time.sleep(5)
    for sphereAs in sphereAsList:
        sphereAs.transferOdb()
        sphereAs.deleteModel()
        sphereAs.deleteJob()
    return


def analyze(sphereAsList, keepOdb=True):
    for sphereAs in sphereAsList:
        sphereAs.extractModelOutputs()
        if not keepOdb:
            sphereAs.deleteOdb()
    return


def unittest(radius=5e-3, G=1e4, fakeRun=False):
    sphereAs = SphereAs(radius=radius, G=G)
    if not fakeRun:
        sphereAs.runModel()
        time.sleep(5)
        sphereAs.transferOdb()
        sphereAs.deleteModel()
        sphereAs.deleteJob()
    sphereAs.extractModelOutputs()
    return sphereAs