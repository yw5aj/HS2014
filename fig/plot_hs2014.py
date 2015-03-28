# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import analyses.sphereas
import cPickle
def loadData(radii, Gs, reconstruct=True):
    if reconstruct:
        sphereAsList = analyses.sphereas.init(radii=radii, Gs=Gs)
    with open('./pickles/sphereAsList.pkl', 'r') as f:
        sphereAsList = cPickle.load(f)
    return sphereAsList
radii = np.arange(4e-3, 10e-3, 2e-3)
Gs = np.arange(1e4, 10e4, 4e4)
sphereAsList = loadData(radii, Gs, False)

# <codecell>

# fig = plt.figure(figsize=(4.86, 4.86))
# axs = np.empty([3, 3], dtype=object)
# axs[0, 0] = fig.add_subplot(331)
# axs[1, 0] = fig.add_subplot(334)
# axs[2, 0] = fig.add_subplot(337)
# axs[2, 1] = fig.add_subplot(338)
# axs[2, 2] = fig.add_subplot(339)
fig, axs = plt.subplots(3, 3, figsize=(4.86, 4.86))
for axes in axs[:2, 1:].ravel():
    fig.delaxes(axes)
gs = gridspec.GridSpec(3, 3)
axsbig = fig.add_subplot(gs[0:2, 1:3])
patches = []
for sphereAs in sphereAsList:
    axes = axs[sphereAs.row, sphereAs.col]
    if axes in axs[:, 0] or axes in axs[-1, :]:
        if axes is axs[0, 0]:
            spec = '-.'
        elif axes is axs[2, 2]:
            spec = '--'
        else:
            spec = '-'
        patches.append(sphereAs.plotData(sphereAs.mcncNodeCoordinates*1e3, sphereAs.mcncNodeDict['sener']*1e-3, axes, spec=spec)[1])
        label = 'G = '+str(int(sphereAs.G/1e3))+' kPa\nr = '+str(int(sphereAs.radius*1e3))+' mm'
        axes.text(0.6, 0.6, label, transform=axes.transAxes, ha='center')
        axes.set_ylabel(r'SED (kJ/$m^3$)')
        axes.set_xlabel('Location (mm)')
        axes.set_xlim(0, 8)
        axes.set_ylim(0, 3)
    if axes is axs[0, 0]:
        sphereAs00 = sphereAs
    elif axes is axs[2, 2]:
        sphereAs22 = sphereAs
label00 = 'G = '+str(int(sphereAs00.G/1e3))+' kPa, r = '+str(int(sphereAs00.radius*1e3))+' mm'
patches00 = sphereAs00.plotData(sphereAs00.mcncNodeCoordinates*1e3, sphereAs00.mcncNodeDict['sener']*1e-3, axsbig, spec='-.')[-1]
label22 = 'G = '+str(int(sphereAs22.G/1e3))+' kPa, r = '+str(int(sphereAs22.radius*1e3))+' mm'
patches22 = sphereAs22.plotData(sphereAs22.mcncNodeCoordinates*1e3, sphereAs22.mcncNodeDict['sener']*1e-3, axsbig, spec='--')[-1]
legend_patches1 = [patches00[-1], patches22[-1]]
legend_labels1 = [label00, label22]
legend_patches2 = list(patches[-2])
legend_labels2 = [patch.get_label() for patch in patches[-2]]
legend = axsbig.legend(legend_patches1+legend_patches2, legend_labels1+legend_labels2, fontsize=8, frameon=False)
axsbig.set_xlim(0, 8)
axsbig.set_ylim(0, 3)
axsbig.set_xlabel('Location (mm)')
axsbig.set_ylabel('SED (kJ/$m^3$)')
fig.tight_layout()
for label, axes in [['A', axs[0, 0]], ['B', axs[1, 0]], ['C', axs[2, 0]], 
                    ['D', axs[2, 1]], ['E', axs[2, 2]], ['F', axsbig]]:
    if label is not 'F':
        axes.text(-0.4, 1.1, label, transform=axes.transAxes, fontsize=12, fontweight='bold', va='top')
    elif label is 'F':
        axes.text(-0.15, 1.05, label, transform=axes.transAxes, fontsize=12, fontweight='bold', va='top')

fig.savefig('./fig/sener_hs2014.pdf', format='pdf')
fig.savefig('./fig/sener_hs2014.png', format='png', dpi=300)

# plt.show()

# <codecell>

