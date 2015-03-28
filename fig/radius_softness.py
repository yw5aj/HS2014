import numpy as np
import matplotlib.pyplot as plt
import analyses.sphereas
import cPickle

def loadData(radii, Gs, reconstruct=True):
    # radii = np.arange(2e-3, 11e-3, 1e-3)
    # Gs = np.arange(1e4, 10e4, 1e4)
    if reconstruct:
        sphereAsList = analyses.sphereas.init(radii=radii, Gs=Gs)
    # with open('./pickles/sphereAsList.pkl', 'r') as f:
        # sphereAsList = cPickle.load(f)
    return sphereAsList



radii = np.arange(4e-3, 10e-3, 2e-3)
Gs = np.arange(1e4, 10e4, 4e4)
sphereAsList = loadData(radii, Gs)

fig, axs = plt.subplots(len(radii), len(Gs), sharex=True, sharey=True, figsize=(6.83, 6.83))
for sphereAs in sphereAsList:
    axes = axs[sphereAs.row, sphereAs.col]
    sphereAs.plotData(sphereAs.mcncNodeCoordinates*1e3, sphereAs.smoothedMcncNodeDict[
        'sener']*1e-3, axes, spec='-')
    sphereAs.plotData(sphereAs.mcncNodeCoordinates*1e3, sphereAs.mcncNodeDict['sener']*1e-3, axes, spec='-')
    label = 'G = '+str(int(sphereAs.G/1e3))+' kPa\nr = '+str(int(sphereAs.radius*1e3))+' mm'
    axes.text(0.6, 0.6, label, transform=axes.transAxes, ha='center')

for axes in axs[:, 0]:
    axes.set_ylabel(r'SED (kJ/$m^3$)')
for axes in axs[-1, :]:
    axes.set_xlabel('Location (mm)')
    axes.set_xlim(0, 8)
    axes.set_ylim(0, 4)

fig.savefig('./fig/mcnc_stress.pdf', format='pdf')
fig.savefig('./fig/mcnc_stress.png', format='png', dpi=300)



fig, axs = plt.subplots(len(radii), len(Gs), sharex=True, sharey=True, figsize=(6.83, 6.83))
for sphereAs in sphereAsList:
    axes = axs[sphereAs.row, sphereAs.col]
    axs[sphereAs.row, sphereAs.col].plot(sphereAs.timePts, sphereAs.tipForceDisp[:, 0]*1e3, '.-k')
    label = 'G = '+str(int(sphereAs.G/1e3))+' kPa\nr = '+str(int(sphereAs.radius*1e3))+' mm'
    axes.text(0.6, 0.3, label, transform=axes.transAxes, ha='center')

for axes in axs[:, 0]:
    axes.set_ylabel('Disp. (mm)')
for axes in axs[-1, :]:
    axes.set_xlabel('Force (N)')
    # axes.set_xlim((0, 11))
    axes.set_ylim(auto=True)

fig.savefig('./fig/forcedisp.pdf', format='pdf')
fig.savefig('./fig/forcedisp.png', format='png', dpi=300)


fig, axs = plt.subplots(len(radii), len(Gs), sharex=True, sharey=True, figsize=(6.83, 6.83))
for sphereAs in sphereAsList:
    axes = axs[sphereAs.row, sphereAs.col]
    sphereAs.plotData(sphereAs.surfaceCoordinates*1e3, sphereAs.surfaceDeflection*1e3, axes, spec='-')
    label = 'G = '+str(int(sphereAs.G/1e3))+' kPa\nr = '+str(int(sphereAs.radius*1e3))+' mm'
    axes.text(0.65, 0.75, label, transform=axes.transAxes, ha='center')

for axes in axs[:, 0]:
    axes.set_ylabel('Deflection (mm)')
for axes in axs[-1, :]:
    axes.set_xlabel('Location (mm)')
    axes.set_xlim((0, 10))
    axes.set_ylim((0, 4))

fig.savefig('./fig/surface_deflection.pdf', format='pdf')
fig.savefig('./fig/surface_deflection.png', format='png', dpi=300)


# fig, axs = plt.subplots(len(radii), len(Gs), sharex=True, sharey=True, figsize=(6.83, 6.83))
# for sphereAs in sphereAsList:
    # axes = axs[sphereAs.row, sphereAs.col]
    # sphereAs.plotData(sphereAs.mcncNodeCoordinates*1e3, sphereAs.mcncNodeDict[
        # 'stressMinPrincipal']*1e-3, axes, spec='-')
    # label = 'G = '+str(int(sphereAs.G/1e3))+' kPa\nr = '+str(int(sphereAs.radius*1e3))+' mm'
    # axes.text(0.6, 0.6, label, transform=axes.transAxes, ha='center')

# for axes in axs[:, 0]:
    # axes.set_ylabel('Stress (kPa)')
# for axes in axs[-1, :]:
    # axes.set_xlabel('Location (mm)')
    # axes.set_xlim((0, 11))
    # axes.set_ylim(auto=True)

# fig.savefig('./fig/mcnc_stress_raw.pdf', format='pdf')
# fig.savefig('./fig/mcnc_stress_raw.png', format='png', dpi=300)


plt.show()