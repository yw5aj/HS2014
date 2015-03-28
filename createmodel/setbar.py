from abqimport import *
from createtools import setInteraction, setStep, setDispLoad
from bartipnaming import (getModelNameFromBaseAndBarWidth, 
    getBarWidthFromModelName)

def buildBar(width=3e-3, baseModelName='pe'):
    modelName = getModelNameFromBaseAndBarWidth(width, baseModelName)
    if modelName in mdb.models.keys():
        del mdb.models[modelName]
    mdb.models.changeKey(fromName=baseModelName, toName=modelName)
    tipName = buildBarTip(modelName)
    setInteraction(modelName, tipName=tipName)
    setStep(modelName, timePts=np.array([1.]))
    setDispLoad(modelName=modelName, tipName=tipName, magnitude=1e-3)
    return modelName


def buildBarTip(modelName, height=5e-3):
    width = getBarWidthFromModelName(modelName)
    tipName = modelName
    # Build tip
    s = mdb.models[modelName].ConstrainedSketch(name='__profile__', sheetSize=0.005)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=4)
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(-width/2., 0.0), point2=(width/2., -height))
    s.FilletByRadius(radius=width/10., curve1=g[2], nearPoint1=(-width/2., -height/5.
        ), curve2=g[5], nearPoint2=(-width/2.*.8, 0.))
    s.FilletByRadius(radius=width/10., curve1=g[5], nearPoint1=(width/2.*.8, 
        0), curve2=g[4], nearPoint2=(width/2., -height/5.))
    p = mdb.models[modelName].Part(name=tipName, dimensionality=TWO_D_PLANAR, 
        type=ANALYTIC_RIGID_SURFACE)
    p.AnalyticRigidSurf2DPlanar(sketch=s)
    s.unsetPrimaryObject()
    del mdb.models[modelName].sketches['__profile__']
    v1, e, d1, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=p.InterestingPoint(edge=e[4], rule=MIDDLE))
    s = p.edges
    side1Edges = s.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Surface(side1Edges=side1Edges, name='tip_contact_surface')
    a = mdb.models[modelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    a.Instance(name=tipName, part=p, dependent=ON)
    a.regenerate()
    return tipName
    