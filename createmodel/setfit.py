
from abqimport import *
from buildbase import buildBase
from createtools import setNH, setInteraction, setStep, setDispLoad

def buildAll():
    buildBase()
    setup_rigid_d317('ps')
    setup_rigid_d952('ps')
    setup_rigid_d635('as')
    setup_rigid_plate('as')
    regenerateAll()


def regenerateAll():
    for key in mdb.models.keys():
        a = mdb.models[key].rootAssembly
        a.regenerate()
    return


def setup_rigid_d635(baseModelName='as'):
    modelName, tipName = build_rigid_d635(baseModelName)
    setInteraction(modelName, tipName=tipName)
    setStep(modelName, timePts=np.arange(.5, 4., .5))
    setDispLoad(modelName=modelName, tipName=tipName, magnitude=3.e-3)
    return


def setup_rigid_d317(baseModelName='ps'):
    modelName, tipName = build_rigid_d317(baseModelName)
    setInteraction(modelName, tipName=tipName)
    setStep(modelName, timePts=np.array([.5, 1., 1.6, 2.5, 3., 3.5]))
    setDispLoad(modelName=modelName, tipName=tipName, magnitude=3.5e-3)
    return


def setup_rigid_d952(baseModelName='ps'):
    modelName, tipName = build_rigid_d952(baseModelName)
    setInteraction(modelName, tipName=tipName)
    setStep(modelName, timePts=np.array([.6, 1.25, 1.8, 2.5, 3, 3.5]))
    setDispLoad(modelName=modelName, tipName=tipName, magnitude=3.5e-3)    
    return


def setup_rigid_plate(baseModelName='as'):
    modelName, tipName = build_rigid_plate(baseModelName)
    setInteraction(modelName, tipName=tipName)
    setStep(modelName, timePts=np.arange(0, 2.5, .5))
    setDispLoad(modelName=modelName, tipName=tipName, magnitude=2e-3)
    return


def build_rigid_d635(baseModelName='as'):
    tipName = 'rigid_d635_tip'
    modelName = baseModelName + '_' + tipName
    mdb.Model(name=modelName, objectToCopy=mdb.models[baseModelName])    
    dia = 6.35e-3
    s1 = mdb.models[modelName].ConstrainedSketch(name='__profile__', sheetSize=0.01)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.sketchOptions.setValues(decimalPlaces=4)
    s1.setPrimaryObject(option=STANDALONE)
    s1.rectangle(point1=(0.0, 0.0), point2=(dia/2., -0.005))
    s1.setAsConstruction(objectList=(g[2], ))
    s1.setAsConstruction(objectList=(g[3], ))
    s1.FilletByRadius(radius=0.1*dia, curve1=g[5], nearPoint1=(
        0.0023848032578826, -1.00615434348583e-05), curve2=g[4], nearPoint2=(
        0.00315582100301981, -0.000851194839924574))        
    p = mdb.models[modelName].Part(name=tipName, dimensionality=AXISYMMETRIC, 
        type=ANALYTIC_RIGID_SURFACE)
    p.AnalyticRigidSurf2DPlanar(sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models[modelName].sketches['__profile__']
    # Assemble
    a = mdb.models[modelName].rootAssembly
    a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0), 
        point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))
    a.Instance(name=tipName, part=p, dependent=ON)
    # Set reference point
    v2, e1, d2, n1 = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=v2[2])  
    # Define surface
    s = p.edges
    side2Edges = s.getSequenceFromMask(mask=('[#2 ]', ), )
    p.Surface(side2Edges=side2Edges, name='tip_contact_surface')
    return (modelName, tipName)


