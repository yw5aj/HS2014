import numpy as np
import matplotlib.pyplot as plt


LINEPARA = (17.366838, -9.84968, -7.13683)  # (x0, y0, slope)
XCALIB = LINEPARA[0]
XHOUSER = 22


def getLinePara(x):
    # Get lower part of skin coordinates
    coord = np.genfromtxt('layerContourCoordList0.csv', delimiter=',')
    coord = coord[coord[:, 1] < 0]
    coord = coord[coord[:, 0].argsort()]
    # Get Y coordinate of the contact point
    y = np.interp(x, *coord.T)
    # Get the slope
    knorm = np.gradient(coord[:, 1], np.gradient(coord[:, 0]))
    ktan = -1 / knorm
    slope = np.interp(x, coord[:, 0], ktan)
    linePara = (x, y, slope)
    return linePara


def getYofLine(x, linePara):
    x0, y0, k = linePara
    y = k * (x - x0) + y0
    return y


def getXofLine(y, linePara):
    x0, y0, k = linePara
    x = (y - y0) / k + x0
    return x


def plotAllLayers(coordListList, axs):
    for coordList in coordListList:
        axs.plot(coordList[:, 0], coordList[:, 1], '.')
    return axs


def rotateCoord(coordList, cor, aor):
    transCoordList = coordList - cor
    rotationMatrix = np.array(
        [[np.cos(aor), -np.sin(aor)], [np.sin(aor), np.cos(aor)]])
    rotCoordList = []
    for coord in transCoordList:
        rotCoordList.append(np.dot(rotationMatrix, coord))
    rotCoordList = np.array(rotCoordList)
    return rotCoordList


def getIntersection(coord4pts):
    x1, y1 = coord4pts[0]
    x2, y2 = coord4pts[1]
    x3, y3 = coord4pts[2]
    x4, y4 = coord4pts[3]
    x = (-x1 * y2 + x2 * y1 + (x1 - x2) * (-x3 * y4 + x4 * y3 + (y3 - y4) * (
        x1 * y2 - x2 * y1) / (y1 - y2)) / (-x3 + x4 + (x1 - x2) * (y3 - y4) / (
                                           y1 - y2))) / (y1 - y2)
    y = (-x3 * y4 + x4 * y3 + (y3 - y4) * (x1 * y2 - x2 * y1) / (y1 - y2)) / \
        (-x3 + x4 + (x1 - x2) * (y3 - y4) / (y1 - y2))
    return np.array([x, y])


def getUpOfLine(coordList, linePara):
    flagStart = np.nan
    flagEnd = np.nan
    for i in range(coordList.shape[0]):
        if coordList[i - 1, 1] < getYofLine(coordList[i - 1, 0], linePara) and\
                coordList[i, 1] > getYofLine(coordList[i, 0], linePara):
            flagStart = i - 1
        elif coordList[i - 1, 1] > getYofLine(coordList[i - 1, 0], linePara)\
                and coordList[i, 1] < getYofLine(coordList[i, 0], linePara):
            flagEnd = i
    if np.isnan(flagStart) and np.isnan(flagEnd):
        subsetCoordList = coordList
    elif flagStart < flagEnd:
        subsetCoordList = coordList[flagStart:flagEnd + 1]
    elif flagStart > flagEnd:
        subsetCoordList = np.vstack(
            (coordList[flagStart:coordList.shape[0]],
             coordList[0:flagEnd + 1]))
    return subsetCoordList


