# -*- coding: utf-8 -*-
"""
Created on Mon Sep 09 07:53:40 2013

@author: Yuxiang Wang
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.interpolate import griddata
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from constants import _deflectionFitResult

def main():
    pass


def meshz(x, y, data):
    pass


if __name__ == '__main__':
    main()


data1 = np.genfromtxt('./fitmodel/csv/r2/r2table_pe_rigid_d317_tip.csv', delimiter=',')
data2 = np.genfromtxt('./fitmodel/csv/r2/r2table_pe_rigid_d952_tip.csv', delimiter=',')
data = 0.5 * (data1 + data2)
# data = np.nan_to_num(data)
np.savetxt('./fitmodel/csv/r2/r2table_pe_rigid_tip_averaged.csv', data, delimiter=',')
grid_x, grid_y = np.mgrid[0:2:100j, 1:3:100j]

grid_z1 = griddata(data[:, :2], data[:, 2], (grid_x, grid_y), method='nearest')
grid_z2 = griddata(data[:, :2], data[:, 2], (grid_x, grid_y), method='linear')
grid_z3 = griddata(data[:, :2], data[:, 2], (grid_x, grid_y), method='cubic')

fig, axs = plt.subplots(1, 1, figsize=(3.27, 3.27))
im = axs.imshow(grid_z1.T[::-1], extent=(0, 2, 1, 3), cmap=cm.coolwarm, vmin=.6, vmax=.8)

axs.set_xlabel('Dermis / Hypodermis (log scale base 10)')
axs.set_ylabel('Epidermis / Dermis (log scale base 10)')

axs.autoscale(False)
optimal_point = tuple(_deflectionFitResult)
axs.plot(optimal_point[0], optimal_point[1], '*', ms=12, mfc='k')
axs.annotate(r"Optimal R$^2$ at (%.2f, %.2f)"%optimal_point, optimal_point, xytext=(-50, 15),
             textcoords='offset points')

axin = inset_axes(axs, width='100%', height='100%', bbox_to_anchor=(1.05, 0., .05, 1.), 
    bbox_transform=axs.transAxes, borderpad=0,)
plt.colorbar(im, cax=axin, ticks=np.arange(.0, .9, .1))
fig.suptitle('Max. R-square search', fontsize=12)

fig.subplots_adjust(right=.85)
fig.savefig('./fig/defl_cloud.pdf', format='pdf')
fig.savefig('./fig/defl_cloud.png', format='png', dpi=300)
