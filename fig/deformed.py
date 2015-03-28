from abqimport import *

def plot_comp_stress():
    odbTuple = (
        './odbs/as_g1000e04_r400_stip.odb', 
        './odbs/as_g5000e04_r400_stip.odb', 
        './odbs/as_g9000e04_r400_stip.odb', 
        './odbs/as_g1000e04_r600_stip.odb', 
        './odbs/as_g5000e04_r600_stip.odb', 
        './odbs/as_g9000e04_r600_stip.odb', 
        './odbs/as_g1000e04_r800_stip.odb', 
        './odbs/as_g5000e04_r800_stip.odb', 
        './odbs/as_g9000e04_r800_stip.odb', 
        )
    o1 = session.openOdbs(names=odbTuple)
    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=OFF, 
        legend=ON, title=OFF, state=OFF, annotations=OFF, compass=OFF)
    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
        legendTitle=OFF, legendNumberFormat=ENGINEERING)    
    session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
        contourStyle=CONTINUOUS, maxValue=131386, minValue=120.056)
    session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
        spectrum='Reversed rainbow')

    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
        legendFont='-*-arial-medium-r-normal-*-*-240-*-*-p-*-*-*')    
    for odbPath in odbTuple:   
        o1 = session.odbs[odbPath]
        session.viewports['Viewport: 1'].setValues(displayedObject=o1)
        session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
            CONTOURS_ON_DEF, ))
        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
            maxAutoCompute=OFF, maxValue=1e4, minAutoCompute=OFF, minValue=-1e5)
        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
        'Min. Principal'), )  
        session.printOptions.setValues(vpDecorations=OFF, reduceColors=False)
        session.viewports['Viewport: 1'].view.fitView()
        odb = session.odbs[odbPath]
        scratchOdb = session.ScratchOdb(odb=odb)
        node = odb.rootAssembly.instances['BONE'].nodes[0]
        scratchOdb.rootAssembly.DatumCsysBy6dofNode(name='_CAMERA_', 
            coordSysType=CARTESIAN, origin=node)
        session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
            cameraMovesWithCsys=ON, cameraCsysName='_CAMERA_')    
        session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0563416, 
            farPlane=0.0836203, width=0.0104683, height=0.01, 
            viewOffsetX=-0.005, viewOffsetY=-0.004)
        session.printToFile(fileName='./fig/snapshots/'+odbPath[7:-4]+
            '_comp_stress.png', format=PNG, canvasObjects=(
            session.viewports['Viewport: 1'], ))
 
 
def plot_sener():
    odbTuple = (
        './odbs/as_g1000e04_r400_stip.odb', 
        './odbs/as_g5000e04_r400_stip.odb', 
        './odbs/as_g9000e04_r400_stip.odb', 
        './odbs/as_g1000e04_r600_stip.odb', 
        './odbs/as_g5000e04_r600_stip.odb', 
        './odbs/as_g9000e04_r600_stip.odb', 
        './odbs/as_g1000e04_r800_stip.odb', 
        './odbs/as_g5000e04_r800_stip.odb', 
        './odbs/as_g9000e04_r800_stip.odb', 
        )
    o1 = session.openOdbs(names=odbTuple)
    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=OFF, 
        legend=ON, title=OFF, state=OFF, annotations=OFF, compass=OFF)
    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
        legendTitle=OFF, legendNumberFormat=ENGINEERING)    
    session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
        contourStyle=CONTINUOUS, maxValue=131386, minValue=120.056)
    session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
        spectrum='Rainbow')

    session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
        legendFont='-*-arial-medium-r-normal-*-*-240-*-*-p-*-*-*')    
    for odbPath in odbTuple:   
        o1 = session.odbs[odbPath]
        session.viewports['Viewport: 1'].setValues(displayedObject=o1)
        session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
            CONTOURS_ON_DEF, ))
        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
            maxAutoCompute=OFF, maxValue=4e3, minAutoCompute=OFF, minValue=0)
        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
            variableLabel='SENER', outputPosition=INTEGRATION_POINT, )
        session.printOptions.setValues(vpDecorations=OFF, reduceColors=False)
        session.viewports['Viewport: 1'].view.fitView()
        odb = session.odbs[odbPath]
        scratchOdb = session.ScratchOdb(odb=odb)
        node = odb.rootAssembly.instances['BONE'].nodes[0]
        scratchOdb.rootAssembly.DatumCsysBy6dofNode(name='_CAMERA_', 
            coordSysType=CARTESIAN, origin=node)
        session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
            cameraMovesWithCsys=ON, cameraCsysName='_CAMERA_')    
        session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0563416, 
            farPlane=0.0836203, width=0.0104683, height=0.01, 
            viewOffsetX=-0.005, viewOffsetY=-0.004)
        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
            outsideLimitsAboveColor='#FF0000')
        session.printToFile(fileName='./fig/snapshots/'+odbPath[7:-4]+
            '_sener.png', format=PNG, canvasObjects=(
            session.viewports['Viewport: 1'], ))
    