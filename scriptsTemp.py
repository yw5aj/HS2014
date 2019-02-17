# cd into that folder
import os
os.chdir('HS2014')

# Test the simclass
import sim.simclass
sphereAs1 = sim.simclass.SphereAs(radius=1e-3, G=1e13, overwrite=True)

reload(sim.simclass)
sphereAs2 = sim.simclass.SphereAs(radius=1e-3, G=1e13, overwrite=True)

# Fit surface deflection
import createmodel.setfit
createmodel.setfit.buildAll()

import fitmodel.deflection
fitmodel.deflection.exhaust('ps_rigid_d317_tip')
fitmodel.deflection.exhaust('ps_rigid_d952_tip')

import fitmodel.magnitude
fitmodel.magnitude.autoOptimize()
        
# Run all the final fit
import fitmodel.runfinalfit
fitmodel.runfinalfit.runMagnitudeFit()
fitmodel.runfinalfit.runDeflectionFit()


# Test model creation
import createmodel.softtip
createmodel.softtip.buildAsSphere(radius=1e-3, G=1e4)
createmodel.softtip.buildAsSphere(radius=1e-2, G=1e4)


# This is to run all models
import cPickle
import sim.sphereas
reload(sim.sphereas)
sphereAsList = sim.sphereas.init(overwrite=False)
sim.sphereas.run(sphereAsList)
# with open('./sim/pickles/sphereAsList.pkl', 'r') as f:
    # sphereAsList = cPickle.load(f)
sim.sphereas.analyze(sphereAsList)



# To perfrom unit tests before running all models
import sim.sphereas
reload(sim.sphereas)
sim.sphereas.unittest(G=5e4, radius=6e-3, fakeRun=False)# To perform unit tests before running all models

import fitmodel.runjohnsonbar
reload(fitmodel.runjohnsonbar)
fitmodel.runjohnsonbar.runJohnsonBar(width=3e-3)
