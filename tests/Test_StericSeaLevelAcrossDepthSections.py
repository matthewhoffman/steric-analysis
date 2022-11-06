"""
Name: Test_StericSeaLevelAcrossDepthSections.py
Author: Sid Bishnu
Details: This script tests the various functions of ../StericSeaLevelAcrossDepthSections.py against the output of 
100-year E3SM runs by Matt.
"""


import os
import sys
import numpy as np
import netCDF4
sys.path.append(os.path.realpath('..') + '/src/')
from IPython.utils import io
with io.capture_output() as captured:
    import StericSeaLevelAcrossDepthSections as SSLADS
    
    
def TestComputeStericSeaLevelAcrossDepthSections():
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
    z0Array = np.array([-200.0,-500.0,-1000.0,-2000.0])
    # Divide the ocean depth into five sections, and specify the elements of z0Array to the depth of the bottom of the 
    # upper four sections.
    RestrictedColorbars = True # Choose RestrictedColorbars to be True or False.
    SSLADS.ComputeStericSeaLevelAcrossDepthSections(fmesh,yr_pi1,f_pi1,yr_pi2,f_pi2,yr_ref,f_ref,yr_i,f_i,z0Array,
                                                    RestrictedColorbars=RestrictedColorbars)
        
        
do_TestComputeStericSeaLevelAcrossDepthSections = False
if do_TestComputeStericSeaLevelAcrossDepthSections:
    TestComputeStericSeaLevelAcrossDepthSections()