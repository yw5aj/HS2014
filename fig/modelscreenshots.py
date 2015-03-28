
mdb.Model(name='ABQdummy')
a = mdb.models['ABQdummy'].rootAssembly
mdb.ModelFromInputFile(name='Sphere-Hyper-MaenoEpi-RC305-1mmDepth', 
    inputFileName='X:/AbaqusFolder/hs2014/createmodel/RawModel/Sphere-Hyper-MaenoEpi-RC305-1mmDepth.inp')
del mdb.models['ABQdummy']
a = mdb.models['Sphere-Hyper-MaenoEpi-RC305-1mmDepth'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].view.setValues(nearPlane=81.7785, 
    farPlane=130.787, width=27.9026, height=17.2988, viewOffsetX=2.00409, 
    viewOffsetY=7.3064)
a.features['INDENTOR-1'].suppress()    
session.printToFile(fileName='./fig/3d.png', format=PNG, canvasObjects=(
    session.viewports['Viewport: 1'], ))

