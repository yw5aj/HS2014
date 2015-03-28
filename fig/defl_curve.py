# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 10:19:08 2013

@author: Yuxiang Wang
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    pass


if __name__ == '__main__':
    main()


fig = {}
axs = {}

for tip_dia in [317, 952]:
    fig[tip_dia], axs[tip_dia] = plt.subplots(3, 2, sharex=True, sharey=True, 
        figsize=(3.27, 3.27))
    for i in range(6):
        fig_data = []
        for j in range(2):
            fig_data.append(np.genfromtxt('./fig/pe_rigid_d'+str(tip_dia)+'_tip/'
                +str(i+1)+'data'+str(j+1)+'.csv', delimiter=',')*1e3)
        axes = axs[tip_dia].ravel()[i]
        axes.plot(fig_data[0][:, 0], fig_data[0][:, 1], ':k', label="Dandekar(1995)")
        axes.plot(fig_data[1][:, 0], fig_data[1][:, 1], '-k', label="Model")
        axes.set_xlim((-10, 10))
        axes.set_ylim((-1.5, 4.5))
        label = "Depth: %.2f"%fig_data[1][:, 1].max()+" mm"
        axes.text(0.5, 0.12, label, transform=axes.transAxes, ha='center', fontsize=6)        
    for axes in axs[tip_dia][:, 0]:
        axes.set_ylabel('Deflection (mm)')
        axes.set_yticks(np.arange(-.5, 4.5, 1))
    for axes in axs[tip_dia][-1, :]:
        axes.set_xlabel('Location (mm)')
    fig[tip_dia].subplots_adjust(top=0.8)
    fig[tip_dia].suptitle('Cylindrical Indenter Dia. '+str(tip_dia/100.)+' mm', 
        y = .99, fontsize=10)    
    axs[tip_dia].ravel()[0].legend(loc=1, fontsize=6)
    fig[tip_dia].tight_layout()
    fig[tip_dia].savefig('./fig/defl_curve_'+str(tip_dia)+'.pdf', format='pdf')
    fig[tip_dia].savefig('./fig/defl_curve_'+str(tip_dia)+'.png', format='png', dpi=300)
    