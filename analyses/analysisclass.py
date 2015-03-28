import cPickle
import numpy as np
import matplotlib.pyplot as plt
import os
from createmodel.softtipnaming import (getSphereModelNameFromRadiusAndG, 
    getGFromModelName, getRadiusFromModelName)
from createmodel.bartipnaming import (getModelNameFromBaseAndBarWidth, 
    getBarWidthFromModelName)
from scipy.optimize import curve_fit


class BaseAnalysisClass():
    
    def __init__(self):
        self.dirpath = './pickles/'+self.jobName+'/'
        output_attr = []
        for filename in os.listdir(self.dirpath):
            if filename.endswith('.pkl'):
                filepath = self.dirpath + filename
                attrname = filename.replace('.pkl', '')
                with open(filepath, 'r') as f:
                    data = cPickle.load(f)
                setattr(self, attrname, data)
        self.step_n = self.timePts.size
        self.surface_node_n = self.surfaceCoordinates.shape[0]
        self.mcnc_node_n = self.mcncNodeCoordinates.shape[0]
        self.getMaxStepTime()
        self.getDeflectedSurfaceCoordinates()
        self.getSmoothedMcncNodeDict()
        return
    
    def getSmoothedMcncNodeDict(self):
        self.smoothedMcncNodeDict = {}
        def expDecay(x, k, l):
            return k * np.exp(-x / l)
        xdata = self.mcncNodeCoordinates[:, 0]
        for key, value in self.mcncNodeDict.iteritems():
            self.smoothedMcncNodeDict[key] = np.zeros_like(value)
            for col in range(value.shape[1]):
                ydata = self.mcncNodeDict[key][:, col]
                p0 = (ydata.max(), xdata.mean()/5)
                popt = curve_fit(expDecay, xdata, ydata, p0)[0]
                self.smoothedMcncNodeDict[key][:, col] = expDecay(xdata, *popt)
        return self.smoothedMcncNodeDict
    
    def getMaxStepTime(self):
        self.maxStepTime = self.timePts[-1]
        return self.maxStepTime
    
    def getDeflectedSurfaceCoordinates(self):
        self.deflectedSurfaceCoordinates = np.tile(self.surfaceCoordinates[:, 
            1], self.step_n).reshape([self.step_n, self.surface_node_n]).T + \
            self.surfaceDeflection
    
    def plotData(self, coordinates, data, axes=None, spec='-'):
        if not axes:
            fig, axes = plt.subplots(1, 1)
        patches = np.array(range(self.step_n-1), dtype=object)
        color_list = np.linspace(1, 0, self.step_n)
        for col in range(1, self.step_n):
            color = color_list[col]
            label = 'Force load = '+'%.3f'%self.timePts[col]+' N'
            patches[col-1] = axes.plot(coordinates[:, 0], data[:, col], spec, 
                color=str(color), label=label)[0]
        return axes, patches
    

class SphereAs(BaseAnalysisClass):
    
    def __init__(self, **kwargs):
        if 'radius' in kwargs and 'G' in kwargs:
            self.radius = kwargs['radius']
            self.G = kwargs['G']
            self.modelName = getSphereModelNameFromRadiusAndG(self.radius, self.G)
            self.jobName = self.modelName
        elif 'jobName' in kwargs:
            self.jobName = kwargs['jobName']
            self.modelName = self.jobName
            self.radius = getRadiusFromModelName(self.modelName)
            self.G = getGFromModelName(self.modelName)
        BaseAnalysisClass.__init__(self)
        return


class BarPe(BaseAnalysisClass):
    
    def __init__(self, **kwargs):
        if 'width' in kwargs:
            self.width = kwargs['width']
            self.modelName = getModelNameFromBaseAndBarWidth(width=self.width,
                baseModelName='pe')
            self.jobName = self.modelName
        elif 'jobName' in kwargs:
            self.jobName = kwargs['jobName']
            self.modelName = self.jobName
            self.barWidth = getBarWidthFromModelName(self.modelName)
        BaseAnalysisClass.__init__(self)
        return
        