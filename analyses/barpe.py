import numpy as np
from analysisclass import BarPe
import matplotlib.pyplot as plt
from createmodel.bartipnaming import (getModelNameFromBaseAndBarWidth, 
    getBarWidthFromModelName)
from scipy.interpolate import UnivariateSpline

barPe = BarPe(width=3e-3)
johnson_data = np.genfromtxt(
    './fitmodel/csv/johnsonbar/3mm_bar_dynamic_static.csv', delimiter=',')
xdata = np.r_[-5:5:100j]
s = UnivariateSpline(barPe.mcncNodeCoordinates[:, 0]*1e3, barPe.mcncNodeDict['stressMinPrincipal'][:, -1], s=1e9)
ydata = s(xdata)
    
fig, axs1 = plt.subplots()
axs2 = axs1.twinx()

axs1.plot(barPe.mcncNodeCoordinates[:, 0]*1e3, barPe.mcncNodeDict['stressMinPrincipal'][:, -1], '-')
axs2.plot(johnson_data[::-1, 0]*1e3, johnson_data[:, 2], ':')
axs1.plot(xdata, ydata, '-r')

axs1.set_xlim((-4.5, 4.5))
axs1.set_ylim((3e4, 9e4))
axs2.set_ylim((0, 70))
axs1.set_ylabel('Stress (Pa)')
axs2.set_ylabel('Firing rate (Hz)')
axs1.set_xlabel('Location (mm)')

fig.savefig('./fig/johnsonbar.pdf', format='pdf')
fig.savefig('./fig/johnsonbar.png', format='png', dpi=300)