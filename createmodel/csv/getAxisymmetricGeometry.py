import numpy as np
import matplotlib.pyplot as plt


def getRightOfLine(coordList,linePara):
    flagStart = np.nan
    flagEnd = np.nan    
    for i in range(coordList.shape[0]):
        if coordList[i-1,1]<getYofLine(coordList[i-1,0],linePara) and coordList[i,1]>getYofLine(coordList[i,0],linePara):
            flagStart = i-1
        elif coordList[i-1,1]>getYofLine(coordList[i-1,0],linePara) and coordList[i,1]<getYofLine(coordList[i,0],linePara):
            flagEnd = i
    if np.isnan(flagStart) and np.isnan(flagEnd):
        subsetCoordList = coordList
    elif flagStart < flagEnd:
        subsetCoordList = coordList[flagStart:flagEnd+1]
    elif flagStart > flagEnd:
        subsetCoordList = np.vstack((coordList[flagStart:coordList.shape[0]],coordList[0:flagEnd+1]))
    return subsetCoordList


def getYofLine(x,linePara):
    x0, y0, k = linePara
    y = k*(x-x0) + y0
    return y


def plotAllLayers(coordListList, axs):
    for coordList in coordListList:
        axs.plot(coordList[:,0],coordList[:,1],'.')
    return axs


def getIntersection(coord4pts):
    x1, y1 = coord4pts[0]
    x2, y2 = coord4pts[1]
    x3, y3 = coord4pts[2]
    x4, y4 = coord4pts[3]
    x = (-x1*y2 + x2*y1 + (x1 - x2)*(-x3*y4 + x4*y3 + (y3 - y4)*(x1*y2 - x2*y1)/(y1 - y2))/(-x3 + x4 + (x1 - x2)*(y3 - y4)/(y1 - y2)))/(y1 - y2)
    y = (-x3*y4 + x4*y3 + (y3 - y4)*(x1*y2 - x2*y1)/(y1 - y2))/(-x3 + x4 + (x1 - x2)*(y3 - y4)/(y1 - y2))
    return np.array([x,y])


def rotateCoord(coordList,cor,aor):
    transCoordList = coordList - cor
    rotationMatrix = np.array([[np.cos(aor),-np.sin(aor)],[np.sin(aor),np.cos(aor)]])
    rotCoordList = []
    for coord  in transCoordList:
        rotCoordList.append(np.dot(rotationMatrix,coord))
    rotCoordList = np.array(rotCoordList)
    return rotCoordList


if __name__=='__main__':
    layerContourCoordList = [[] for i in range(5)]   
    for i in range(4):
        layerContourCoordList[i] = np.genfromtxt('layerContourCoordList'+str(i)+'.csv', delimiter=',')
    layerContourCoordList[4] = np.genfromtxt('nailCoordList.csv',delimiter=',')
    linePara=(17.366838, -9.84968, -7.13683) # A tuple containing x0, y0, k
    x3, x4 = 15., 18.
    y3, y4 = getYofLine(np.array([x3,x4]),linePara)    
    
    subsetLayerContourCoordList = [[] for i in range(5)]
    newLayerContourCoordList = [[] for i in range(5)]
    for i in range(4):
        subsetLayerContourCoordList[i] = getRightOfLine(layerContourCoordList[i],linePara)
        intersectionStart = getIntersection([subsetLayerContourCoordList[i][0],subsetLayerContourCoordList[i][1],[x3,y3],[x4,y4]])
        intersectionEnd = getIntersection([subsetLayerContourCoordList[i][-1],subsetLayerContourCoordList[i][-2],[x3,y3],[x4,y4]])
        newLayerContourCoordList[i] = subsetLayerContourCoordList[i]
        newLayerContourCoordList[i][0] = intersectionStart
        newLayerContourCoordList[i][-1] = intersectionEnd
    subsetLayerContourCoordList[4] = layerContourCoordList[4]
    newLayerContourCoordList[4] = layerContourCoordList[4]
    
    cor = newLayerContourCoordList[0][0] # define center of rotation
    aor = -(0.5*np.pi - (- np.arctan(linePara[2])))
    
    finalLayerContourCoordList = [[] for i in range(5)]
    for i in range(5):
        finalLayerContourCoordList[i] = rotateCoord(newLayerContourCoordList[i],cor,aor)
    
    # Smooth the dots distribution due to the cut
    smooth_dots = False
    if smooth_dots == True:
        N = 20
        for i in range(3):
            coord = finalLayerContourCoordList[i]
            oldx = coord[:N][:, 0]
            oldy = coord[:N][:, 1]
            newx = np.linspace(0, coord[N-1][0], N)
            newy = np.interp(newx, oldx, oldy)
            finalLayerContourCoordList[i][:N] = np.c_[newx, newy]
    
    fig, axs = plt.subplots()      
    axs = plotAllLayers(newLayerContourCoordList,axs)
    axs.plot(range(15,19), getYofLine(np.array(range(15,19)), linePara))
    fig.show()
    
    axs = plotAllLayers(finalLayerContourCoordList, axs)
    axs.plot([0,0],[0, 15],'-')
    fig.show()
    
    for i in range(5):    
        # Put the newly generated text file into the temp folder to avoid overwriting good data
        np.savetxt('./temp/axisymCoordList'+str(i)+'.csv',finalLayerContourCoordList[i],delimiter=',')

