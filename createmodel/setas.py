from abqimport import *
import numpy as np
from createtools import setNH

# Define globals
from constants import GArrayAverage as GList
modelName = 'as'

def main():
    contourCoordList = [[] for i in range(5)]    
    for i in range(5):
        contourCoordList[i] = np.genfromtxt('./createmodel/csv/axisymCoordList'+str(i)+'.csv',delimiter=',') * 1e-3
    
    mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT) # Create the model
    
    p = mdb.models[modelName].Part(name='finger', dimensionality=AXISYMMETRIC, 
        type=DEFORMABLE_BODY) # Create empty part
    s = makeSketch(contourCoordList[0]) # Draw the geometry of the epidermis layer
    p.BaseShell(sketch=s) # Convert geometry into part
    del mdb.models[modelName].sketches['__profile__'] # Recycle the sketch
    
    for i in range(2):
        f = p.faces[-1] # Select the face of the part
        s = makeSketch(contourCoordList[i+1])
        p.PartitionFaceBySketch(faces=f, sketch=s)
        del mdb.models[modelName].sketches['__profile__'] # Recycle the sketch
    
    ## Cut the bone from finger and make a rigid bone
    s = makeSketch(contourCoordList[3])
    p.Cut(sketch=s)
    del mdb.models[modelName].sketches['__profile__']
    p = mdb.models[modelName].Part(name='bone', dimensionality=AXISYMMETRIC, 
        type=ANALYTIC_RIGID_SURFACE)
    s = makeSketchAxisymRigid(contourCoordList[3])
    p.AnalyticRigidSurf2DPlanar(sketch=s)
    del mdb.models[modelName].sketches['__profile__']
    
    ## Make a rigid fingernail
    s = makeSketch(contourCoordList[4])
    p = mdb.models[modelName].Part(name='nail', dimensionality=AXISYMMETRIC, 
        type=ANALYTIC_RIGID_SURFACE)
    p.AnalyticRigidSurf2DPlanar(sketch=s)
    del mdb.models[modelName].sketches['__profile__']
    
    ## Set up reference point for the bone and nail
    p = mdb.models[modelName].parts['bone']
    v1, e, d1, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=v1[-1])
    p = mdb.models[modelName].parts['nail']
    v1, e, d1, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=v1[-1])
    
    ## Set up the assembly
    a = mdb.models[modelName].rootAssembly
    a.Instance(name='finger', part=mdb.models[modelName].parts['finger'], dependent=ON)
    a.Instance(name='bone', part=mdb.models[modelName].parts['bone'], dependent=ON)
    a.Instance(name='nail', part=mdb.models[modelName].parts['nail'], dependent=ON)
    
    ## Set up material property
    setNH('epidermis', modelName, GList[0])
    setNH('dermis', modelName, GList[1])
    setNH('hypodermis', modelName, GList[2])
    
    ## Make and assign sections
    p = mdb.models[modelName].parts['finger']
    mdb.models[modelName].HomogeneousSolidSection(name='epidermis', 
        material='epidermis', thickness=None)
    mdb.models[modelName].HomogeneousSolidSection(name='dermis', material='dermis', 
        thickness=None)
    mdb.models[modelName].HomogeneousSolidSection(name='hypodermis', 
        material='hypodermis', thickness=None)
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#2 ]', ), )
    region = p.Set(faces=faces, name='Set-5')
    p.SectionAssignment(region=region, sectionName='epidermis', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(faces=faces, name='Set-6')
    p.SectionAssignment(region=region, sectionName='dermis', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    faces = f.getSequenceFromMask(mask=('[#4 ]', ), )
    region = p.Set(faces=faces, name='Set-7')
    p.SectionAssignment(region=region, sectionName='hypodermis', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)    
    
    ## Set up interaction property
    mdb.models[modelName].ContactProperty('tip2skin')
    mdb.models[modelName].interactionProperties['tip2skin'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
        table=((0.3, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)    
    
    ## Mesh all
    p = mdb.models[modelName].parts['finger']
    p.deleteMesh()
    p.seedPart(size=0.0005, deviationFactor=0.1, minSizeFactor=0.1)
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=(
        '[#ffffffff:2 #7fffffff #0:12 #fffffffc #7ffff ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=0.001, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    pickedEdges = e.getSequenceFromMask(mask=(
        '[#0:3 #ffffffff:5 #7fffffff #ffffffff:6 #3 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=0.00025, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    # Define element types
    f = p.faces
    pickedRegions = f.getSequenceFromMask(mask=('[#7 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TRI, technique=STRUCTURED)
    elemType1 = mesh.ElemType(elemCode=CAX4RH, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=CAX3H, elemLibrary=STANDARD)
    faces = f.getSequenceFromMask(mask=('[#7 ]', ), )
    pickedRegions = (faces, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
    # Generate and modify meshes
    p.generateMesh()

    
    ## Set up sets
    # bone_surface, nail_surface, finger_surface_bone, finger_surface_nail
    p = mdb.models[modelName].parts['bone']
    s = p.edges
    side2Edges = s.getSequenceFromMask(mask=('[#0 #800 ]', ), )
    p.Surface(side2Edges=side2Edges, name='bone_surface')
    p = mdb.models[modelName].parts['nail']
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#0 #10 ]', ), )
    p.Surface(side1Edges=side1Edges, name='nail_surface')
    p = mdb.models[modelName].parts['finger']
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#0:15 #ffffffe4 #7ffff ]', ), )
    p.Surface(side1Edges=side1Edges, name='finger_surface_bone')
    side1Edges = s.getSequenceFromMask(mask=('[#0:9 #fffffffe #ffffffff:5 #1 ]', ), 
        )
    p.Surface(side1Edges=side1Edges, name='finger_surface_nail')
    # contact_nodes and intermediate_nodes
    p = mdb.models[modelName].parts['finger']
    n = p.nodes
    nodes = n.getSequenceFromMask(mask=('[#0:11 #fff80000 #ffffffff:3 ]', ), )
    p.Set(nodes=nodes, name='contact_nodes')
    nodes = n.getSequenceFromMask(mask=('[#0:5 #fffe0000 #ffffffff:2 #7fffffff #0:10 #100000 ]', ), )
    p.Set(nodes=nodes, name='intermediate_nodes')
    ## Set up constraints
    a = mdb.models[modelName].rootAssembly
    a.regenerate()
    region1=a.instances['bone'].surfaces['bone_surface']
    region2=a.instances['finger'].surfaces['finger_surface_bone']
    mdb.models[modelName].Tie(name='tie_bone', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        thickness=ON)
    region1=a.instances['nail'].surfaces['nail_surface']
    region2=a.instances['finger'].surfaces['finger_surface_nail']
    mdb.models[modelName].Tie(name='tie_nail', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
        thickness=ON)    
    
    ## Fix bone    
    a = mdb.models[modelName].rootAssembly
    r1 = a.instances['bone'].referencePoints
    refPoints1=(r1[2], )
    region = a.Set(referencePoints=refPoints1, name='Set-1')
    mdb.models[modelName].DisplacementBC(name='fixed_bone', 
        createStepName='Initial', region=region, u1=SET, u2=SET, ur3=SET, 
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    
    ## Fix finger nodes on axis
    a = mdb.models[modelName].rootAssembly
    e1 = a.instances['finger'].edges
    edges1 = e1.getSequenceFromMask(mask=(
        '[#0:2 #80000000 #0:5 #80000000 #1 #0:5 #1a ]', ), )
    region = a.Set(edges=edges1, name='finger_axis_nodes')
    mdb.models[modelName].DisplacementBC(name='symmetric_axis_finger', 
        createStepName='Initial', region=region, u1=SET, u2=UNSET, ur3=SET, 
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)

    ## Regenerate
    a.regenerate()
    
    return



def splitMeshEdge(part, elemEdges, noList):
    for no in noList:
        part.splitMeshEdge(edge=elemEdges[no])
    return


def makeSketch(coordList):
    s = mdb.models[modelName].ConstrainedSketch(name='__profile__', 
        sheetSize=20.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(viewStyle=AXISYM)
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
    s.FixedConstraint(entity=g[2])
    for i in range(coordList.shape[0]):
        coordStart=coordList[i-1]
        coordEnd=coordList[i]
        s.Line(point1=tuple(coordStart), point2=tuple(coordEnd))
    s.unsetPrimaryObject()
    return s


def makeSketchAxisymRigid(coordList):
    s = mdb.models[modelName].ConstrainedSketch(name='__profile__', 
        sheetSize=20.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(viewStyle=AXISYM)
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -10.0), point2=(0.0, 10.0))
    s.FixedConstraint(entity=g[2])
    for i in range(coordList.shape[0]-1):
        coordStart=coordList[i]
        coordEnd=coordList[i+1]
        s.Line(point1=tuple(coordStart), point2=tuple(coordEnd))
    s.unsetPrimaryObject()
    return s


if __name__=="__main__":
    main()