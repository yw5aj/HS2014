# -*- coding: utf-8 -*-

from abqimport import *

import numpy as np
from scipy.optimize import minimize

from commontools import (deleteJob, submitJob, getR2, plotInCae, writeLine, 
    transferOdb)
from readodb.odbtools import getSurfaceCoordinates, getSurfaceDeflection
from createmodel.createtools import setNH
import time


def exhaust(modelName, run_nan=False):
    filePath = './fitmodel/csv/r2/r2table_'+modelName+'.csv'
    inputList = []
    for i in np.nditer(np.arange(0, 2.1, 0.2)):
        for j in np.nditer(np.arange(1, 3.1, 0.2)):
            inputList.append(np.array((i, j)))
    new_i, nan_list = readExistingResult(filePath)
    for i, input in enumerate(inputList):
        if i >= new_i:
            line = [input[0], input[1], mat2avgR2deflectionLog10ratios(input, modelName)]
            writeLine(filePath, line)
    if run_nan:
        for input in nan_list:
            line = [input[0], input[1], mat2avgR2deflectionLog10ratios(input, modelName)]
            writeLine(filePath, line)
    return


def readExistingResult(filePath):
    try:
        data = np.genfromtxt(filePath, delimiter=',')
        new_i = data.shape[0]
        nan_idx = np.where(np.isnan(data[:, 2]))[0]
        nan_list = data[:, :2][nan_idx]
    except IOError:
        new_i, nan_list = 0, []
    return (new_i, nan_list)


def autoOptimize():
    """
    This function is obsolete. DO NOT USE BEFORE MODIFYING.
    """
    x0 = [2.1, 1.4]
    cons = ({'type': 'ineq', 'fun' : lambda x: x[0] - x[1]},
            )
    bnds = ((3, 10), (3, 10))
    res = minimize(mat2avgR2deflectionLog10ratios, x0, method='l-bfgs-b', 
        args=(-1.,),constraints=cons, bounds=bnds, 
        options={'disp':True, 'eps':.2}, tol=1e-2
        )
    print(res)
    return res


def mat2avgR2deflectionLog10ratios(GListLog10ratios, modelName, sign=1.):
    """
    A simple wrapper to return one scaler value for optimization.
    
    Parameters
    ----------
    GListLog10 : array_like
        GList will be np.power(10., [GListLog10[0], GListLog10[1], 3.])
    """
    hypoG = 10**3.
    dermG = hypoG * 10.**GListLog10ratios[0]
    epiG = dermG * 10.**GListLog10ratios[1]
    GList = (epiG, dermG, hypoG)
    avgR2 = np.average(mat2r2deflection(GList, modelName, sign=sign))
    print(GListLog10ratios, avgR2)
    return avgR2


def mat2r2deflection(GList, modelName, sign=1., save_data=False):
    """
    Run the model with given material Parameters, compare model with 
    experiment skin surface deflections, save deflections data and return
    the R-square value.
    
    Parameters
    ----------
    GList : array_like
        Usually GList is a list containing the G for epidermis, dermis and 
        hypodermis layer.
    sign : float
        It is a sign used for optimization purpose. Set sign = -1. can turn
        this maximization problem into minimization problem easily.
    save_data : bool, optional
        If True, the fit will be plotted and saved to filePath appending
        .csv and .png in fig/ folder.
        
    Returns
    -------
    r2signed : ndarray
        The R-squared values multiplied by the sign multiplier.
    """
    # Modify the model
    jobName = modelName
    setNH('epidermis', modelName, GList[0])
    setNH('dermis', modelName, GList[1])
    setNH('hypodermis', modelName, GList[2])
    # Submit job and wait for completion
    jobName = deleteJob(jobName) # to clean old files
    submitJob(modelName, jobName)
    mdb.jobs[jobName].waitForCompletion()
    transferOdb(jobName)
    # Extract R-square values and plot the deflections
    timePts, = zip(*mdb.models[modelName].timePoints['timePts'].points)
    timePts = np.array(timePts)
    r2 = np.zeros(timePts.size)
    if str(mdb.jobs[jobName].messages[-1].type) == 'JOB_COMPLETED':
        expFileName = ['./fitmodel/csv/experiment/exp'+modelName[-7:-4]+'_'+ 
            str(i+1)+'.csv' for i in range(timePts.size)]
        surfaceCoordinates = getSurfaceCoordinates(jobName)
        surfaceDeflection = getSurfaceDeflection(jobName)
        for i in range(timePts.size):
            modelData = np.column_stack((surfaceCoordinates[:, 0], surfaceDeflection[:, i+1]))
            expData = np.genfromtxt(expFileName[i],delimiter=',') * 1e-3
            r2[i] = getR2(expData, modelData)
            filePath = './fig/' + modelName + '/' + str(i+1)
            plotInCae(expData, modelData, save_data=save_data, filePath=filePath)
    else:
        r2 = -np.nan * np.ones(timePts.size)
    # Delete the job and associated files
    deleteJob(jobName)
    r2signed = r2 * sign
    return r2signed


if __name__ == "__main__":
    pass
