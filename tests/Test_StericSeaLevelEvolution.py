"""
Name: Test_StericSeaLevelEvolution.py
Author: Sid Bishnu and Matt Hoffman
Details: This script tests the various functions of ../src/StericSeaLevelEvolution.py against the outputs of 
(a) 100-year E3SM runs by Matt, and
(b) 10-year E3SM runs by Sid for z-level and z-star vertical coordinates.
"""


import os
import sys
import netCDF4
sys.path.append(os.path.realpath('..') + '/src/')
from IPython.utils import io
with io.capture_output() as captured:
    import StericSeaLevelEvolution as SSLE
    

def TestComputeStericSeaLevelEvolution():
    # WC v1
    fmesh = (
    netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/oEC60to30v3_60layer.restartFrom_anvil0926.171101.nc'))
    yr_pi1 = 405 # nominal year
    f_pi1 = netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/piControl/0400-0410/mpaso.hist.0400-0410.nc','r')
    yr_pi2 = 495 # nominal year
    f_pi2 = netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/piControl/0490-0500/mpaso.hist.0490-0500.nc','r')
    yr_ref = 1900
    f_ref = netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/lowres_hist_ens/ensMn/mpaso.hist.1900-1909.nc','r')
    yr_i = 2000
    f_i = netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/lowres_hist_ens/ensMn/mpaso.hist.2000-2009.nc','r')
    f = netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/lowres_hist_ens/ensMn/mpaso.hist.2000-2009.nc','r')
    RestrictedColorbars = True # Choose RestrictedColorbars to be True or False.
    SSLE.ComputeStericSeaLevelEvolution(fmesh,yr_pi1,f_pi1,yr_pi2,f_pi2,yr_ref,f_ref,yr_i,f_i,f,
                                        RestrictedColorbars=RestrictedColorbars)
        
        
do_TestComputeStericSeaLevelEvolution = False
if do_TestComputeStericSeaLevelEvolution:
    TestComputeStericSeaLevelEvolution()
    
    
def TestComputeStericSeaLevelEvolutionOnZLevelAndZStarVerticalCoordinates(VerticalCoordinate='zStar'):
    fmesh = netCDF4.Dataset('/global/cfs/cdirs/e3sm/inputdata/ocn/mpas-o/EC30to60E2r2/ocean.EC30to60E2r2.210210.nc',
                            'r')
    if VerticalCoordinate == 'zStar':
        filename_part = 'zstar'
    elif VerticalCoordinate == 'zLevel':
        filename_part = 'zlevel'
    #
    # 10-Year SSLC
    #
    # For 10-year runs, PI drift correction is not applicable.
    #
    yr_ref = 1
    f_ref = netCDF4.Dataset('/global/cscratch1/sd/sbishnu/e3sm_scratch/cori-knl/220505a_GMPAS-IAF_T62_EC30to60E2r2_' 
                            + filename_part + '/run/220505a_GMPAS-IAF_T62_EC30to60E2r2_' + filename_part 
                            + '.mpaso.hist.am.timeSeriesStatsMonthly.0001-01-01.nc','r')
    yr_i = 11
    f_i = netCDF4.Dataset('/global/cscratch1/sd/sbishnu/e3sm_scratch/cori-knl/220505a_GMPAS-IAF_T62_EC30to60E2r2_' 
                          + filename_part + '/run/220505a_GMPAS-IAF_T62_EC30to60E2r2_' + filename_part 
                          + '.mpaso.hist.am.timeSeriesStatsMonthly.0011-01-01.nc','r')
    f = f_i
    RestrictedColorbars = True # Choose RestrictedColorbars to be True or False.
    SSLE.ComputeStericSeaLevelEvolutionOnZLevelAndZStarVerticalCoordinates(
    fmesh,yr_ref,f_ref,yr_i,f_i,f,VerticalCoordinate=VerticalCoordinate,RestrictedColorbars=RestrictedColorbars)
        
        
do_TestComputeStericSeaLevelEvolutionOnZLevelAndZStarVerticalCoordinates = False
if do_TestComputeStericSeaLevelEvolutionOnZLevelAndZStarVerticalCoordinates:
    TestComputeStericSeaLevelEvolutionOnZLevelAndZStarVerticalCoordinates(VerticalCoordinate='zStar')
    TestComputeStericSeaLevelEvolutionOnZLevelAndZStarVerticalCoordinates(VerticalCoordinate='zLevel')