#!/usr/bin/env python
'''
Try to calculate and plot steric sea level change from E3SM runs

Notes see:
Griffies, S.M., Yin, J., Durack, P.J., Goddard, P., Bates, S.C., Behrens, E., Bentsen, M., Bi, D., Biastoch, A., Böning, C.W., Bozec, A., Chassignet, E., Danabasoglu, G., Danilov, S., Domingues, C.M., Drange, H., Farneti, R., Fernandez, E., Greatbatch, R.J., Holland, D.M., Ilicak, M., Large, W.G., Lorbacher, K., Lu, J., Marsland, S.J., Mishra, A., George Nurser, A.J., Salas y Mélia, D., Palter, J.B., Samuels, B.L., Schröter, J., Schwarzkopf, F.U., Sidorenko, D., Treguier, A.M., Tseng, Y. heng, Tsujino, H., Uotila, P., Valcke, S., Voldoire, A., Wang, Q., Winton, M., Zhang, X., 2014. An assessment of global and regional sea level for years 1993-2007 in a suite of interannual core-II simulations. Ocean Model. 78, 35-89. doi:10.1016/j.ocemod.2014.03.004

Griffies, S.M., Greatbatch, R.J., 2012. Physical processes that impact the evolution of global mean sea level in ocean climate models. Ocean Model. 51, 37-72. doi:10.1016/j.ocemod.2012.04.003


'''

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import netCDF4
import datetime
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from matplotlib import cm
import gsw
from gsw.density import sigma0

# Load MPAS-Ocean base mesh fields needed
#fmesh=netCDF4.Dataset('/project/projectdirs/e3sm/inputdata/ocn/mpas-o/oEC60to30v3wLI/oEC60to30v3wLI60lev.171031.nc') # Cryo
fmesh=netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/oEC60to30v3_60layer.restartFrom_anvil0926.171101.nc') # WC v1
latCell = fmesh.variables['latCell'][:]
lonCell = fmesh.variables['lonCell'][:]
xCell = fmesh.variables['xCell'][:]
yCell = fmesh.variables['yCell'][:]
depths = fmesh.variables['refBottomDepth'][:]
areaCell = fmesh.variables['areaCell'][:]
bottomDepth = fmesh.variables['bottomDepth'][:]
maxLevelCell = fmesh.variables['maxLevelCell'][:]
areaCell = fmesh.variables['areaCell'][:]


# some constants
pii=3.14159
g=9.8101


# ---- Choose run directory ----
# These contain E3SM v1 files downloaded manually from ESGF
path='/project/projectdirs/m3412/simulations/20190819.GMPAS-DIB-IAF-ISMF.T62_oEC60to30v3wLI.cori-knl.testNewGM/archive/ocn/hist'
path='/global/cscratch1/sd/hoffman2/4xc02'
path='/global/cscratch1/sd/hoffman2/SLR_tests/lowres_hist_ens1'
# -------------------------



# ---- Choose spatial extent -----
# Code below adopted from some regional analysis scripts, so there is option to subset the data.
# But for this script would probably be less confusing to drop this.  Leaving for now.
#idx = np.nonzero( (latCell<-50.0/180.0*pii) )[0] # SO
idx = np.nonzero(latCell<99999999999999999)[0] # global ocean


print("Found {} cells in idx".format(len(idx)))

mo=1

# Define rho_0 from e.g. Griffies et al. (2014) Eq. 54.  Results not sensitive to the choice because 
# choices (and impact on results) only vary by ~1%.  Griffies uses 1035.  See Eq. 6.
rho_ref = 1036.0 # typical surface density
#rho_ref = 1026.0 # E3SM rho_sw

