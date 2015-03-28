# -*- coding: utf-8 -*-

from abqimport import *
from commontools import (deleteJob, submitJob, getR2, writeLine, 
                         plotInCae, transferOdb)
from createmodel.createtools import setNH
from readodb.odbtools import getTipForceDisp
from createmodel import setfit
import numpy as np
from scipy.optimize import minimize
from scipy import interpolate
from constants import GListFromDeflection


def main():
    return


def autoOptimize():
    setfit.buildAll()
    for sub_n in range(1, 5):
        k0 = 2.5
        bnds = ((0., np.inf), ) 
        res = minimize(mat2r2magnitude_k, k0, method='l-bfgs-b', 
                       args=(sub_n, -1.), bounds=bnds, options={'disp':True, 
                       'eps':1e-3}, tol=1e-3)
        print(res)
        to_write = ['Sub #'+str(sub_n), res.x[0], res.fun]
        writeLine('./fitmodel/csv/r2/frc_sub'+str(sub_n)+'.csv', to_write)
    return


def mat2r2magnitude_k(k, sub_n, sign=1., save_data=False):
    """
    A simple wrapper to provide only one input argument for optimization.
    
    Parameters
    ----------
    k : float
        The scale constant for the materials.
    """
    GList = k * (GListFromDeflection)
    r2List = mat2r2magnitude(GList, sub_n, sign=sign, save_data=save_data)
    r2 = r2List.mean()
    print(k, r2List)
    return r2


def mat2r2magnitude(GList, sub_n, sign=1., save_data=False):
    """
    Run the model with given material Parameters, compare model with 
    experiment displacement-force trace, save both traces and return
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
    modelNameList = ['as_rigid_plate_tip', 'as_rigid_d635_tip']
    jobNameList = []
    for modelName in modelNameList:
        jobName = modelName
        setNH('epidermis', modelName, GList[0])
        setNH('dermis', modelName, GList[1])
        setNH('hypodermis', modelName, GList[2])
        # Submit job
        jobName = deleteJob(jobName)
        submitJob(modelName, jobName)
        jobNameList.append(jobName)
    for jobName in jobNameList:
        mdb.jobs[jobName].waitForCompletion()
        transferOdb(jobName)
    # Extract R-square value and plot the traces
    r2 = []
    for i, jobName in enumerate(jobNameList):
        if str(mdb.jobs[jobName].messages[-1].type) == 'JOB_COMPLETED':
            expFileName = './fitmodel/csv/experiment/frc_disp_sub'+str(sub_n)+'.csv'
            # Read different data depending on job name
            if 'd635' in jobName:
                expData = np.genfromtxt(expFileName, delimiter=',')[:7]
            elif 'plate' in jobName:
                expData = np.genfromtxt(expFileName, delimiter=',')[7:]
            modelData = getTipForceDisp(jobName)
            r2.append(getR2(expData, modelData))
            filePath = './fig/' + modelNameList[i] + '/' + str(sub_n)
            plotInCae(expData, modelData, save_data=save_data, filePath=filePath)
        else:
            r2.append(-np.nan)
            # Delete the job and associated files
            deleteJob(jobName)
    r2 = np.array(r2)
    r2signed = r2 * sign
    return r2signed


if __name__ == "__main__":
    main()
