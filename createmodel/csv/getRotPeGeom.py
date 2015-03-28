import numpy as np
import matplotlib.pyplot as plt


def main():
    layerContourCoordList = [[] for i in range(5)]   
    for i in range(5):
        layerContourCoordList[i] = np.genfromtxt('layerContourCoordList'+str(i)+'.csv', delimiter=',')
    linePara=(17.366838, -9.84968, -7.13683) # A tuple containing x0, y0, k
    
    cor = np.array(linePara[0:2]) # define center of rotation
    aor = -(0.5*np.pi - (- np.arctan(linePara[2])))
    
    rotLayerContourCoordList = [[] for i in range(5)]
    for i in range(5):
        rotLayerContourCoordList[i] = rotateCoord(layerContourCoordList[i],cor,aor)
    
    
    fig, axs = plt.subplots(1,1)      
    
    axs = plotAllLayers(layerContourCoordList,axs)
    axs.plot(range(15,19),getYofLine(np.array(range(15,19)),linePara))
    fig.show()
    
    axs = plotAllLayers(rotLayerContourCoordList, axs)
    axs.plot([0,0],[0, 15],'-')
    fig.show()
    
    for i in range(5):    
        np.savetxt('./temp/rotCoordList'+str(i)+'.csv',rotLayerContourCoordList[i],delimiter=',')
    


def getYofLine(x,linePara):
    x0, y0, k = linePara
    y = k*(x-x0) + y0
    return y


def plotAllLayers(coordListList, axs):
    for coordList in coordListList:
        axs.plot(coordList[:,0],coordList[:,1],'.')
    return axs



def rotateCoord(coordList,cor,aor):
    transCoordList = coordList - cor
    rotationMatrix = np.array([[np.cos(aor),-np.sin(aor)],[np.sin(aor),np.cos(aor)]])
    rotCoordList = []
    for coord  in transCoordList:
        rotCoordList.append(np.dot(rotationMatrix,coord))
    rotCoordList = np.array(rotCoordList)
    return rotCoordList


if __name__=='__main__':
    main()