def SL(file):
    '''
    Function to calculate sea level for a given file (time slice).
    This is based on the equations in G14 Appendix B.
    Specifically, this function is calculating the local steric tendency, 
    the second term in Eq. 47 and elaborated on in section B.1.2.
    Fundamentally, I am just solving Eq. 55 for two different time periods
    and then taking the difference.
    '''

    SL = np.zeros((len(idx),))
    rho =            file.variables['timeMonthly_avg_density']       [0, :, :]
    layerThickness = file.variables['timeMonthly_avg_layerThickness'][0, :, :]
    ssh = file.variables['timeMonthly_avg_ssh'][0,:]
    pressAdjSSH = file.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
    cnt = 0
    upperOnly = False
    if upperOnly:
      # This option only considers upper water column and avoids dealing with drift in deep ocean
      # This way is much slower to run
      for i in idx:
        maxLev = maxLevelCell[i]
        bottomDepthHere = bottomDepth[i]
        thicknessSum = layerThickness[i, :maxLev].sum()
        thicknessCumSum = layerThickness[i, :maxLev].cumsum()
        zSurf = bottomDepthHere - thicknessSum
        zLayerBot = zSurf - thicknessCumSum
        z = zLayerBot + 0.5 * layerThickness
        k = np.where(zLayerBot > -700.0)[0][-1]
        SL[cnt] = -1.0 / rho_ref * (rho[i, :k+1] * layerThickness[i, :k+1]).sum()
        #print(maxLev, k, zLayerBot.shape)
        if k+1 <= maxLev-1:
         if zLayerBot[k+1] < -700.0:
            # add in partial layer
            SL[cnt] += -1.0 / rho_ref * (rho[i, k+1] * (zLayerBot[k+1] - -700.0))
        cnt += 1
    else:
      # This way considers entire water column. This should be ok if model output is drift-corrected.
      for i in idx:

        maxLev = maxLevelCell[i]
        #SL[cnt] = -1.0 / rho_ref * (rho[i, :maxLev] * layerThickness[i, :maxLev]).sum()
        # Calculate SL as column height above the bottom depth.  Question: Does this differ from G14 Eq. 55
        # which instead subtracts the steric height from the full sea level?  But where do they get 
        # the "full sea level"?  Should that be 'ssh'?
        SL[cnt] = -1.0 / rho_ref * (rho[i, :maxLev] * layerThickness[i, :maxLev]).sum() + bottomDepth[i]

        # Check for unphysical values
        if SL[cnt] > 990:
            print('maxLev=',maxLev,' bottomDepth=',bottomDepth[i], ' nz=', rho.shape, ' SL=',SL[cnt], ' ssh=',ssh[i], ' ssh_adj=',pressAdjSSH[i])
            print('rho:', rho[i,:])

            print('layerThick:', layerThickness[i,:])
            sys.exit()

        # Here complete G14 Eq. 55 by subtracting the steric height from SSH.
        # The pressAdjSSH term is supposed to account for sea ice, but I'm not sure it works correctly.
        # Outside of polar regions this should be right?  This doesn't look right, actually.
        SL[i] = SL[i] + (pressAdjSSH[i] - ssh[i]) * 1035.0/1026.0
        cnt += 1

#    ssh = file.variables['timeMonthly_avg_ssh'][0,:]
#    pressAdjSSH = file.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
#    SL = SL + (pressAdjSSH - ssh) * 1035.0/1026.0
    return SL


# --- Drift correction ---
# In this section, estimate PI drift by taking the difference of two ten year averages.
# The ten year averages were calculated with NCO manually from ten years of monthly averages.
# In papers I've looked at, they don't explain exactly how they do this drift correction.
# Should we be fitting a line to the whole PI time series?  Should we be averaging over more than 10 years?

pipath='/global/cscratch1/sd/hoffman2/SLR_tests/piControl'
yr_pi1=405 #nominal yr
#fpi1=netCDF4.Dataset('{0}/mpaso.hist.am.timeSeriesStatsMonthly.{1:04d}-{2:02d}-01.nc'.format(pipath, yr_pi1, mo), 'r')
fpi1=netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/piControl/0400-0410/mpaso.hist.0400-0410.nc', 'r')
yr_pi2=495 # nominal yr
#fpi2=netCDF4.Dataset('{0}/mpaso.hist.am.timeSeriesStatsMonthly.{1:04d}-{2:02d}-01.nc'.format(pipath, yr_pi2, mo), 'r')
fpi2=netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/piControl/0490-0500/mpaso.hist.0490-0500.nc', 'r')
drift = (SL(fpi2)-SL(fpi1))/(yr_pi2-yr_pi1) # m/yr



# --- Historical SLC ---
# Also using ten year averages calculated offline by NCO.
ens='ens2'
yr= 2000
#f=netCDF4.Dataset('{0}/mpaso.hist.am.timeSeriesStatsMonthly.{1:04d}-{2:02d}-01.nc'.format(path, yr, mo), 'r')
f=netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/lowres_hist_ens/ensMn/mpaso.hist.2000-2009.nc', 'r')
yr_ref = 1900
#fref=netCDF4.Dataset('{0}/mpaso.hist.am.timeSeriesStatsMonthly.{1:04d}-{2:02d}-01.nc'.format(path, yr_ref, 1), 'r')
fref=netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/lowres_hist_ens/ensMn/mpaso.hist.1900-1909.nc', 'r')
SLref = SL(fref)
SLi = SL(f)

