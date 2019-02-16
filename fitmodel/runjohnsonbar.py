from createmodel.setbar import buildBar
from sim.simclass import BarPs as BarPsSim
import time
import numpy as np

    
def runJohnsonBar(width=3e-3, keepOdb=True):
    barPs = BarPsSim(width=width)
    barPs.runModel()
    time.sleep(5)
    barPs.transferOdb()
    barPs.deleteModel()
    barPs.deleteJob()
    barPs.extractModelOutputs()
    if not keepOdb:
        barPs.deleteOdb()
    return