fig = plt.figure(figsize=(4.86, 4.86))
axs = np.empty([3, 3], dtype=object)
axs[0, 0] = fig.add_subplot(331)
axs[1, 0] = fig.add_subplot(334)
axs[2, 0] = fig.add_subplot(337)
axs[2, 1] = fig.add_subplot(338)
axs[2, 2] = fig.add_subplot(339)
gs = gridspec.GridSpec(3, 3)
axsbig = fig.add_subplot(gs[0:2, 1:3])
patches = []
for sphereAs in sphereAsList:
    axes = axs[sphereAs.row, sphereAs.col]
    if axes in axs[:, 0] or axes in axs[-1, :]:
        if axes is axs[0, 0]:
            spec = '-.'
        elif axes is axs[2, 2]:
            spec = '--'
        else:
            spec = '-'
        patches.append(sphereAs.plotData(sphereAs.surfaceCoordinates*1e3, sphereAs.surfaceDeflection*1e3, axes, spec=spec)[1])
        label = 'G = '+str(int(sphereAs.G/1e3))+' kPa\nr = '+str(int(sphereAs.radius*1e3))+' mm'
        axes.text(0.65, 0.7, label, transform=axes.transAxes, ha='center')
        axes.set_ylabel(r'Deflection (mm)')
        axes.set_xlabel('Location (mm)')
        axes.set_xlim(0, 8)
        axes.set_ylim(0, 4)
    if axes is axs[0, 0]:
        sphereAs00 = sphereAs
    elif axes is axs[2, 2]:
        sphereAs22 = sphereAs
label00 = 'G = '+str(int(sphereAs00.G/1e3))+' kPa, r = '+str(int(sphereAs00.radius*1e3))+' mm'
patches00 = sphereAs00.plotData(sphereAs00.surfaceCoordinates*1e3, sphereAs00.surfaceDeflection*1e3, axsbig, spec='-.')[-1]
label22 = 'G = '+str(int(sphereAs22.G/1e3))+' kPa, r = '+str(int(sphereAs22.radius*1e3))+' mm'
patches22 = sphereAs22.plotData(sphereAs22.surfaceCoordinates*1e3, sphereAs22.surfaceDeflection*1e3, axsbig, spec='--')[-1]
legend_patches1 = [patches00[-1], patches22[-1]]
legend_labels1 = [label00, label22]
legend_patches2 = list(patches[-2])
legend_labels2 = [patch.get_label() for patch in patches[-2]]
legend = axsbig.legend(legend_patches1+legend_patches2, legend_labels1+legend_labels2, fontsize=8, frameon=False)
axsbig.set_xlim(0, 10)
axsbig.set_ylim(0, 4)
axsbig.set_xlabel('Location (mm)')
axsbig.set_ylabel('Deflection (mm)')
fig.tight_layout()
for label, axes in [['A', axs[0, 0]], ['B', axs[1, 0]], ['C', axs[2, 0]], 
                    ['D', axs[2, 1]], ['E', axs[2, 2]], ['F', axsbig]]:
    if label is not 'F':
        axes.text(-0.4, 1.1, label, transform=axes.transAxes, fontsize=12, fontweight='bold', va='top')
    elif label is 'F':
        axes.text(-0.15, 1.05, label, transform=axes.transAxes, fontsize=12, fontweight='bold', va='top')

fig.savefig('./fig/deflection_hs2014.pdf', format='pdf')
fig.savefig('./fig/deflection_hs2014.png', format='png', dpi=300)

# plt.show()

# <codecell>

fig, axs = plt.subplots(figsize=(3.27, 3.27))
spec_list = [':', '--', '-.', '-', 'o-']
spec = iter(spec_list)
for sphereAs in sphereAsList:
    if sphereAs.row == 2 or sphereAs.col == 0:
        label = 'G = '+str(int(sphereAs.G/1e3))+' kPa, r = '+str(int(sphereAs.radius*1e3))+' mm'
        axs.plot(sphereAs.timePts, sphereAs.tipForceDisp[:, 0]*1e3, spec.next(), label=label, color='.0')
        axs.set_ylabel(r'Displacement (mm)')
        axs.set_xlabel('Force (N)')
        #axs.set_xlim(0, 1)
        #axs.set_ylim(0, 4)
axs.legend(fontsize=8, loc=4)
fig.tight_layout()
fig.savefig('./fig/compliance_hs2014.pdf', format='pdf')
fig.savefig('./fig/compliance_hs2014.png', format='png', dpi=300)

# plt.show()

# <codecell>


