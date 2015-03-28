from abqimport import *
from buildbase import buildBase
from createtools import (setNH, setInteraction, setStep, setDispLoad, 
    setForceLoad)
import re
from softtipnaming import (
    getSphereModelNameFromRadiusAndG, getRadiusFromModelName, getHeightFromModelName,
    getTipNamesFromModelName, getGFromModelName, getCylinderModelNameFromRGH)


def buildAsCylinder(radius, G, height):
    """
    Currently, height must be fixed at 35 mm.
    """
    baseModelName = 'as'
    if 'as' not in mdb.models.keys():
        buildBase(baseModelName)
    modelName = getCylinderModelNameFromRGH(radius, G, height)
    tipBaseName, tipTipName = getTipNamesFromModelName(modelName)
    if modelName in mdb.models.keys():
        del mdb.models[modelName]
    mdb.models.changeKey(fromName=baseModelName, toName=modelName)
    makeTipBase(modelName, baseRadius=radius)
    makeAsCylinderTipTip(modelName)
    assembleAsCylinderTip(modelName)
    setInteraction(modelName, tipTipName)
    setStep(modelName, timePts=np.linspace(.1, 1., 20))
    setForceLoad(modelName, tipBaseName, magnitude=1.)
    return modelName


def buildAsSphere(radius, G):
    baseModelName = 'as'
    if 'as' not in mdb.models.keys():
        buildBase(baseModelName)
    modelName = getSphereModelNameFromRadiusAndG(radius, G)
    tipBaseName, tipTipName = getTipNamesFromModelName(modelName)
    if modelName in mdb.models.keys():
        del mdb.models[modelName]
    mdb.models.changeKey(fromName=baseModelName, toName=modelName)
    makeTipBase(modelName)
    makeAsSphereTipTip(modelName)
    assembleAsSphereTip(modelName)
    setInteraction(modelName, tipTipName)
    setStep(modelName, timePts=np.array([.125, .25, .5, 1.]))
    setForceLoad(modelName, tipBaseName, magnitude=1.)
    return modelName


def buildPeCylinder():
    pass


def makeTipBase(modelName, baseRadius=.015):
    tipBaseName = getTipNamesFromModelName(modelName)[0]
    s1 = mdb.models[modelName].ConstrainedSketch(name='__profile__', 
        sheetSize=0.01)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.sketchOptions.setValues(decimalPlaces=4, viewStyle=AXISYM)
    s1.setPrimaryObject(option=STANDALONE)
    s1.ConstructionLine(point1=(0.0, -0.005), point2=(0.0, 0.005))
    s1.FixedConstraint(entity=g[2])
    s1.Line(point1=(0.0, 0.0), point2=(baseRadius, 0.0))
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    p = mdb.models[modelName].Part(name=tipBaseName, 
        dimensionality=AXISYMMETRIC, type=ANALYTIC_RIGID_SURFACE)
    p.AnalyticRigidSurf2DPlanar(sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models[modelName].sketches['__profile__']
    # Set RF
    v1, e, d1, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=v1[0])
    return tipBaseName


