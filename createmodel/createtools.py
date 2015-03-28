from abqimport import *
import numpy as np


def setInteraction(modelName, tipName):
    a = mdb.models[modelName].rootAssembly
    region1=a.instances[tipName].surfaces['tip_contact_surface']
    region2=a.instances['finger'].surfaces['finger_surface_nail']
    mdb.models[modelName].SurfaceToSurfaceContactStd(name='tip2skin', 
        createStepName='Initial', master=region1, slave=region2, 
        sliding=FINITE, enforcement=NODE_TO_SURFACE, thickness=OFF, 
        interactionProperty='tip2skin', surfaceSmoothing=NONE, 
        adjustMethod=NONE, smooth=0.2, initialClearance=OMIT, datumAxis=None, 
        clearanceRegion=None)
    return


def setStep(modelName, timePts, dummyTimePeriod=1e-2):
    # Set dummy step (step to make contact)
    mdb.models[modelName].StaticStep(name='Dummy', previous='Initial', 
        timePeriod=dummyTimePeriod, initialInc=dummyTimePeriod, 
        minInc=dummyTimePeriod*1e-05, maxInc=dummyTimePeriod, nlgeom=ON)
    # Set actual load step
    totalTime = timePts[-1]
    mdb.models[modelName].StaticStep(name='Ramp', previous='Dummy', 
        timePeriod=totalTime, initialInc=totalTime, minInc=totalTime*1e-05, 
        maxInc=totalTime, nlgeom=ON)
    # Time points shifted by dummyTimePeriod, but set 0th to be 0
    points = [[timePts[i],] for i in range(len(timePts))]
    mdb.models[modelName].TimePoint(name='timePts', points=points)
    mdb.models[modelName].fieldOutputRequests['F-Output-1'].setValues(
        timePoint='timePts', variables=('S', 'PE', 'PEEQ', 'PEMAG', 'LE', 
        'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 'ENER'))
    return


def setDispLoad(modelName, tipName, magnitude):
    a = mdb.models[modelName].rootAssembly
    r1 = a.instances[tipName].referencePoints
    p = mdb.models[modelName].parts[tipName]
    refPointNo = p.referencePoints.keys()[0]
    refPoints1=(r1[refPointNo], )
    region = a.Set(referencePoints=refPoints1, name='Set-2')
    mdb.models[modelName].DisplacementBC(name='load', createStepName='Ramp', 
        region=region, u1=UNSET, u2=magnitude, ur3=UNSET, amplitude=UNSET, 
        fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
    mdb.models[modelName].DisplacementBC(name='vertical_indenter', 
        createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, 
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    return


def setForceLoad(modelName, tipName, magnitude, dummyMagnitude=1e-5):
    setDummyLoad(modelName, tipName, magnitude=dummyMagnitude)
    a = mdb.models[modelName].rootAssembly
    r1 = a.instances[tipName].referencePoints
    p = mdb.models[modelName].parts[tipName]
    refPointNo = p.referencePoints.keys()[0]
    refPoints1=(r1[refPointNo], )
    region = a.Set(referencePoints=refPoints1, name='Set-2')
    mdb.models[modelName].ConcentratedForce(name='load', 
        createStepName='Ramp', region=region, cf2=magnitude, 
        distributionType=UNIFORM, field='', localCsys=None)
    mdb.models[modelName].DisplacementBC(name='vertical_indenter', 
        createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, 
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    return


def setDummyLoad(modelName, tipName, magnitude=1e-5):
    a = mdb.models[modelName].rootAssembly
    r1 = a.instances[tipName].referencePoints
    p = mdb.models[modelName].parts[tipName]
    refPointNo = p.referencePoints.keys()[0]
    refPoints1=(r1[refPointNo], )
    region = a.Set(referencePoints=refPoints1, name='Set-2')
    mdb.models[modelName].DisplacementBC(name='dummy_contact', createStepName=
        'Dummy', region=region, u1=UNSET, u2=magnitude, ur3=UNSET, 
        amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    mdb.models[modelName].boundaryConditions['dummy_contact'].deactivate(
        'Ramp')
    return


def setNH(materialName, modelName, G, **kwargs):
    """
    Set Neo-Hookean material properties for given model.
    
    Parameters
    ----------
    materialName : str
        Name of material being created.
    modelName : str
        Name of model where the material is going to be created.
    G : float
        Initial shear modulus of the material.
    D1 : float, optional
        D1 parameter of the material, defaulted to 2e5 / G (assuming that
        K = G * 1e-5, and we know D1 = 2 / K
        
    """
    if 'D1' in kwargs:
        D1 = kwargs['D1']
    elif 'nu' in kwargs:
        nu = kwargs['nu']
        K = 2. * G * (1. + nu) / (3. * (1. - 2. * nu))
        D1 = 2. / K
    else:
        D1 = 2e5 / G
    mdb.models[modelName].Material(name=materialName)
    mdb.models[modelName].materials[materialName].Hyperelastic(
        materialType=ISOTROPIC, testData=OFF, type=NEO_HOOKE, 
		volumetricResponse=VOLUMETRIC_DATA, table=((G/2., D1), ))
    return




