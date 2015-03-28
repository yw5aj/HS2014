import matplotlib.pyplot as plt
import numpy as np


def main():
    frontCoordArray = np.genfromtxt('./getgeometry/frontCoordArray.csv', delimiter=',')
    sideCoordArray = np.genfromtxt('./getgeometry/sideCoordArray.csv', delimiter=',')
    fig, axs = plt.subplots(3, 3, figsize=(6.28, 6.28), sharex=True, sharey=True)
    for i, x in enumerate(range(15, 24, 1)):
        axes = axs.ravel()[i]
        plotBoth(axes, x=x)
        axes.set_title('Shifted '+str(x)+' mm')
    for axes in axs[:, 0]:
        axes.set_ylabel('Y coord. (mm)')
    for axes in axs[-1, :]:
        axes.set_xlabel('X coord. (mm)')
    fig.savefig('./fig/set_shifted.png', dpi=300)
    return


def plotBoth(axes, x=22.5):
    plotFrontContour(x, frontCoordArray, axes, tol=.2)
    plotSideContour(x, sideCoordArray, axes)
    axes.set_xlim(-15, 15)
    axes.set_ylim(-5, 20)
    return axes



def plotFrontContour(x, frontCoordArray, axs, tol = .2):
    leftIdx =  np.nonzero(frontCoordArray[:, 0] > x-tol)[0]
    rightIdx = np.nonzero(frontCoordArray[:, 0] < x+tol)[0]
    idxToDisplay = np.intersect1d(leftIdx, rightIdx)
    arrayToDisplay = frontCoordArray[idxToDisplay]
    axs.plot(-arrayToDisplay[:, 2], arrayToDisplay[:, 1]-arrayToDisplay[:, 1].min(), '.k')
    axs.plot(arrayToDisplay[:, 2], arrayToDisplay[:, 1]-arrayToDisplay[:, 1].min(), '.k')
    axs.set_aspect('equal')
    return

def plotSideContour(x, sideCoordArray, axs):
    halfFingerCoordArrayIdx = sideCoordArray[:, 1]<0
    halfFingerCoordArray = sideCoordArray[halfFingerCoordArrayIdx]
    halfFingerCoordArray = halfFingerCoordArray[halfFingerCoordArray[:, 0].argsort()]
    point1idx = np.nonzero(halfFingerCoordArray>x)[0][0] - 1
    point2idx = np.nonzero(halfFingerCoordArray>x)[0][0]
    point1 = halfFingerCoordArray[point1idx]
    point2 = halfFingerCoordArray[point2idx]
    slope = (point2[1]-point1[1])/(point2[0]-point1[0])
    theta = np.arctan(slope)
    # Rotate angle = -theta
    rotMatrix = np.array([[np.cos(-theta), -np.sin(-theta), -x], [np.sin(-theta), np.cos(-theta), 0], [0, 0, 1]])
    rotated = sideCoordArray.copy()
    for i, coord in enumerate(rotated):
        rotated[i, :2] = np.dot(rotMatrix, np.hstack((coord[:2], 1)))[:2]
    axs.plot(rotated[:, 0], rotated[:, 1]-rotated[:, 1].min(), '.r')
    return
    


if __name__ == '__main__':
    frontCoordArray = np.genfromtxt('./getgeometry/frontCoordArray.csv', delimiter=',')
    sideCoordArray = np.genfromtxt('./getgeometry/sideCoordArray.csv', delimiter=',')
    main()