# Calculate difference and rate
SLCdiff = (SLi - SLref)
SLCrate = (SLi - SLref) / (yr - yr_ref)


# --- Plots ---

# Plot the steric sea level height (not the change).
# Locally sea level varies by 10s of meters from 0!
# Strong imprinting of continental shelf / bottom depth.
figSL = plt.figure(10, facecolor='w', figsize=(14, 6))
nrow=1
ncol=2
size = 1
ax = figSL.add_subplot(nrow, ncol, 1)
rng=1
plt.scatter(lonCell[idx], latCell[idx], s=size, c=SLref, cmap='RdBu_r')
plt.colorbar()
plt.title('1900 sea level (m)')
ax = figSL.add_subplot(nrow, ncol, 2)
rng=1
plt.scatter(lonCell[idx], latCell[idx], s=size, c=SLi, cmap='RdBu_r')
plt.colorbar()
plt.title('2000 sea level (m)')


# Plot SLC in PI control and historical.
# Things are obviously wrong where there is sea ice.
# But also clearly there is bathymetry imprinting as seen in previous figure.
fig1 = plt.figure(1, facecolor='w', figsize=(14, 6))
nrow=2
ncol=2
ax = fig1.add_subplot(nrow, ncol, 1)
#plt.grid()
size = 4
#plt.scatter(yCell[idx], xCell[idx], s=size, c=SLC)
size = 1
rng=1
plt.scatter(lonCell[idx], latCell[idx], s=size, c=(drift)*1000.0, vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar()
plt.title('PI drift in steric sea\nlevel change (mm/yr)')


ax = fig1.add_subplot(nrow, ncol, 2)
plt.scatter(lonCell[idx], latCell[idx], s=size, c=(SLCrate)*1000.0, vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar()
plt.title('raw steric sea level\nchange (mm/yr), 2000-1900')

ax = fig1.add_subplot(nrow, ncol, 3)
plt.scatter(lonCell[idx], latCell[idx], s=size, c=(SLCrate-drift)*1000.0*(yr - yr_ref), vmin=-100, vmax=100, cmap='RdBu_r')
plt.colorbar()
plt.title('drift-corrected steric sea\nlevel change (mm), 2000-1900')

ax = fig1.add_subplot(nrow, ncol, 4)
plt.scatter(lonCell[idx], latCell[idx], s=size, c=(SLCrate-drift - (SLCrate-drift).mean())*1000.0, vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar()
plt.title('drift-corrected & demeaned steric\nsea level change (mm/yr), 2000-1900')


print("drift mean={}".format((drift*areaCell).mean()/areaCell.mean()*1000))
print("raw SLC mean={}".format((SLCrate*areaCell).mean()/areaCell.mean()*1000))
print("drift-corrected SLC mean={}".format(((SLCrate-drift)*areaCell).mean()/areaCell.mean()*1000))
#axTS.legend()
#plt.colorbar()
plt.draw()
#plt.savefig('foo.png')



# Plot SSH and SSH change.
# I believe this represents dynamic sea level.
# This has nothing to do with steric, but is the other ocean component we want.
# This looks reasonable compared to previous papers.
fig2 = plt.figure(2, facecolor='w', figsize=(14, 6))
nrow=2
ncol=2
rng = 1.0
ax = fig2.add_subplot(nrow, ncol, 1)
ssh = f.variables['timeMonthly_avg_ssh'][0,:]
pressAdjSSH = f.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
plt.scatter(lonCell[idx], latCell[idx], s=size, c=pressAdjSSH, vmin=-2.4, vmax=1.2, cmap='RdBu_r')
plt.colorbar()
plt.title('SSH, 2000-2009 (m)')

ax = fig2.add_subplot(nrow, ncol, 2)
sshRef = fref.variables['timeMonthly_avg_ssh'][0,:]
pressAdjSSHRef = fref.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
plt.scatter(lonCell[idx], latCell[idx], s=size, c=pressAdjSSHRef, vmin=-2.4, vmax=1.2, cmap='RdBu_r')
plt.colorbar()
plt.title('SSH, 1900-1909 (m)')

ax = fig2.add_subplot(nrow, ncol, 3)
rng=0.1
plt.scatter(lonCell[idx], latCell[idx], s=size, c=pressAdjSSH-pressAdjSSHRef, vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar()
plt.title('SSH, difference (m)')


plt.show()
