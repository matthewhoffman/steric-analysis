"""
Name: StericSeaLevelRoutines.py
Authors: Matt Hoffman and Sid Bishnu
Details: This script calculates and plots steric sea level change from E3SM runs.

References:

Griffies, S.M., Yin, J., Durack, P.J., Goddard, P., Bates, S.C., Behrens, E., Bentsen, M., Bi, D., Biastoch, A., 
Böning, C.W., Bozec, A., Chassignet, E., Danabasoglu, G., Danilov, S., Domingues, C.M., Drange, H., Farneti, R., 
Fernandez, E., Greatbatch, R.J., Holland, D.M., Ilicak, M., Large, W.G., Lorbacher, K., Lu, J., Marsland, S.J., Mishra, 
A., George Nurser, A.J., Salas y Mélia, D., Palter, J.B., Samuels, B.L., Schröter, J., Schwarzkopf, F.U., Sidorenko, D.,
Treguier, A.M., Tseng, Y. heng, Tsujino, H., Uotila, P., Valcke, S., Voldoire, A., Wang, Q., Winton, M., Zhang, X., 
2014. An assessment of global and regional sea level for years 1993-2007 in a suite of interannual core-II simulations. 
Ocean Model. 78, 35-89. doi:10.1016/j.ocemod.2014.03.004

Griffies, S.M., Greatbatch, R.J., 2012. Physical processes that impact the evolution of global mean sea level in ocean 
climate models. Ocean Model. 51, 37-72. doi:10.1016/j.ocemod.2012.04.003
"""


import os
import sys
import numpy as np
sys.path.append(os.path.realpath('..') + '/src/')
from IPython.utils import io
with io.capture_output() as captured:
    import CommonRoutines as CR


def ComputeStericSeaLevel(fmesh,file):
    """
    This function determines the sea level for a given file (time slice). It is based on the equations in Appendix B of
    the Griffies 2014 paper. Specifically, this function calculates the local steric tendency, the second term in Eq. 47
    and elaborated on in section B.1.2. Fundamentally, I am just solving Eq. 55 for two different time periods, and then
    taking the difference.
    """
    myGlobalConstants = CR.GlobalConstants()
    rho_ref = myGlobalConstants.rho_ref
    # Load the MPAS-Ocean base mesh fields as needed.
    latCell = fmesh.variables['latCell'][:]
    bottomDepth = fmesh.variables['bottomDepth'][:]
    maxLevelCell = fmesh.variables['maxLevelCell'][:]
    # Choose the spatial extent. The code below is adopted from some regional analysis scripts. So, we have the option 
    # to subset the data. But for this script, it would probably be less confusing to drop it. So, we are leaving it 
    # for now.
    idx = np.nonzero(latCell<99999999999999999)[0] # global ocean
    EchoNumberOfCells = False
    if EchoNumberOfCells:
        print("Found {} cells in idx." .format(len(idx)))
    StericSeaLevel = np.zeros(len(idx))
    rho = file.variables['timeMonthly_avg_density'][0,:, :]
    layerThickness = file.variables['timeMonthly_avg_layerThickness'][0,:,:]
    ssh = file.variables['timeMonthly_avg_ssh'][0,:]
    PressureAdjustedSSH = file.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
    cnt = 0
    upperOnly = False
    if upperOnly:
        z0 = -700.0
        # This option only considers the upper water column above the z = z0 isobath, and avoids dealing with drift in 
        # the deep ocean. This way is much slower to run.
        for i in idx:
            maxLevel = maxLevelCell[i]
            bottomDepthHere = bottomDepth[i]
            thicknessSum = layerThickness[i,0:maxLevel].sum()
            thicknessCumSum = layerThickness[i,0:maxLevel].cumsum()
            # thicknessCumSum is the array consisting of the layer thickness of the first layer, the sum of the layer 
            # thicknesses of the first and the second layer, the sum of the layer thicknesses of the first, second, and
            # third layers, and so on.
            zSurf = thicknessSum - bottomDepthHere
            zLayerBot = zSurf - thicknessCumSum # zLayerBot is the depth of the bottom of every layer.
            z = zLayerBot + 0.5*layerThickness # z is the depth of the (vertical) center of every layer.
            k = np.where(zLayerBot > z0)[0][-1] 
            # np.where(condition,[x,y]) yields x when condition is True, and y otherwise. The output is [ndarray or 
            # tuple of ndarrays]. If both x and y are specified, the output array contains elements of x where 
            # condition is True, and elements from y elsewhere. For example, if a = np.arange(10) i.e.
            # a = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), then np.where(a < 5, a, 10*a) yields 
            # np.array([ 0,  1,  2,  3,  4, 50, 60, 70, 80, 90]). In our case, np.where(zLayerBot > z0)[0] represents 
            # the array of layers whose bottom depth is above z = z0, and k represents the last index of that array. 
            # So, the z = z0 m isobath passes through the layer with index k + 1.
            StericSeaLevel[cnt] = -1.0/rho_ref*(rho[i,0:k+1]*layerThickness[i,0:k+1]).sum()
            if k + 1 <= maxLevel - 1: 
            # if the layer straddling the z = z0 isobath coincides with or overlies the lowermost layer of water right
            # above the bottom topography
                if zLayerBot[k+1] <= z0:
                # if the z = z0 isobath overlies or coincides with the bottom depth of the layer straddling the isobath
                    StericSeaLevel[cnt] += -1.0/rho_ref*(rho[i,k+1]*(z0 - zLayerBot[k])) 
                    # Add in the partial or the entire layer.
            cnt += 1
    else:
        # This way considers the entire water column. This should be fine if the model output is drift-corrected.
        StericSeaLevel_UnphysicalValues_LowerLimit = 990.0
        for i in idx:
            maxLevel = maxLevelCell[i]
            StericSeaLevel[cnt] = -1.0/rho_ref*(rho[i,0:maxLevel]*layerThickness[i,0:maxLevel]).sum()
            # Check for unphysical values.
            if StericSeaLevel[cnt] > StericSeaLevel_UnphysicalValues_LowerLimit:
                print('i = ', i, ', cnt = ', cnt)
                print('maxLevel = ', maxLevel, ', bottomDepth = ', bottomDepth[i], ', nz = ', rho.shape[1], 
                      ', StericSeaLevel = ', StericSeaLevel[cnt], ', ssh = ', ssh[i], ', ssh_adj = ', 
                      PressureAdjustedSSH[i])
                print('rho[i,:] = ', rho[i,:])
                print('layerThickness[i,:] = ', layerThickness[i,:])
                sys.exit()
            # We now take into consideration, the depression due to sea-ice loading in the steric contribution to SSH.
            StericSeaLevel[i] += -1.0/rho_ref*rho[i,0]*(PressureAdjustedSSH[i] - ssh[i])
            cnt += 1
    return StericSeaLevel