def makeAsCylinderTipTip(modelName):
    tipTipName = getTipNamesFromModelName(modelName)[1]
    radius = getRadiusFromModelName(modelName)
    height = getHeightFromModelName(modelName)
    s = mdb.models[modelName].ConstrainedSketch(name='__profile__', 
        sheetSize=0.01)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=4, viewStyle=AXISYM)
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -0.005), point2=(0.0, 0.005))
    s.FixedConstraint(entity=g[2])
    s.rectangle(point1=(0.0, 0.0), point2=(radius, height))
    s.FilletByRadius(radius=radius/20, curve1=g[4], nearPoint1=(radius, 
        height), curve2=g[5], nearPoint2=(radius, height))    
    p = mdb.models[modelName].Part(name=tipTipName, 
        dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    del mdb.models[modelName].sketches['__profile__']    
    # Mesh tip
    e = p.edges
    pickedEdges1 = e.getSequenceFromMask(mask=('[#2 ]', ), )
    pickedEdges2 = e.getSequenceFromMask(mask=('[#10 ]', ), )
    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, 
        end2Edges=pickedEdges2, minSize=0.00025, maxSize=0.001, constraint=FINER)
    pickedEdges = e.getSequenceFromMask(mask=('[#9 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=0.00025, deviationFactor=0.1, 
        constraint=FINER)
    pickedEdges = e.getSequenceFromMask(mask=('[#1 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=0.0005, deviationFactor=0.1, 
        constraint=FINER)        
    elemType1 = mesh.ElemType(elemCode=CAX4RH, elemLibrary=STANDARD, 
        hourglassControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=CAX3H, elemLibrary=STANDARD)
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(faces, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
    pickedRegions = f.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, technique=FREE, elemShape=TRI)
    p.generateMesh()    
    # Assign tip material
    assignTipMaterial(modelName)    
    return


def makeAsSphereTipTip(modelName):
    tipTipName = getTipNamesFromModelName(modelName)[1]
    radius = getRadiusFromModelName(modelName)
    s1 = mdb.models[modelName].ConstrainedSketch(name='__profile__', 
        sheetSize=0.01)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.sketchOptions.setValues(decimalPlaces=4, viewStyle=AXISYM)
    s1.setPrimaryObject(option=STANDALONE)
    s1.ConstructionLine(point1=(0.0, -0.005), point2=(0.0, 0.005))
    s1.FixedConstraint(entity=g[2])
    s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(radius, 0.0), point2=(0.0, radius), 
        direction=COUNTERCLOCKWISE)
    s1.Line(point1=(0.0, radius), point2=(0.0, 0.0))
    s1.VerticalConstraint(entity=g[4], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s1.Line(point1=(0.0, 0.0), point2=(radius, 0.0))
    s1.HorizontalConstraint(entity=g[5], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    p = mdb.models[modelName].Part(name=tipTipName, 
        dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
    p.BaseShell(sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models[modelName].sketches['__profile__']
    # Mesh tip
    p = mdb.models[modelName].parts[tipTipName]
    p.seedPart(size=250e-6, deviationFactor=0.1, minSizeFactor=0.1)
    e = p.edges
    pickedEdges1 = e.getSequenceFromMask(mask=('[#4 ]', ), )
    pickedEdges2 = e.getSequenceFromMask(mask=('[#1 ]', ), )
    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, 
        end2Edges=pickedEdges2, minSize=0.00025, maxSize=0.001, constraint=FINER)
    f = p.faces
    pickedRegions = f.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TRI)
    elemType1 = mesh.ElemType(elemCode=CAX4RH, elemLibrary=STANDARD, 
        hourglassControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=CAX3H, elemLibrary=STANDARD)
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(faces, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
    p.generateMesh()
    # Assign tip material
    assignTipMaterial(modelName)
    return tipTipName


def assembleAsCylinderTip(modelName):
    radius = getRadiusFromModelName(modelName)
    height = getHeightFromModelName(modelName)
    tipBaseName, tipTipName = getTipNamesFromModelName(modelName)
    # Initialize assembly
    a = mdb.models[modelName].rootAssembly
    a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0), 
    point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))
    # Add instances
    p = mdb.models[modelName].parts[tipBaseName]
    a.Instance(name=tipBaseName, part=p, dependent=ON)
    p = mdb.models[modelName].parts[tipTipName]
    a.Instance(name=tipTipName, part=p, dependent=ON)
    # Translate to position
    a.translate(instanceList=(tipTipName, tipBaseName), vector=(0.0, -height, 0.0))
    # Fix tip on symmetric axis
    e1 = a.instances[tipTipName].edges
    edges1 = e1.getSequenceFromMask(mask=('[#4 ]', ), )
    region = a.Set(edges=edges1, name='tip_axis_nodes')
    mdb.models[modelName].DisplacementBC(name='symmetric_axis_tip', 
        createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, 
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    # Regenerate model
    a.regenerate()
    # Tie tip
    p = mdb.models[modelName].parts[tipTipName]
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#e ]', ), )
    p.Surface(side1Edges=side1Edges, name='tip_contact_surface')
    side1Edges = s.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Surface(side1Edges=side1Edges, name='tip_tip_surface')    
    p = mdb.models[modelName].parts[tipBaseName]
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Surface(side1Edges=side1Edges, name='tip_base_surface')
    # Tie surfaces
    a = mdb.models[modelName].rootAssembly
    region1=a.instances[tipBaseName].surfaces['tip_base_surface']
    region2=a.instances[tipTipName].surfaces['tip_tip_surface']
    mdb.models[modelName].Tie(name='tie_tip', master=region1, 
        slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
        tieRotations=ON, thickness=ON)
    return


def assembleAsSphereTip(modelName):
    radius = getRadiusFromModelName(modelName)
    tipBaseName, tipTipName = getTipNamesFromModelName(modelName)
    # Initialize assembly
    a = mdb.models[modelName].rootAssembly
    a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0), 
    point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))
    # Add instances
    p = mdb.models[modelName].parts[tipBaseName]
    a.Instance(name=tipBaseName, part=p, dependent=ON)
    p = mdb.models[modelName].parts[tipTipName]
    a.Instance(name=tipTipName, part=p, dependent=ON)
    # Translate to position
    a.translate(instanceList=(tipTipName, tipBaseName), vector=(0.0, -radius, 0.0))
    # Fix tip on symmetric axis
    e1 = a.instances[tipTipName].edges
    edges1 = e1.getSequenceFromMask(mask=('[#4 ]', ), )
    region = a.Set(edges=edges1, name='tip_axis_nodes')
    mdb.models[modelName].DisplacementBC(name='symmetric_axis_tip', 
        createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, 
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    # Regenerate model
    a.regenerate()
    # Tie tip
    p = mdb.models[modelName].parts[tipTipName]
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#2 ]', ), )
    p.Surface(side1Edges=side1Edges, name='tip_contact_surface')
    side1Edges = s.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Surface(side1Edges=side1Edges, name='tip_tip_surface')    
    p = mdb.models[modelName].parts[tipBaseName]
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Surface(side1Edges=side1Edges, name='tip_base_surface')
    # Tie surfaces
    a = mdb.models[modelName].rootAssembly
    region1=a.instances[tipBaseName].surfaces['tip_base_surface']
    region2=a.instances[tipTipName].surfaces['tip_tip_surface']
    mdb.models[modelName].Tie(name='tie_tip', master=region1, 
        slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
        tieRotations=ON, thickness=ON)    
    return


def assignTipMaterial(modelName):
    G = getGFromModelName(modelName)
    # Assuming almost incompressible soft-tip
    setNH('tip', modelName, G, nu=.475) 
    tipTipName = getTipNamesFromModelName(modelName)[1]
    mdb.models[modelName].HomogeneousSolidSection(name='tip', 
        material='tip', thickness=None)
    p = mdb.models[modelName].parts[tipTipName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(faces=faces, name='Set-3')
    p.SectionAssignment(region=region, sectionName='tip', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    return