def build_rigid_d317(baseModelName='ps'):
    tipName = 'rigid_d317_tip'
    modelName = baseModelName + '_' + tipName
    mdb.Model(name=modelName, objectToCopy=mdb.models[baseModelName])
    dia = 3.17e-3
    s = mdb.models[modelName].ConstrainedSketch(name='__profile__', 
        sheetSize=0.005)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=4)
    s.setPrimaryObject(option=STANDALONE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(-0.0018, 0.0002), point2=(
        0.001625, 0.000275), direction=CLOCKWISE)
    s.RadialDimension(curve=g[2], textPoint=(0.0, 0.0), radius=dia/2.)
    s.Line(point1=(0.0, 0.0), point2=(-0.00157530571945769, 0.000175033968828632))
    s.Line(point1=(0.0, 0.0), point2=(0.00156277970345108, 0.000264470411353259))
    s.setAsConstruction(objectList=(g[3], ))
    s.setAsConstruction(objectList=(g[4], ))
    s.AngularDimension(line1=g[3], line2=g[4], textPoint=(4.33626119047403e-05, 
        0.000344789470545948), value=179.)
    s.ConstructionLine(point1=(0.0, 0.0), point2=(0.0, 0.00107500001825392))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.CoincidentConstraint(entity1=v[2], entity2=g[5], addUndoState=False)
    s.SymmetryConstraint(entity1=g[3], entity2=g[4], symmetryAxis=g[5])
    p = mdb.models[modelName].Part(name=tipName, 
        dimensionality=TWO_D_PLANAR, type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models[modelName].parts[tipName]
    p.AnalyticRigidSurf2DPlanar(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models[modelName].parts[tipName]
    del mdb.models[modelName].sketches['__profile__']
    a = mdb.models[modelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[modelName].parts[tipName]
    a.Instance(name=tipName, part=p, dependent=ON)
    v1, e, d1, n = p.vertices, p.edges, p.datums, p.nodes
    # Set reference point
    p.ReferencePoint(point=p.InterestingPoint(edge=e[0], rule=CENTER))
    # Assemble
    a.regenerate()
    a1 = mdb.models[modelName].rootAssembly
    a1.translate(instanceList=(tipName, ), vector=(0.0, -dia/2., 0.0))
    # Define surface
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Surface(side1Edges=side1Edges, name='tip_contact_surface')
    return (modelName, tipName)


def build_rigid_d952(baseModelName='ps'):
    tipName = 'rigid_d952_tip'
    modelName = baseModelName + '_' + tipName
    mdb.Model(name=modelName, objectToCopy=mdb.models[baseModelName])
    dia = 9.52e-3
    s = mdb.models[modelName].ConstrainedSketch(name='__profile__', 
        sheetSize=0.005)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=4)
    s.setPrimaryObject(option=STANDALONE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(-0.0018, 0.0002), point2=(
        0.001625, 0.000275), direction=CLOCKWISE)
    s.RadialDimension(curve=g[2], textPoint=(0.0, 0.0), radius=dia/2.)
    s.Line(point1=(0.0, 0.0), point2=(-0.00157530571945769, 0.000175033968828632))
    s.Line(point1=(0.0, 0.0), point2=(0.00156277970345108, 0.000264470411353259))
    s.setAsConstruction(objectList=(g[3], ))
    s.setAsConstruction(objectList=(g[4], ))
    s.AngularDimension(line1=g[3], line2=g[4], textPoint=(4.33626119047403e-05, 
        0.000344789470545948), value=179.)
    s.ConstructionLine(point1=(0.0, 0.0), point2=(0.0, 0.00107500001825392))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.CoincidentConstraint(entity1=v[2], entity2=g[5], addUndoState=False)
    s.SymmetryConstraint(entity1=g[3], entity2=g[4], symmetryAxis=g[5])
    p = mdb.models[modelName].Part(name=tipName, 
        dimensionality=TWO_D_PLANAR, type=ANALYTIC_RIGID_SURFACE)
    p = mdb.models[modelName].parts[tipName]
    p.AnalyticRigidSurf2DPlanar(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models[modelName].parts[tipName]
    del mdb.models[modelName].sketches['__profile__']
    a = mdb.models[modelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[modelName].parts[tipName]
    a.Instance(name=tipName, part=p, dependent=ON)
    v1, e, d1, n = p.vertices, p.edges, p.datums, p.nodes
    # Set reference point
    p.ReferencePoint(point=p.InterestingPoint(edge=e[0], rule=CENTER))
    # Assemble
    a.regenerate()
    a1 = mdb.models[modelName].rootAssembly
    a1.translate(instanceList=(tipName, ), vector=(0.0, -dia/2, 0.0))
    # Define surface
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Surface(side1Edges=side1Edges, name='tip_contact_surface')
    return (modelName, tipName)


def build_rigid_plate(baseModelName='as'):
    tipName = 'rigid_plate_tip'
    modelName = baseModelName + '_' + tipName
    mdb.Model(name=modelName, objectToCopy=mdb.models[baseModelName])
    # Sketch and build model
    s1 = mdb.models[modelName].ConstrainedSketch(name='__profile__', sheetSize=0.01)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.sketchOptions.setValues(decimalPlaces=4, viewStyle=AXISYM)
    s1.setPrimaryObject(option=STANDALONE)
    s1.ConstructionLine(point1=(0.0, -0.005), point2=(0.0, 0.005))
    s1.FixedConstraint(entity=g[2])
    s1.Line(point1=(0.0, 0.0), point2=(0.02, 0.0))
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    p = mdb.models[modelName].Part(name=tipName, dimensionality=AXISYMMETRIC, 
        type=ANALYTIC_RIGID_SURFACE)
    p.AnalyticRigidSurf2DPlanar(sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models[modelName].sketches['__profile__']
    a = mdb.models[modelName].rootAssembly
    a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0), 
        point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))
    a.Instance(name=tipName, part=p, dependent=ON)
    # Set reference point
    v1, e, d1, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=v1[0])
    # Define surface
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Surface(side1Edges=side1Edges, name='tip_contact_surface')
    return (modelName, tipName)


if __name__ == '__main__':
    main()