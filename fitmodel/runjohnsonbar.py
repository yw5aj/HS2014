from createmodel.setbar import buildBar
from sim.simclass import BarPe as BarPeSim
import time
import numpy as np

    
def runJohnsonBar(width=3e-3, keepOdb=True):
    barPe = BarPeSim(width=width)
    barPe.runModel()
    time.sleep(5)
    barPe.transferOdb()
    barPe.deleteModel()
    barPe.deleteJob()
    barPe.extractModelOutputs()
    if not keepOdb:
        barPe.deleteOdb()
    return
