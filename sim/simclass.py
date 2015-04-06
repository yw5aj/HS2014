from abqimport import *
from commontools import (runModels, deleteJob, transferOdb, submitJob, 
    deleteModel)
from createmodel import setas, setpe
from readodb.odbtools import (getSurfaceCoordinates, getSurfaceDeflection,
    getTipForceDisp, getMcncNodeDistribution, getTimePts, getMcncNodeCoordinates,
    openOdb_ )
from createmodel.softtip import buildAsSphere, buildAsCylinder
from createmodel.setbar import buildBar
import inspect
import cPickle
import os
import time


class BaseSimClass:
    
    def __init__(self, baseModelName):
        self.baseModelName = baseModelName
        if baseModelName == 'pe':
            setpe.setpe()
        elif baseModelName == 'as':
            setas.setas()
        for key in mdb.models.keys():
            if key.startswith('Model-'):
                del mdb.models[key]
        return
    
    def runModel(self):
        if self.overwrite or not self.exists():
            self.submitJob()
            self.waitForCompletion()
        return
    
    def getOdb(self):
        self.odb = openOdb_(self.jobName)
        return self.odb
    
    def getSurfaceCoordinates(self):
        self.surfaceCoordinates = getSurfaceCoordinates(self.jobName)
        return self.surfaceCoordinates
    
    def getSurfaceDeflection(self):
        self.surfaceDeflection = getSurfaceDeflection(self.jobName)
        return self.surfaceDeflection
    
    def getTipForceDisp(self):
        self.tipForceDisp = getTipForceDisp(self.jobName)
        return self.tipForceDisp
    
    def getMcncNodeDistribution(self):
        outputQuantities = ['stressMinPrincipal', 'stressVertical', 
            'stressVonMises', 'strainMinPrincipal', 'strainVertical', 
            'sener']
        self.mcncNodeDict = {}
        for quantity in outputQuantities:
            self.mcncNodeDict[quantity] = getMcncNodeDistribution(self.jobName, quantity)
        return self.mcncNodeDict
    
    def getTimePts(self):
        self.timePts = getTimePts(self.jobName)
        return self.timePts
    
    def getMcncNodeCoordinates(self):
        self.mcncNodeCoordinates = getMcncNodeCoordinates(self.jobName)
        return self.mcncNodeCoordinates
    
    def extractModelOutputs(self, toFile=True):
        try:
            self.getMcncNodeCoordinates()
            self.getMcncNodeDistribution()
            self.getTimePts()
            self.getSurfaceCoordinates()
            self.getSurfaceDeflection()
            self.getTipForceDisp()

            for attr in ['timePts', 'mcncNodeCoordinates', 'mcncNodeDict', 
                'tipForceDisp', 'surfaceCoordinates', 'surfaceDeflection']:
                if toFile:
                    filePath = './pickles/'+self.jobName+'/'+attr+'.pkl'
                    dirPath = os.path.dirname(filePath)
                    if not os.path.isdir(dirPath):
                        os.makedirs(dirPath)
                    with open(filePath, 'w+') as f:
                        cPickle.dump(getattr(self, attr), f)
        except (visualization.OdbError, IndexError):
            pass
        return
    
    def deleteOdb(self):
        try:
            os.remove('./odbs/'+self.jobName+'.odb')
        except WindowsError:
            pass
        return
    
    def waitForCompletion(self):
        mdb.jobs[self.jobName].waitForCompletion()
    
    def transferOdb(self):
        transferOdb(self.jobName)
        return
    
    def submitJob(self):
        submitJob(self.modelName, self.jobName)
        return
    
    def deleteJob(self):
        deleteJob(self.jobName)
        return
    
    def deleteModel(self):
        deleteModel(self.modelName)
    
    def exists(self):
        return os.path.exists('./odbs/'+self.jobName)
        




class SphereAs(BaseSimClass):
    
    def __init__(self, radius, G, overwrite=True):
        """
        Parameters
        ----------
        radius, G : float
            The model parameters.
        overwrite : bool
            Flag to control overwriting.
        """
        # Initialize model parameters
        BaseSimClass.__init__(self, 'as')
        self.radius = radius
        self.G = G
        self.modelName = buildAsSphere(self.radius, self.G)
        self.jobName = self.modelName
        self.overwrite = overwrite
        return
    

class BarPe(BaseSimClass):
    
    def __init__(self, width, overwrite=True):
        # Initialize model parameters
        BaseSimClass.__init__(self, 'pe')
        self.width = width
        self.modelName = buildBar(width=3e-3, baseModelName='pe')
        self.jobName = self.modelName
        self.overwrite = overwrite
        return
    

class CylinderAs(BaseSimClass):
    
    def __init__(self, radius, G, height, overwrite=True):
        """
        Parameters
        ----------
        radius, G : float
            The model parameters.
        overwrite : bool
            Flag to control overwriting.
        """
        # Initialize model parameters
        BaseSimClass.__init__(self, 'as')
        self.radius = radius
        self.G = G
        self.height = height
        self.modelName = buildAsCylinder(self.radius, self.G, self.height)
        self.jobName = self.modelName
        self.overwrite = overwrite
        return
        