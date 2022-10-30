"""
Name: Test_StericSeaLevelRoutines_Sid.py
Author: Matt Hoffman and Sid Bishnu
Details: This script tests the function ComputeStericSeaLevel in ../src/StericSeaLevelRoutines.py by computing the 
steric contribution to sea level rise using the output of 10-year E3SM runs by Sid for z-level and z-star vertical coordinates.
"""


import os
import sys
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import time
sys.path.append(os.path.realpath('..') + '/src/')
from IPython.utils import io
with io.capture_output() as captured:
    import CommonRoutines as CR
    import StericSeaLevelRoutines as SSLR
    
    
def TestComputeStericSeaLevel(VerticalCoordinate='zStar',RestrictedColorbars=False):
    display_elapsed_time = True
    if display_elapsed_time:
        start_time = time.time()
    if VerticalCoordinate == 'zStar':
        filename_part = 'zstar'
        title_prefix = 'z* Coordinate: '
    elif VerticalCoordinate == 'zLevel':
        filename_part = 'zlevel'
        title_prefix = 'z Coordinate: '
    myGlobalConstants = CR.GlobalConstants()
    # WC v1    
    fmesh = netCDF4.Dataset('/global/cfs/cdirs/e3sm/inputdata/ocn/mpas-o/EC30to60E2r2/ocean.EC30to60E2r2.210210.nc',
                            'r')
    # Load the MPAS-Ocean base mesh fields as needed.
    latCell = fmesh.variables['latCell'][:]*180.0/myGlobalConstants.pii
    lonCell = fmesh.variables['lonCell'][:]*180.0/myGlobalConstants.pii
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
    SSL_ref = SSLR.ComputeStericSeaLevel(fmesh,f_ref)
    SSL_i = SSLR.ComputeStericSeaLevel(fmesh,f_i)
    # Calculate the steric sea level change and the rate of change.
    SSLChange = SSL_i - SSL_ref
    SSLChangeRate = SSLChange/(yr_i - yr_ref)
    #
    # Plots
    #
    output_directory = '../output/'
    labels = ['Longitude (degrees)','Latitude (degrees)']
    labelfontsizes = [17.5,17.5]
    labelpads = [10.0,10.0]
    tickfontsizes = [15.0,15.0]
    nColorBarTicks = 6
    titlefontsize = 22.5
    SaveAsPDF = True
    cbarfontsize = 13.75
    set_xticks_manually = False
    xticks_set_manually = []
    set_yticks_manually = False
    yticks_set_manually = []
    Show = False
    #
    # Plot the steric sea levels in the January of years 1 and 11, the change in these steric sea levels, and the rate 
    # of change.
    #
    plot_type = 'ScatterPlot' # Choose plot_type to be 'ScatterPlot' or 'FilledContourPlot'.
    nRows = 2
    nCols = 2
    nSubPlots = nRows*nCols
    ColorBarLimits = np.zeros((nSubPlots,2))
    if RestrictedColorbars:
        useGivenColorBarLimits = [False,False,True,True]
        ColorBarLimits[2,:] = np.array([-250.0,250.0])
        ColorBarLimits[3,:] = np.array([-25.0,25.0])
    else:
        useGivenColorBarLimits = [False,False,False,False]
    markersizes = [4.0,4.0,4.0,4.0]
    nContours = [300,300,300,300]
    cbarShrinkRatio = 0.65
    titles = [title_prefix + 'Steric Sea\nLevel (m) in Year 1 January',
              title_prefix + 'Steric Sea\nLevel (m) in Year 11 January',
              title_prefix + '\nSteric Sea Level Change (mm),\nYear 11 January - Year 1 January',
              title_prefix + '\nSteric Sea Level Change Rate (mm/yr),\nYear 11 January - Year 1 January']
    FileName = VerticalCoordinate + '_StericSeaLevel_Change_Rate_Year_1_Jan_Year_11_Jan'
    fig_size = [20.0,20.0]
    set_aspect_equal = [False,False,False,False]
    colormaps = [plt.cm.RdBu_r,plt.cm.RdBu_r,plt.cm.RdBu_r,plt.cm.RdBu_r]
    cbarlabelformats = ['%.1f','%.1f','%.1f','%.1f']
    hspace = 0.04 # height of the padding between subplots i.e. the vertical spacing between subplots
    wspace = 0.20 # width of the padding between subplots i.e. the horizontal spacing between subplots
    FigureFormat = 'png'
    bbox_inches = 'tight'
    StericSeaLevels_Change_Rate = np.zeros((nSubPlots,len(SSL_ref)))
    StericSeaLevels_Change_Rate[0,:] = SSL_ref
    StericSeaLevels_Change_Rate[1,:] = SSL_i
    StericSeaLevels_Change_Rate[2,:] = SSLChangeRate*1000.0*(yr_i - yr_ref)
    StericSeaLevels_Change_Rate[3,:] = SSLChangeRate*1000.0
    CR.ScatterAndContourPlotsAsSubPlots(plot_type,output_directory,lonCell,latCell,nRows,nCols,
                                        StericSeaLevels_Change_Rate,markersizes,nContours,labels,labelfontsizes,
                                        labelpads,tickfontsizes,useGivenColorBarLimits,ColorBarLimits,nColorBarTicks,
                                        cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,fig_size,
                                        set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,set_xticks_manually,
                                        xticks_set_manually,set_yticks_manually,yticks_set_manually,hspace,wspace,
                                        FigureFormat,bbox_inches)
    #
    # Plot the demeaned steric sea level change from Year 1 January to Year 11 January, and the rate of change.
    #
    plot_type = 'ScatterPlot' # Choose plot_type to be 'ScatterPlot' or 'FilledContourPlot'.
    nRows = 1
    nCols = 2
    nSubPlots = nRows*nCols
    ColorBarLimits = np.zeros((nSubPlots,2))
    if RestrictedColorbars:
        useGivenColorBarLimits = [True,True]
        ColorBarLimits[0,:] = np.array([-100.0,100.0])
        ColorBarLimits[1,:] = np.array([-10.0,10.0])  
    else:
        useGivenColorBarLimits = [False,False]
    markersizes = [4.0,4.0]
    nContours = [300,300]
    cbarShrinkRatio = 0.65
    titles = [title_prefix + 'Demeaned\nSteric Sea Level Change (mm),\nYear 11 January - Year 1 January',
              title_prefix + 'Demeaned Steric\nSea Level Change Rate (mm/yr),\nYear 11 January - Year 1 January']
    FileName = VerticalCoordinate + '_Demeaned_StericSeaLevelChange_Rate_Year_1_Jan_Year_11_Jan'
    fig_size = [15.0+1.25,7.5]
    set_aspect_equal = [False,False]
    colormaps = [plt.cm.RdBu_r,plt.cm.RdBu_r]
    cbarlabelformats = ['%.1f','%.1f']
    hspace = 0.04 # height of the padding between subplots i.e. the vertical spacing between subplots
    wspace = 0.25 # width of the padding between subplots i.e. the horizontal spacing between subplots
    FigureFormat = 'png'
    bbox_inches = 'tight'
    Demeaned_StericSeaLevelChange_Rate = np.zeros((nSubPlots,len(SSLChangeRate)))
    Demeaned_StericSeaLevelChange_Rate[0,:] = (SSLChangeRate - SSLChangeRate.mean())*1000.0*(yr_i - yr_ref)
    Demeaned_StericSeaLevelChange_Rate[1,:] = (SSLChangeRate - SSLChangeRate.mean())*1000.0
    CR.ScatterAndContourPlotsAsSubPlots(plot_type,output_directory,lonCell,latCell,nRows,nCols,
                                        Demeaned_StericSeaLevelChange_Rate,markersizes,nContours,labels,labelfontsizes,
                                        labelpads,tickfontsizes,useGivenColorBarLimits,ColorBarLimits,nColorBarTicks,
                                        cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,fig_size,
                                        set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,set_xticks_manually,
                                        xticks_set_manually,set_yticks_manually,yticks_set_manually,hspace,wspace,
                                        FigureFormat,bbox_inches)
    #
    # We finally plot the pressure-adjusted SSH and the difference between its annual mean across a decade. We 
    # believe this represents the dynamic sea level. It has nothing to do with steric, but is the other ocean component 
    # we want.
    #
    f = f_i
    PressureAdjustedSSH = f.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
    PressureAdjustedSSHRef = f_ref.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
    plot_type = 'ScatterPlot' # Choose plot_type to be 'ScatterPlot' or 'FilledContourPlot'.
    nSubPlots = 3
    ColorBarLimits = np.zeros((nSubPlots,2))
    if RestrictedColorbars:
        useGivenColorBarLimits = [True,True,True]
        ColorBarLimits[0,:] = np.array([-1.5,1.5])
        ColorBarLimits[1,:] = np.array([-1.5,1.5])
        ColorBarLimits[2,:] = np.array([-0.6,0.6])
    else:
        useGivenColorBarLimits = [False,False,False]
    markersizes = [4.0,4.0,4.0]
    nContours = [300,300,300]
    cbarShrinkRatio = 0.65
    titles = [title_prefix + 'Pressure Adjusted SSH (m)\nin Year 1 January',
              title_prefix + 'Pressure Adjusted SSH (m)\nin Year 11 January',
              title_prefix + 'Difference in Pressure Adjusted SSH (m),\nYear 11 January - Year 1 January']
    FileName = VerticalCoordinate + '_PressureAdjustedSSH_Difference_Year_1_Jan_Year_11_Jan'
    fig_size = [20.0,20.0]
    set_aspect_equal = [False,False,False]
    colormaps = [plt.cm.RdBu_r,plt.cm.RdBu_r,plt.cm.RdBu_r]
    cbarlabelformats = ['%.1f','%.1f','%.1f']
    hspace = 0.05 # height of the padding between subplots i.e. the vertical spacing between subplots
    wspace = 0.50 # width of the padding between subplots i.e. the horizontal spacing between subplots
    FigureFormat = 'png'
    bbox_inches = 'tight'
    PressureAdjustedSSH_1900_2000 = np.zeros((nSubPlots,len(PressureAdjustedSSH)))
    PressureAdjustedSSH_1900_2000[0,:] = PressureAdjustedSSH
    PressureAdjustedSSH_1900_2000[1,:] = PressureAdjustedSSHRef
    PressureAdjustedSSH_1900_2000[2,:] = PressureAdjustedSSH - PressureAdjustedSSHRef
    CR.ScatterAndContourPlotsAs3SubPlots(plot_type,output_directory,lonCell,latCell,PressureAdjustedSSH_1900_2000,
                                         markersizes,nContours,labels,labelfontsizes,labelpads,tickfontsizes,
                                         useGivenColorBarLimits,ColorBarLimits,nColorBarTicks,cbarShrinkRatio,titles,
                                         titlefontsize,SaveAsPDF,FileName,Show,fig_size,set_aspect_equal,colormaps,
                                         cbarlabelformats,cbarfontsize,set_xticks_manually,xticks_set_manually,
                                         set_yticks_manually,yticks_set_manually,hspace,wspace,FigureFormat,bbox_inches)
    if display_elapsed_time:
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_minutes = np.floor(elapsed_time/60.0)
        elapsed_time_seconds = np.mod(elapsed_time,60.0)
        print('The elapsed time is %d minutes %d seconds.' %(elapsed_time_minutes,elapsed_time_seconds))
    
    
TestComputeStericSeaLevel(VerticalCoordinate='zStar',RestrictedColorbars=False)
TestComputeStericSeaLevel(VerticalCoordinate='zLevel',RestrictedColorbars=False)