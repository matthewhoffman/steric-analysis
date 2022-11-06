"""
Name: StericSeaLevelAcrossDepthSections.py
Author: Sid Bishnu
Details: This script computes the steric contribution to sea level rise arising from various sections of the ocean 
depth.
"""


import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
sys.path.append(os.path.realpath('..') + '/src/')
from IPython.utils import io
with io.capture_output() as captured:
    import CommonRoutines as CR
    import StericSeaLevel as SSL
    
    
def ComputeStericSeaLevelAcrossDepthSections(fmesh,yr_pi1,f_pi1,yr_pi2,f_pi2,yr_ref,f_ref,yr_i,f_i,z0Array,
                                             RestrictedColorbars=False,display_elapsed_time_within_loop=True,
                                             display_elapsed_time=True):
    if display_elapsed_time:
        start_time = time.time()
    myGlobalConstants = CR.GlobalConstants()
    # Load the MPAS-Ocean base mesh fields as needed.
    latCell = fmesh.variables['latCell'][:]*180.0/myGlobalConstants.pii
    lonCell = fmesh.variables['lonCell'][:]*180.0/myGlobalConstants.pii
    Title_Suffixes = ['from z = 0 to z = %d m' %z0Array[0],'from z = %d m to z = %d m' %(z0Array[0],z0Array[1]),
                      'from z = %d m to z = %d m' %(z0Array[1],z0Array[2]),
                      'from z = %d m to z = %d m' %(z0Array[2],z0Array[3]),'from z = %d m to Ocean Bottom' %z0Array[3]]
    FileName_Suffixes = ['_0-%d_m' %(-z0Array[0]),'_%d_m-%d_m' %(-z0Array[0],-z0Array[1]),
                         '_%d_m-%d_m' %(-z0Array[1],-z0Array[2]),'_%d_m-%d_m' %(-z0Array[2],-z0Array[3]),
                         '_%d_m-Ocean_Bottom' %(-z0Array[3])]
    nCases = len(z0Array) + 1
    for iCase in range(0,nCases):
        if display_elapsed_time_within_loop:
            start_time_within_loop = time.time()
        if iCase == nCases - 1:
            upperOnly = False
            z0 = 0.0
        else:
            upperOnly = True
            z0 = z0Array[iCase]
        Title_Suffix = Title_Suffixes[iCase]
        FileName_Suffix = FileName_Suffixes[iCase]
        #
        # Drift correction
        #
        # We first estimate the PI drift by taking the difference between two 10-year averages. The 10-year averages 
        # were calculated with NCO manually from ten years of monthly averages. In the papers we have looked at, they 
        # do not explain exactly how they do this drift correction. Should we be fitting a line to the whole PI time 
        # series? Should we be averaging over more than 10 years?
        #
        if iCase == 0:
            SSL_pi1 = SSL.ComputeStericSeaLevel(fmesh,f_pi1,upperOnly,z0)
            SSL_pi2 = SSL.ComputeStericSeaLevel(fmesh,f_pi2,upperOnly,z0)
            SSL_pi1_Surface_to_Depth_z0_Last = SSL_pi1
            SSL_pi2_Surface_to_Depth_z0_Last = SSL_pi2
        else:
            SSL_pi1_Surface_to_Depth_z0 = SSL.ComputeStericSeaLevel(fmesh,f_pi1,upperOnly,z0) 
            SSL_pi1 = SSL_pi1_Surface_to_Depth_z0 - SSL_pi1_Surface_to_Depth_z0_Last
            SSL_pi2_Surface_to_Depth_z0 = SSL.ComputeStericSeaLevel(fmesh,f_pi2,upperOnly,z0) 
            SSL_pi2 = SSL_pi2_Surface_to_Depth_z0 - SSL_pi2_Surface_to_Depth_z0_Last
            SSL_pi1_Surface_to_Depth_z0_Last = SSL_pi1_Surface_to_Depth_z0
            SSL_pi2_Surface_to_Depth_z0_Last = SSL_pi2_Surface_to_Depth_z0
        drift = (SSL_pi2 - SSL_pi1)/(yr_pi2 - yr_pi1) # m/year
        #
        # Historical SSLC
        #
        # Here again we are using 10-year averages calculated offline by NCO.
        #
        if iCase == 0:
            SSL_ref = SSL.ComputeStericSeaLevel(fmesh,f_ref,upperOnly,z0)
            SSL_i = SSL.ComputeStericSeaLevel(fmesh,f_i,upperOnly,z0)
            SSL_ref_Surface_to_Depth_z0_Last = SSL_ref
            SSL_i_Surface_to_Depth_z0_Last = SSL_i
        else:
            SSL_ref_Surface_to_Depth_z0 = SSL.ComputeStericSeaLevel(fmesh,f_ref,upperOnly,z0) 
            SSL_ref = SSL_ref_Surface_to_Depth_z0 - SSL_ref_Surface_to_Depth_z0_Last
            SSL_i_Surface_to_Depth_z0 = SSL.ComputeStericSeaLevel(fmesh,f_i,upperOnly,z0) 
            SSL_i = SSL_i_Surface_to_Depth_z0 - SSL_i_Surface_to_Depth_z0_Last
            SSL_pi1_Surface_to_Depth_z0_Last = SSL_pi1_Surface_to_Depth_z0
            SSL_pi2_Surface_to_Depth_z0_Last = SSL_pi2_Surface_to_Depth_z0
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
        # Plot the PI steric sea levels in years yr_pi1 and yr_pi2, the change in these PI steric sea levels, and the 
        # rate of change (drift).
        #
        plot_type = 'ScatterPlot' # Choose plot_type to be 'ScatterPlot' or 'FilledContourPlot'.
        nRows = 2
        nCols = 2
        nSubPlots = nRows*nCols
        ColorBarLimits = np.zeros((nSubPlots,2))
        if RestrictedColorbars:
            useGivenColorBarLimits = [False,False,True,True]
            ColorBarLimits[2,:] = np.array([-100.0,100.0])
            ColorBarLimits[3,:] = np.array([-1.0,1.0])
        else:
            useGivenColorBarLimits = [False,False,False,False]
        markersizes = [4.0,4.0,4.0,4.0]
        nContours = [300,300,300,300]
        cbarShrinkRatio = 0.65
        titles = ['PI Steric Sea Level (m)\nin Year %d\n' %yr_pi1 + Title_Suffix,
                  'PI Steric Sea Level (m)\nin Year %d\n' %yr_pi2 + Title_Suffix,
                  'PI Steric Sea Level\nChange (mm), %d to %d\n' %(yr_pi1,yr_pi2) + Title_Suffix,
                  'PI Steric Sea Level Change\nRate or Drift (mm/yr), %d to %d\n' %(yr_pi1,yr_pi2) + Title_Suffix]
        FileName = 'PI_StericSeaLevel_Change_Rate_%d-%d' %(yr_pi1,yr_pi2) + FileName_Suffix
        fig_size = [20.0,20.0]
        set_aspect_equal = [False,False,False,False]
        colormaps = [plt.cm.RdBu_r,plt.cm.RdBu_r,plt.cm.RdBu_r,plt.cm.RdBu_r]
        cbarlabelformats = ['%.1f','%.1f','%.1f','%.1f']
        hspace = 0.04 # height of the padding between subplots i.e. the vertical spacing between subplots
        wspace = 0.20 # width of the padding between subplots i.e. the horizontal spacing between subplots
        FigureFormat = 'png'
        bbox_inches = 'tight'
        PI_StericSeaLevels_Change_Rate = np.zeros((nSubPlots,len(SSL_pi1)))
        PI_StericSeaLevels_Change_Rate[0,:] = SSL_pi1
        PI_StericSeaLevels_Change_Rate[1,:] = SSL_pi2
        PI_StericSeaLevels_Change_Rate[2,:] = drift*1000.0*(yr_pi2 - yr_pi1)
        PI_StericSeaLevels_Change_Rate[3,:] = drift*1000.0
        CR.ScatterAndContourPlotsAsSubPlots(plot_type,output_directory,lonCell,latCell,nRows,nCols,
                                            PI_StericSeaLevels_Change_Rate,markersizes,nContours,labels,labelfontsizes,
                                            labelpads,tickfontsizes,useGivenColorBarLimits,ColorBarLimits,
                                            nColorBarTicks,cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,
                                            fig_size,set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,
                                            set_xticks_manually,xticks_set_manually,set_yticks_manually,
                                            yticks_set_manually,hspace,wspace,FigureFormat,bbox_inches)
        #
        # Plot the steric sea levels in years yr_ref and yr_i, the change in these steric sea levels, and the rate of 
        # change.
        #
        plot_type = 'ScatterPlot' # Choose plot_type to be 'ScatterPlot' or 'FilledContourPlot'.
        nRows = 2
        nCols = 2
        nSubPlots = nRows*nCols
        ColorBarLimits = np.zeros((nSubPlots,2))
        if RestrictedColorbars:
            useGivenColorBarLimits = [False,False,True,True]
            ColorBarLimits[2,:] = np.array([-100.0,100.0])
            ColorBarLimits[3,:] = np.array([-1.0,1.0])
        else:
            useGivenColorBarLimits = [False,False,False,False]
        markersizes = [4.0,4.0,4.0,4.0]
        nContours = [300,300,300,300]
        cbarShrinkRatio = 0.65
        titles = ['Steric Sea Level (m)\nin Year %d\n' %yr_ref + Title_Suffix,
                  'Steric Sea Level (m)\nin Year %d\n' %yr_i + Title_Suffix,
                  'Steric Sea Level\nChange (mm), %d to %d\n' %(yr_ref,yr_i) + Title_Suffix,
                  'Steric Sea Level Change\nRate (mm/yr), %d to %d\n' %(yr_ref,yr_i) + Title_Suffix]
        FileName = 'StericSeaLevel_Change_Rate_%d-%d' %(yr_ref,yr_i) + FileName_Suffix
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
                                            labelpads,tickfontsizes,useGivenColorBarLimits,ColorBarLimits,
                                            nColorBarTicks,cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,
                                            fig_size,set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,
                                            set_xticks_manually,xticks_set_manually,set_yticks_manually,
                                            yticks_set_manually,hspace,wspace,FigureFormat,bbox_inches)
        #
        # Plot the drift-corrected and demeaned steric sea level change from yr_ref to yr_i, and the rate of change.
        #
        plot_type = 'ScatterPlot' # Choose plot_type to be 'ScatterPlot' or 'FilledContourPlot'.
        nRows = 2
        nCols = 2
        nSubPlots = nRows*nCols
        ColorBarLimits = np.zeros((nSubPlots,2))
        if RestrictedColorbars:
            useGivenColorBarLimits = [True,True,True,True]
            ColorBarLimits[0,:] = np.array([-100.0,100.0])
            ColorBarLimits[1,:] = np.array([-1.0,1.0])
            ColorBarLimits[2,:] = np.array([-100.0,100.0])
            ColorBarLimits[3,:] = np.array([-1.0,1.0])
        else:
            useGivenColorBarLimits = [False,False,False,False]
        markersizes = [4.0,4.0,4.0,4.0]
        nContours = [300,300,300,300]
        cbarShrinkRatio = 0.65
        titles = ['Drift-Corrected Steric Sea\nLevel Change (mm), %d to %d\n' %(yr_ref,yr_i) + Title_Suffix,
                  'Drift-Corrected Steric Sea Level\nChange Rate (mm/yr), %d to %d\n' %(yr_ref,yr_i) + Title_Suffix,
                  ('Drift-Corrected and Demeaned Steric\nSea Level Change (mm), %d to %d\n' %(yr_ref,yr_i) 
                   + Title_Suffix),
                  ('Drift-Corrected and Demeaned Steric Sea\nLevel Change Rate (mm/yr), %d to %d\n' %(yr_ref,yr_i) 
                   + Title_Suffix)]
        FileName = 'DriftCorrected_Demeaned_StericSeaLevelChange_Rate_%d-%d' %(yr_ref,yr_i) + FileName_Suffix
        fig_size = [20.0,20.0]
        set_aspect_equal = [False,False,False,False]
        colormaps = [plt.cm.RdBu_r,plt.cm.RdBu_r,plt.cm.RdBu_r,plt.cm.RdBu_r]
        cbarlabelformats = ['%.1f','%.1f','%.1f','%.1f']
        hspace = 0.04 # height of the padding between subplots i.e. the vertical spacing between subplots
        wspace = 0.20 # width of the padding between subplots i.e. the horizontal spacing between subplots
        FigureFormat = 'png'
        bbox_inches = 'tight'
        DriftCorrected_Demeaned_StericSeaLevelChange_Rate = np.zeros((nSubPlots,len(SSLChangeRate)))
        DriftCorrected_Demeaned_StericSeaLevelChange_Rate[0,:] = (SSLChangeRate - drift)*1000.0*(yr_i - yr_ref)
        DriftCorrected_Demeaned_StericSeaLevelChange_Rate[1,:] = (SSLChangeRate - drift)*1000.0
        DriftCorrected_Demeaned_StericSeaLevelChange_Rate[2,:] = (
        (SSLChangeRate - drift - (SSLChangeRate - drift).mean())*1000.0*(yr_i - yr_ref))
        DriftCorrected_Demeaned_StericSeaLevelChange_Rate[3,:] = (SSLChangeRate - drift 
                                                                  - (SSLChangeRate - drift).mean())*1000.0
        CR.ScatterAndContourPlotsAsSubPlots(plot_type,output_directory,lonCell,latCell,nRows,nCols,
                                            DriftCorrected_Demeaned_StericSeaLevelChange_Rate,markersizes,nContours,
                                            labels,labelfontsizes,labelpads,tickfontsizes,useGivenColorBarLimits,
                                            ColorBarLimits,nColorBarTicks,cbarShrinkRatio,titles,titlefontsize,
                                            SaveAsPDF,FileName,Show,fig_size,set_aspect_equal,colormaps,
                                            cbarlabelformats,cbarfontsize,set_xticks_manually,xticks_set_manually,
                                            set_yticks_manually,yticks_set_manually,hspace,wspace,FigureFormat,
                                            bbox_inches)
        if iCase == nCases - 1:
            Title_Suffix = 'from z = %d m to the ocean bottom' %z0Array[3]
        if display_elapsed_time_within_loop:
            end_time_within_loop = time.time()
            elapsed_time_within_loop = end_time_within_loop - start_time_within_loop
            if elapsed_time_within_loop >= 3600.0:
                elapsed_time_within_loop_hours = np.floor(elapsed_time_within_loop/3600.0)
                remaining_time_within_loop = np.mod(elapsed_time_within_loop,3600.0)
                elapsed_time_within_loop_minutes = np.floor(remaining_time_within_loop/60.0)
                elapsed_time_within_loop_seconds = np.mod(remaining_time_within_loop,60.0)
                print('The elapsed time for computing the steric sea level %s is %d hours %d minutes %d seconds.' 
                      %(Title_Suffix,elapsed_time_within_loop_hours,elapsed_time_within_loop_minutes,
                        elapsed_time_within_loop_seconds))
            else:
                elapsed_time_within_loop_minutes = np.floor(elapsed_time_within_loop/60.0)
                elapsed_time_within_loop_seconds = np.mod(elapsed_time_within_loop,60.0)
                print('The elapsed time for computing the steric sea level %s is %d minutes %d seconds.' 
                      %(Title_Suffix,elapsed_time_within_loop_minutes,elapsed_time_within_loop_seconds))
    if display_elapsed_time:
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time >= 3600.0:
            elapsed_time_hours = np.floor(elapsed_time/3600.0)
            remaining_time = np.mod(elapsed_time,3600.0)
            elapsed_time_minutes = np.floor(remaining_time/60.0)
            elapsed_time_seconds = np.mod(remaining_time,60.0)
            print('The total elapsed time for computing the steric sea level is %d hours %d minutes %d seconds.' 
                  %(elapsed_time_hours,elapsed_time_minutes,elapsed_time_seconds))
        else:
            elapsed_time_minutes = np.floor(elapsed_time/60.0)
            elapsed_time_seconds = np.mod(elapsed_time,60.0)
            print('The total elapsed time for computing the steric sea level is %d minutes %d seconds.' 
                  %(elapsed_time_minutes,elapsed_time_seconds))