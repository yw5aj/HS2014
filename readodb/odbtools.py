from abqimport import *
from uuid import uuid4


def getWholeModelOutput(jobName):
    import cPickle
    odb = openOdb_(jobName)
    data_dict = {}
    step = odb.steps['Ramp']
    time = []
    kinesthetic_output, tactile_output = [], []
    kinesthetic = ['U', 'RF', 'CF']
    tactile = ['S', 'LE', 'SENER']
    for frame in step.frames:
        time.append(frame.frameValue)
        # Output kinesthetic 
        kinesthetic_output.append({})
        for key in kinesthetic:
            kinesthetic_output[-1][key] = []
            for instance_name, instance in odb.rootAssembly.instances.items():
                for node in instance.nodes:
                    try:
                        value = frame.fieldOutputs[key].getSubset(region=node).values[0]
                        kinesthetic_output[-1][key].append({})
                        output_dict = kinesthetic_output[-1][key][-1]
                        output_dict['instance'] = value.instance.name
                        output_dict['data'] = value.data
                        output_dict['magnitude'] = value.magnitude        
                        output_dict['coordinate'] = node.coordinates
                    except IndexError:
                        pass
        # Output tactile 
        tactile_output.append({})
        for key in tactile:
            tactile_output[-1][key] = []
            for instance_name, instance in odb.rootAssembly.instances.items():
                for node in instance.nodes:
                    try:
                        value = frame.fieldOutputs[key].getSubset(region=node, position=ELEMENT_NODAL).values[0]
                        tactile_output[-1][key].append({})
                        output_dict = tactile_output[-1][key][-1]
                        output_dict['instance'] = value.instance.name
                        output_dict['data'] = value.data
                        output_dict['minPrincipal'] = value.minPrincipal
                        output_dict['coordinate'] = node.coordinates
                    except IndexError:
                        pass
    data_dict['time'] = np.array(time)
    data_dict['kinesthetic_output'] = kinesthetic_output
    data_dict['tactile_output'] = tactile_output
    with open('./pickles/%s.pkl' % jobName, 'w') as f:
        cPickle.dump(data_dict, f)
    odb.close()
    return


def getSurfaceCoordinates(jobName):
    odb = openOdb_(jobName)
    surfaceNodes = odb.rootAssembly.instances['FINGER'].nodeSets['CONTACT_NODES'].nodes
    coordinates = []
    for node in surfaceNodes:
        coordinates.append(node.coordinates[:2])
    coordinates = np.array(coordinates)
    odb.close()
    return coordinates


def getSurfaceDeflection(jobName):
    odb = openOdb_(jobName)
    frames = odb.steps['Ramp'].frames
    surfaceNodes = odb.rootAssembly.instances['FINGER'].nodeSets[
        'CONTACT_NODES'].nodes
    surfaceDeflection = np.empty((len(surfaceNodes),len(frames)))
    for frameCounter, frame in enumerate(frames):
        for nodeCounter, node in enumerate(surfaceNodes):
            surfaceDeflection[nodeCounter, frameCounter] = frame.fieldOutputs[
                'U'].getSubset(region=node).values[0].data[1]
    odb.close()
    return surfaceDeflection


def getDeflectionMatrix(jobName):
    """
    Deprecated.
    Find the surface deflection at different time points.
    
    Parameters
    ----------
    jobName : string
        The jobName in current mdb.
    
    Returns
    -------
    deflectionMatrix : ndarray
        1st column the x coord and 2nd - nth column are the U2s of the node
    """
    # Get the coordinates and displacements at surface, from odb file
    odb = openOdb_(jobName)
    frameList = odb.steps['Ramp'].frames
    surfaceNodes = odb.rootAssembly.instances['FINGER'].nodeSets['CONTACT_NODES'].nodes
    coordList = [[] for i in range(len(frameList))]
    deflectionList = [[] for i in range(len(frameList))]
    for frameCounter, frame in enumerate(frameList):
        frameTime = frame.frameValue
        for node in surfaceNodes:
            coordList[frameCounter].append(node.coordinates[0:2])
            deflectionList[frameCounter].append(frame.fieldOutputs[
                'U'].getSubset(region=node).values[0].data)
        else:
            continue
    # Generate deflectionMatrix 
    for i in range(len(frameList)):
        coordList[i] = np.array(coordList[i])
        deflectionList[i] = np.array(deflectionList[i])
    nodeNum = coordList[0].shape[0]
    deflectionMatrix = np.zeros([nodeNum,1+len(frameList)])
    for i in range(nodeNum):
        deflectionMatrix[i,0] = coordList[0][i][0]
        for j in range(len(frameList)):
            deflectionMatrix[i,j+1] = deflectionList[j][i][1]
    odb.close()
    return deflectionMatrix


