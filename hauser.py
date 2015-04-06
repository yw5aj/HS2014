import os
if not os.getcwd().endswith('hs2014'):
    os.chdir('hs2014')

import sim.cylinderas, sim.sphereas
from readodb.odbtools import getWholeModelOutput

# Model already done
inputDictTest = {
    'cylinder': (
        (24.39e3, 17.5e-3, 10e-3), ),
    'sphere': (
        (24.39e3, 17.5e-3, 10e-3), )}
inputDict0306 = {
    'cylinder': (
        (28.2e3, 17.5e-3, 35e-3),
        (56.9e3, 17.5e-3, 35e-3),
        (28.2e3, 2e-3, 35e-3),
        (56.9e3, 2e-3, 35e-3),
        (5e3, 17.5e-3, 35e-3),
        (100e3, 17.5e-3, 35e-3)),
    'sphere': (
        (28.2e3, 5e-3),
        (56.9e3, 5e-3),
        (28.2e3, 10e-3),
        (56.9e3, 10e-3))}
inputDict0308 = {
    'cylinder': (
        (10e3, 17.5e-3, 35e-3),
        (15e3, 17.5e-3, 35e-3),
        (20e3, 17.5e-3, 35e-3),
        (200e3, 17.5e-3, 35e-3),
        (1e8, 17.5e-3, 35e-3),
        (100e3, 10e-3, 35e-3),
        (200e3, 10e-3, 35e-3),
        (1e8, 10e-3, 35e-3)),
    'sphere': (
        (100e3, 2e-3),
        (200e3, 2e-3),
        (1e8, 2e-3),
        (100e3, 5e-3),
        (200e3, 5e-3),
        (1e8, 5e-3))}
inputDict0326 = {
    'cylinder': (
        (24.39e3, 17.5e-3, 10e-3),
        (35.65e3, 17.5e-3, 10e-3),
        (12.185e3, 17.5e-3, 10e-3),
        (17.825e3, 17.5e-3, 10e-3),
        (18.2925e3, 17.5e-3, 10e-3),
        (26.7375e3, 17.5e-3, 10e-3),)}        
        

def runModels(inputDict, fakeRun=False):
    modelNameList = []
    for type, tuples in inputDict.iteritems():
        for G, radius, height in tuples:
            if type == 'cylinder':
                model = sim.cylinderas.unittest(G=G, radius=radius, height=height, fakeRun=fakeRun)
            elif type == 'sphere':
                model = sim.sphereas.unittest(G=G, radius=radius, fakeRun=fakeRun)
            modelNameList.append(model.modelName)
    return modelNameList

def readModels(modelNameList):
    for modelName in modelNameList:
        getWholeModelOutput(modelName)


if __name__ == '__main__':
    modelNameList = runModels(inputDictTest, fakeRun=True)
    # readModels(modelNameList)

