#!/usr/bin/env python2.7
# Create dictionary of seismic synthetics - to be run in examples folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir  = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import numpy as np
import seispy.GeologicalModelling as GM
import seispy.SeismicModelling2D  as SM


def Create_Seismic_Dictionary(directory = 'datasets/seismic/synthetics/', models = ['flat','dip','wedge','fault','trap'], nsubmodels = 5000, moddims = [100, 100], norm_seismic = 6e12):
    """
    Create dictionary of seismic files
    :param models: 	        Name of directory where to save files
    :param models: 	        Name of models to be created
    :param nsubmodels: 	    Number of models for each type
    :param moddims: 	    Dimensions of models
    :param norm_seismic:    Normalization factor
    """

    savemod = False


    # directories
    filepath = os.path.join(parentdir, directory)
    filename = 'dict'

    # create directories
    if not os.path.isdir(filepath):
        os.mkdir(filepath)

    for model in models:
        if not os.path.isdir(filepath + model + '/'):
            os.mkdir(filepath+model+'/')



    # create data
    nsubmodels        = nsubmodels*np.ones(len(models),dtype=np.int)
    nsubmodels_sum    = np.sum(nsubmodels)
    nsubmodels_cumsum = np.cumsum(nsubmodels)

    for imod in range(nsubmodels_sum):

        if imod<nsubmodels_cumsum[0]:

            # Make stochastic layered models
            print('layer '+str(imod))
            dv   = [1500, 2000]
            drho = [1000, 1800]
            nint = 3
            dint = [20, 80]

            GeoMod = GM.LayeredModel({'dims': moddims, 'type': 'layer'})
            GeoMod.Stochastic(nint, dv, drho, dint=dint)
            GeoMod.Apply()

        elif imod<nsubmodels_cumsum[1]:

            # Make stochastic dipping models
            print('dip '+str(imod))
            vback   = [1500, 1800]
            rhoback = [1000, 1200]
            nint    = 3
            dint    = [20, 80]
            p       = [0.1, 0.2]
            dv      = [-400, 400]
            drho    = [-600, 600]

            GeoMod = GM.DippingModel({'dims': moddims, 'type': 'dipping'})
            GeoMod.Stochastic(nint, p, vback, dv, rhoback, drho, dint=dint, flip=True)
            GeoMod.Apply()

        elif imod<nsubmodels_cumsum[2]:

            # Make stochastic wedge models
            print('wedge '+str(imod))
            vback   = [1500, 1800]
            rhoback = [1000, 1200]
            p       = [0.2, 0.4]
            dv      = [-400, 400]
            drho    = [-600, 600]

            GeoMod = GM.WedgeModel({'dims': moddims, 'type': 'dipping'})
            GeoMod.Stochastic(p, vback, dv, rhoback, drho, flip=True)
            GeoMod.Apply()

        elif imod<nsubmodels_cumsum[3]:

            # Make stochastic fault models
            print('fault ' + str(imod))
            dv   = [1500, 2000]
            drho = [1000, 1800]
            dfaultlim = [40, 60]
            nint = 3
            dint = [20, 80]
            doffset = [10,20]

            GeoMod = GM.FaultModel({'dims': moddims, 'type': 'layer'})
            GeoMod.Stochastic(nint, dv, drho, dint=dint, dfaultlim=dfaultlim, doffset=doffset)
            GeoMod.Apply()

        elif imod<nsubmodels_cumsum[4]:

            # Make stochastic trap models
            print('trap ' + str(imod))
            perc = 0
            nint = 1
            center_x = 50
            dcenter_z = [80, 110]
            dv = [1500, 2000]
            drho = [1000, 1800]

            GeoMod = GM.TrapModel({'dims': moddims, 'type': 'trap'})
            GeoMod.Stochastic(nint, center_x, dcenter_z, dv, drho, perc=0)
            GeoMod.Apply()



        # Create seismic stack
        Seismod = SM.SeismicModelling2D({'V'      : GeoMod.V,
                                         'Rho'    : GeoMod.Rho,
                                         'dt'     : 0.004,
                                         'ot'     : 0,
                                         'ntrick' : 31,
                                         'f0'     : 10})

        Seismod.Apply()
        #Seismod.Visualize(cbarlims=[-4e12,4e12])


        # Save seismic data in subfolders
        if imod<nsubmodels_cumsum[0]:
            if savemod==True: GeoMod.Save( filepath=filepath+models[0]+'/', filename=filename + str(imod), normV=3000, normRho=3000)
            Seismod.Save(filepath=filepath+models[0]+'/', filename=filename + str(imod), norm=norm_seismic)

        elif imod<nsubmodels_cumsum[1]:
            if savemod == True: GeoMod.Save( filepath=filepath+models[1]+'/', filename=filename + str(imod), normV=3000, normRho=3000)
            Seismod.Save(filepath=filepath+models[1]+'/', filename=filename + str(imod), norm=norm_seismic)

        elif imod < nsubmodels_cumsum[2]:
            if savemod == True: GeoMod.Save( filepath=filepath+models[2]+'/', filename=filename + str(imod), normV=3000, normRho=3000)
            Seismod.Save(filepath=filepath+models[2]+'/', filename=filename + str(imod), norm=norm_seismic)

        elif imod<nsubmodels_cumsum[3]:
            if savemod == True: GeoMod.Save( filepath=filepath+models[3]+'/', filename=filename + str(imod), normV=3000, normRho=3000)
            Seismod.Save(filepath=filepath+models[3]+'/', filename=filename + str(imod), norm=norm_seismic)

        elif imod < nsubmodels_cumsum[4]:
            if savemod == True: GeoMod.Save( filepath=filepath+models[4]+'/', filename=filename + str(imod), normV=3000, normRho=3000)
            Seismod.Save(filepath=filepath+models[4]+'/', filename=filename + str(imod), norm=norm_seismic)



        #imgpng = sp.imread(filepath+filename+str(imod)+'_stack.png', flatten=True)
        #plt.figure()
        #plt.imshow(imgpng, cmap='gray',vmin=0, vmax=255)

    #plt.show()



if __name__ == "__main__":
    Create_Seismic_Dictionary()