def getAsGeom(xcontact=XCALIB, plot_layers=False, save_csv=False):
    # Read geometry from old model
    layerContourCoordList = [[] for i in range(5)]
    for i in range(4):
        layerContourCoordList[i] = np.genfromtxt(
            'layerContourCoordList' + str(i) + '.csv', delimiter=',')
    layerContourCoordList[4] = np.genfromtxt(
        'nailCoordList.csv', delimiter=',')
    # Line for the point of contact of the old model
    linePara = getLinePara(xcontact)
    y3 = layerContourCoordList[0][:, 1].min() - 1
    y4 = layerContourCoordList[0][:, 1].max() + 1
    x3, x4 = getXofLine(np.array((y3, y4)), linePara)
    # Start getting new data list
    subsetLayerContourCoordList = [[] for i in range(5)]
    newLayerContourCoordList = [[] for i in range(5)]
    for i in range(5):
        subsetLayerContourCoordList[i] = getUpOfLine(
            layerContourCoordList[i], linePara)
        intersectionStart = getIntersection(
            [subsetLayerContourCoordList[i][0],
             subsetLayerContourCoordList[i][1], [x3, y3], [x4, y4]])
        intersectionEnd = getIntersection(
            [subsetLayerContourCoordList[i][-1],
             subsetLayerContourCoordList[i][-2], [x3, y3], [x4, y4]])
        newLayerContourCoordList[i] = subsetLayerContourCoordList[i]
        # If there are intersections, use intersections to start/end
        if subsetLayerContourCoordList[i] is not layerContourCoordList[i]:
            newLayerContourCoordList[i][0] = intersectionStart
            newLayerContourCoordList[i][-1] = intersectionEnd
    cor = newLayerContourCoordList[0][0]  # define center of rotation
    aor = -(0.5 * np.pi - (- np.arctan(linePara[2])))
    finalLayerContourCoordList = [[] for i in range(5)]
    for i in range(5):
        finalLayerContourCoordList[i] = rotateCoord(
            newLayerContourCoordList[i], cor, aor)
    # Plotting
    if plot_layers:
        fig, axs = plt.subplots()
        axs = plotAllLayers(newLayerContourCoordList, axs)
        axs.plot((x3, x4), (y3, y4), '-')
        axs = plotAllLayers(finalLayerContourCoordList, axs)
        axs.plot([0, 0], [0, 15], '-')
        axs.set_aspect('equal')
    # Save to csv
    if save_csv:
        for i in range(5):
            np.savetxt('./axisymCoordList' + str(i) + '.csv',
                       finalLayerContourCoordList[i], delimiter=',')
    return finalLayerContourCoordList


def getPsGeom(xcontact=XCALIB, plot_layers=False, save_csv=False):
    # Read geometry from old model
    layerContourCoordList = [[] for i in range(5)]
    for i in range(5):
        layerContourCoordList[i] = np.genfromtxt(
            'layerContourCoordList' + str(i) + '.csv', delimiter=',')
    # Get point of contact for the old model
    linePara = getLinePara(xcontact)
    y3 = layerContourCoordList[0][:, 1].min() - 1
    y4 = layerContourCoordList[0][:, 1].max() + 1
    x3, x4 = getXofLine(np.array((y3, y4)), linePara)
    cor = np.array(linePara[0:2])  # define center of rotation
    aor = -(0.5 * np.pi - (- np.arctan(linePara[2])))
    # Get the new coordinates
    rotLayerContourCoordList = [[] for i in range(5)]
    for i in range(5):
        rotLayerContourCoordList[i] = rotateCoord(
            layerContourCoordList[i], cor, aor)
    # Plotting
    if plot_layers:
        fig, axs = plt.subplots()
        axs = plotAllLayers(layerContourCoordList, axs)
        axs.plot((x3, x4), (y3, y4), '-')
        axs = plotAllLayers(rotLayerContourCoordList, axs)
        axs.plot([0, 0], [0, 15], '-')
        axs.set_aspect('equal')
    # Save to csv
    if save_csv:
        for i in range(5):
            np.savetxt('./temp/rotCoordList' + str(i) + '.csv',
                       rotLayerContourCoordList[i], delimiter=',')
    return rotLayerContourCoordList


if __name__ == '__main__':
    plot_layers = True
    save_csv = False
    rotLayerContourCoordList = getPsGeom(XCALIB, plot_layers=plot_layers)
    rotLayerContourCoordList = getPsGeom(22, plot_layers=plot_layers)
    asLayerContourCoordList = getAsGeom(XCALIB, plot_layers=plot_layers)
    asLayerContourCoordList = getAsGeom(22, plot_layers=plot_layers)