def getTipForceDisp(jobName):
    """
    Find the force and displacement curve from indentation tip.
    
    Parameters
    ----------
    jobName : string
        The jobName in current mdb / odbName for the odb.
    
    Returns
    -------
    disp_force_y : ndarray
        Displacement-force result of the model, with the first column as
        displacement and second column as force. Note that the force is the
        magnitude (abs) in the normal direction.
    """
    # Get the coordinates and displacements at surface, from odb file
    odb = openOdb_(jobName)
    frameList = odb.steps['Ramp'].frames
    for key in odb.rootAssembly.nodeSets.keys():
        if key.startswith('REFERENCE_POINT') and 'TIP' in key:
            rp = odb.rootAssembly.nodeSets[key].nodes[0][0]
    force_xy = []
    disp_xy = []
    for frame in frameList:
        force_xy.append(frame.fieldOutputs['RF'].getSubset(region=rp).values[0].data)
        disp_xy.append(frame.fieldOutputs['U'].getSubset(region=rp).values[0].data)
    odb.close()
    # Generate force-disp trace
    force_xy = np.array(force_xy)
    disp_xy = np.array(disp_xy)
    force_mag = []
    disp_mag = []
    force_y = []
    disp_y = []
    for force in force_xy:
        force_mag.append(np.linalg.norm(force))
        force_y.append(abs(force[1]))
    for disp in disp_xy:
        disp_mag.append(np.linalg.norm(disp))
        disp_y.append(abs(disp[1]))
    force_mag = np.array(force_mag)
    disp_mag = np.array(disp_mag)
    force_y = np.array(force_y)
    disp_y = np.array(disp_y)
    disp_force_mag = np.column_stack((disp_mag, force_mag))
    disp_force_y = np.column_stack((disp_y, force_y))
    return disp_force_y


def getMcncNodeDistribution(jobName, quantity):
    """
    Deprecated
    Get distribution of quantities at MCNC location, specifically at 
    epidermis-dermis junction nodes.
    
    Parameters
    ----------
    jobName : str
        Job name, used to locate odb file.
    quantity : str
        The quantity to output distribution, can be one of the following:
            'stressMinPrincipal': minPrincipal in S
            'stressVertical': S22
            'stressVonMises': Von Mises in S
            'strainMinPrincipal': minPrincipal in LE
            'strainVertical': LE22
            'sener': SENER
        Note that they are all taken absolute values.
    
    Returns
    -------
    mcncNodeOutputs : ndarray of shape (M, N)
        Extracted mcncNodeOutputs specified.
    """
    # Map Abaqus fieldName to quantity name
    if quantity.startswith('stress'):
        fieldName = 'S'
    elif quantity.startswith('strain'):
        fieldName = 'LE'
    elif quantity.startswith('sener'):
        fieldName = 'SENER'
    # Open odb, get coordinates and time points
    odb = openOdb_(jobName)
    mcncNodeList = odb.rootAssembly.instances['FINGER'].nodeSets[
        'INTERMEDIATE_NODES'].nodes
    # Fill the mcncNodeOutputs
    step = odb.steps['Ramp']
    frames = step.frames
    mcncNodeOutputs = np.empty((len(mcncNodeList), len(frames)))
    for (frameCounter, frame) in enumerate(frames):
        for nodeCounter, node in enumerate(mcncNodeList):
            output = frame.fieldOutputs[fieldName].getSubset(region=node, 
                position=ELEMENT_NODAL, readOnly=True).values[0]
            if quantity.endswith('Principal'):
                mcncNodeOutputs[nodeCounter, frameCounter] = output.minPrincipal
            elif quantity.endswith('Vertical'):
                mcncNodeOutputs[nodeCounter, frameCounter] = output.data[1]
            elif quantity.endswith('VonMises'):
                mcncNodeOutputs[nodeCounter, frameCounter] = output.mises
            elif quantity.endswith('sener'):
                mcncNodeOutputs[nodeCounter, frameCounter] = output.data
    mcncNodeOutputs = np.abs(mcncNodeOutputs)
    odb.close()
    return mcncNodeOutputs


def getTimePts(jobName):
    """
    Returns timePts ndarray given odb or jobName.
    """
    odb = openOdb_(jobName)
    timePtsList = []
    step = odb.steps['Ramp']
    for frame in step.frames:
        timePtsList.append(frame.frameValue)
    timePts = np.array(timePtsList)
    odb.close()
    return timePts


def getMcncNodeCoordinates(jobName):
    odb = openOdb_(jobName)
    mcncNodeList = odb.rootAssembly.instances['FINGER'].nodeSets[
        'INTERMEDIATE_NODES'].nodes
    coordinates = np.empty((len(mcncNodeList), 2))
    for nodeCounter, node in enumerate(mcncNodeList):
        coordinates[nodeCounter] = node.coordinates[:2]    
    odb.close()
    return coordinates


def openOdb_(jobName, readOnly=True):
    odb = odbAccess.openOdb('./odbs/'+jobName+'.odb', readOnly=readOnly)
    return odb