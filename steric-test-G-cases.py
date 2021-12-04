#!/usr/bin/env python
'''
Script to compare some scalar values from different runs of Thwaites melt variability experiment.
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

fmesh=netCDF4.Dataset('/project/projectdirs/e3sm/inputdata/ocn/mpas-o/oEC60to30v3wLI/oEC60to30v3wLI60lev.171031.nc') # Cryo
#fmesh=netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/oEC60to30v3_60layer.restartFrom_anvil0926.171101.nc') # WC v1
latCell = fmesh.variables['latCell'][:]
lonCell = fmesh.variables['lonCell'][:]
xCell = fmesh.variables['xCell'][:]
yCell = fmesh.variables['yCell'][:]
depths = fmesh.variables['refBottomDepth'][:]
areaCell = fmesh.variables['areaCell'][:]
bottomDepth = fmesh.variables['bottomDepth'][:]
maxLevelCell = fmesh.variables['maxLevelCell'][:]
areaCell = fmesh.variables['areaCell'][:]


pii=3.14159
g=9.8101


# ---- Choose time(s) -----
#yrs=(10, 30, 50, 60, 70,80, 90, 100, 150)
#yrs=(10, 30, 50, 60, 70,80, 90, 100, 100)
#yrs=np.arange(1,150,1)
yrs=np.arange(1,120,2)

#yrs=(50, 50, 50, 60, 70,80, 90, 100, 150)
#yrs = np.arange(95,102,1)
mos=(1,)

mo=1
#mos=np.arange(1,13,1)
# -------------------------




# ---- Choose spatial extent -----
#idx = np.nonzero(np.logical_and(np.logical_and(latCell<-70.0/180.0*pii, latCell>-85.0/180.0*pii), np.logical_and(lonCell>300.0/360.0*2.0*pii, lonCell<350.0/360.0*2*pii)))[0]  #entire weddell
#idx = np.nonzero(np.logical_and(np.logical_and(latCell<-70.0/180.0*pii, latCell>-85.0/180.0*pii), np.logical_and(lonCell>270.0/360.0*2.0*pii, lonCell<350.0/360.0*2*pii)))[0]  #entire weddell wider
#idx = np.nonzero( (latCell<-60.0/180.0*pii) * (latCell>-85.0/180.0*pii) * np.logical_or(lonCell>280.0/360.0*2.0*pii, lonCell<80.0/360.0*2*pii))[0]; size=1.4; fsz=(15,9)  # weddell to Amery 
idx = np.nonzero( (latCell<-50.0/180.0*pii) )[0] # SO

idx = np.nonzero(latCell<99999999999999999)[0]


print("Found {} cells in idx".format(len(idx)))

mo=1
rho_ref = 1036.0 # typical surface density
#rho_ref = 1026.0 # E3SM rho_sw

def SL(file):
    rho =            file.variables['timeMonthly_avg_density']       [0, :, :]
    layerThickness = file.variables['timeMonthly_avg_layerThickness'][0, :, :]
    ssh = file.variables['timeMonthly_avg_ssh'][0,:]
    pressAdjSSH = file.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
    nCells = len(file.dimensions['nCells'])
    SL = np.zeros((nCells,))
    SLv = np.zeros((nCells,))
    ht = np.zeros((nCells,))
    cnt = 0
    upperOnly = False
    if upperOnly:
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
      for i in idx:

        maxLev = maxLevelCell[i]
        #SL[cnt] = -1.0 / rho_ref * (rho[i, :maxLev] * layerThickness[i, :maxLev]).sum()
        SL[i] = -1.0 / rho_ref * (rho[i, :maxLev] * layerThickness[i, :maxLev]).sum() + bottomDepth[i]
        SLv[i] = (rho_ref/rho[i, :maxLev] * layerThickness[i, :maxLev]).sum() - bottomDepth[i]
        ht[i] = layerThickness[i, :maxLev].sum() - bottomDepth[i]
#        if SL[cnt] > 990:
#            print('maxLev=',maxLev,' bottomDepth=',bottomDepth[i], ' nz=', rho.shape, ' SL=',SL[cnt], ' ssh=',ssh[i], ' ssh_adj=',pressAdjSSH[i])
#            print('rho:', rho[i,:])
#
#            print('layerThick:', layerThickness[i,:])
#            sys.exit()

        #SL[i] = SL[i] - 1.0/rho_ref * (pressAdjSSH[i] - ssh[i]) * 1035.0/1026.0 * rho[i,0]
        SL[i] = SL[i] - 1.0/rho_ref * (pressAdjSSH[i] - ssh[i]) * 1026.0
        SLv[i] = SLv[i] +(pressAdjSSH[i] - ssh[i]) * 1035.0/1026.0 * rho_ref/rho[i,0]
        ht[i] = ht[i] + (pressAdjSSH[i] - ssh[i]) * 1035.0/1026.0
        cnt += 1

#    ssh = file.variables['timeMonthly_avg_ssh'][0,:]
#    pressAdjSSH = file.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
#    SL = SL + (pressAdjSSH - ssh) * 1035.0/1026.0
    return SL, SLv, ht


yrs='0120-0129'
f1=netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/Cryo-G-cases/noEAmelt/mpaso.hist.{}.nc'.format(yrs), 'r')
f2=netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/Cryo-G-cases/ISMF/mpaso.hist.{}.nc'.format(yrs), 'r')
SL1, SLv1, ht1 = SL(f1)
SL2, SLv2, ht2 = SL(f2)

SLCdiff = (SL2 - SL1)
size = 1

figSL = plt.figure(10, facecolor='w', figsize=(14, 6))
nrow=1
ncol=3

idx = np.nonzero( (latCell<-50.0/180.0*pii) )[0] # SO
ax = figSL.add_subplot(nrow, ncol, 1)
rng=10
#plt.scatter(lonCell[idx], latCell[idx], s=size, c=SL1[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.scatter(yCell[idx], xCell[idx], s=size, c=SL1[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar()
plt.title('SL1 (m)')
ax.axis('equal'); plt.axis('off')
  
ax = figSL.add_subplot(nrow, ncol, 2)
#plt.scatter(lonCell[idx], latCell[idx], s=size, c=SL2[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.scatter(yCell[idx], xCell[idx], s=size, c=SL2[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar()
plt.title('SL2 (m)')
ax.axis('equal'); plt.axis('off')
  
ax = figSL.add_subplot(nrow, ncol, 3)
rng=0.25
plt.scatter(yCell[idx], xCell[idx], s=size, c=SLCdiff[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar(shrink=.3)
plt.title('SL diff (m)')
ax.axis('equal'); plt.axis('off')
  



figSLv = plt.figure(12, facecolor='w', figsize=(14, 6))
nrow=1
ncol=3

idx = np.nonzero( (latCell<-50.0/180.0*pii) )[0] # SO
ax = figSLv.add_subplot(nrow, ncol, 1)
rng=10
#plt.scatter(lonCell[idx], latCell[idx], s=size, c=SL1[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.scatter(yCell[idx], xCell[idx], s=size, c=SLv1[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar()
plt.title('SLv1 (m)')
ax.axis('equal'); plt.axis('off')
  
ax = figSLv.add_subplot(nrow, ncol, 2)
#plt.scatter(lonCell[idx], latCell[idx], s=size, c=SL2[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.scatter(yCell[idx], xCell[idx], s=size, c=SLv2[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar()
plt.title('SLv2 (m)')
ax.axis('equal'); plt.axis('off')
  
ax = figSLv.add_subplot(nrow, ncol, 3)
rng=0.25
plt.scatter(yCell[idx], xCell[idx], s=size, c=SLv2[idx]-SLv1[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar(shrink=.3)
plt.title('SLv diff (m)')
ax.axis('equal'); plt.axis('off')
 
   
fight = plt.figure(11, facecolor='w', figsize=(14, 6))
nrow=1
ncol=3

idx = np.nonzero( (latCell<-50.0/180.0*pii) )[0] # SO
ax = fight.add_subplot(nrow, ncol, 1)
rng=3
plt.scatter(yCell[idx], xCell[idx], s=size, c=ht1[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar()
plt.title('ht1 (m)')
ax.axis('equal'); plt.axis('off')
  
ax = fight.add_subplot(nrow, ncol, 2)
#plt.scatter(lonCell[idx], latCell[idx], s=size, c=SL2[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.scatter(yCell[idx], xCell[idx], s=size, c=ht2[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar()
plt.title('ht2 (m)')
ax.axis('equal'); plt.axis('off')
  
ax = fight.add_subplot(nrow, ncol, 3)
rng=0.25
plt.scatter(yCell[idx], xCell[idx], s=size, c=ht2[idx]-ht1[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar(shrink=.3)
plt.title('ht diff (m)')
ax.axis('equal'); plt.axis('off')
 





SSH = f1.variables['timeMonthly_avg_ssh'][0,:]
pressAdjSSH = f1.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
pressAdjSSH2= f2.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
#ax = fig2.add_subplot(nrow, ncol, 1)
#plt.scatter(lonCell[idx], latCell[idx], s=size, c=pressAdjSSH, vmin=-2, vmax=2, cmap='RdBu_r')
#plt.colorbar()
#plt.title('pressAdjSSH (m)')
#
#ax = fig2.add_subplot(nrow, ncol, 2)
#plt.scatter(lonCell[idx], latCell[idx], s=size, c=SSH, vmin=-2, vmax=2, cmap='RdBu_r')
#plt.colorbar()
#plt.title('SSH (m)')
#
#ax = fig2.add_subplot(nrow, ncol, 3)
#plt.scatter(lonCell[idx], latCell[idx], s=size, c=pressAdjSSH-SSH, vmin=-2, vmax=2, cmap='RdBu_r')
#plt.colorbar()
#plt.title('diff (m)')
#


# SO diffs
idx = np.nonzero( (latCell<-50.0/180.0*pii) )[0] # SO
fig2 = plt.figure(2, facecolor='w', figsize=(14, 6))
nrow=1
ncol=2

ax = fig2.add_subplot(nrow, ncol, 1)
rng=0.25
plt.scatter(yCell[idx], xCell[idx], s=size, c=SLCdiff[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
#plt.scatter(yCell[idx], xCell[idx], s=size, c=SLCdiff[idx], vmin=-0.035, vmax=-0.005, cmap='turbo')
plt.colorbar(shrink=.3)
plt.title('steric SL diff (m)')
ax.axis('equal'); plt.axis('off')
  
   
ax = fig2.add_subplot(nrow, ncol, 2)
rng=0.1
#plt.scatter(lonCell[idx], latCell[idx], s=size, c=pressAdjSSH2-pressAdjSSHRef, vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.scatter(yCell[idx], xCell[idx], s=size, c=pressAdjSSH2[idx]-pressAdjSSH[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
ax.axis('equal'); plt.axis('off')
plt.colorbar(shrink=.3)
plt.title('SSH diff (m)')


# SO diffs - remove global trend
idx = np.nonzero( (latCell<-50.0/180.0*pii) )[0] # SO
fig4 = plt.figure(4, facecolor='w', figsize=(14, 6))
nrow=1
ncol=2

ax = fig4.add_subplot(nrow, ncol, 1)
rng=0.25
plt.scatter(yCell[idx], xCell[idx], s=size, c=SLCdiff[idx] - SLCdiff[~idx].mean(), vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.scatter(yCell[idx], xCell[idx], s=size, c=SLCdiff[idx], cmap='turbo')
plt.colorbar(shrink=.3)
plt.title('steric SL diff (m)')
ax.axis('equal'); plt.axis('off')
  
   
ax = fig4.add_subplot(nrow, ncol, 2)
rng=0.1
plt.scatter(yCell[idx], xCell[idx], s=size, c=pressAdjSSH2[idx]-pressAdjSSH[idx] - (pressAdjSSH2[~idx]-pressAdjSSH[~idx]).mean(), vmin=-rng, vmax=rng, cmap='RdBu_r')
ax.axis('equal'); plt.axis('off')
plt.colorbar(shrink=.3)
plt.title('SSH diff (m)')



# plot global
idx = np.nonzero(latCell<99999999999999999)[0]
fig3 = plt.figure(3, facecolor='w', figsize=(14, 6))
nrow=1
ncol=2

ax = fig3.add_subplot(nrow, ncol, 1)
rng=0.25
plt.scatter(lonCell[idx], latCell[idx], s=size, c=SLCdiff[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.colorbar(shrink=.3)
plt.title('steric SL diff (m)')
ax.axis('equal'); plt.axis('off')
  
   
ax = fig3.add_subplot(nrow, ncol, 2)
rng=0.1
#plt.scatter(lonCell[idx], latCell[idx], s=size, c=pressAdjSSH2-pressAdjSSHRef, vmin=-rng, vmax=rng, cmap='RdBu_r')
plt.scatter(lonCell[idx], latCell[idx], s=size, c=pressAdjSSH2[idx]-pressAdjSSH[idx], vmin=-rng, vmax=rng, cmap='RdBu_r')
ax.axis('equal'); plt.axis('off')
plt.colorbar(shrink=.3)
plt.title('SSH diff (m)')



plt.show()
