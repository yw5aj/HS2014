# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 12:33:37 2013

@author: Yuxiang Wang
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    pass


if __name__ == '__main__':
    main()



tip_name = ['d635', 'plate']
spec_list = [':sk', '-sk', ':ok', '-ok']
label_list = ["Gulati(1995): plate", "Model: plate", "Gulati(1995): cylinder", 
              "Model: cylinder"]

fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(3.27, 3.27))

for i in range(4):
    for j in range(2):
        for k in range(2):
            fig_data = np.genfromtxt('./fig/as_rigid_'+tip_name[j]+'_tip/'+
                str(i+1)+'data'+str(k+1)+'.csv', delimiter=',')
            fig_data[:, 0] = fig_data[:, 0] * 1e3
            axs.ravel()[i].plot(fig_data[:, 0], fig_data[:, 1], 
                spec_list[2*j+k], label=label_list[2*j+k], markersize=2)
            axs.ravel()[i].set_title('Subject #'+str(i+1), fontsize=8)
            axs.ravel()[i].set_xlim((0, 3.5))
            axs.ravel()[i].set_xticks(np.arange(0, 3.5, 1.))
for axes in axs[:, 0]:
    axes.set_ylabel('Force (N)')
for axes in axs[-1, :]:
    axes.set_xlabel('Tip disp. (mm)')
axs.ravel()[-1].legend(fontsize=6, loc=1, frameon=False)

fig.tight_layout()
fig.savefig('./fig/mag_curve.pdf', format='pdf')
fig.savefig('./fig/mag_curve.png', format='png', dpi=300)
