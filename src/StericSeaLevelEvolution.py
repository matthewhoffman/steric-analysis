"""
Name: StericSeaLevelEvolution.py
Author: Sid Bishnu and Matt Hoffman
Details: This script computes the global steric sea level  (SSL) at preindustrial and historial times, and plots the 
SSL evolution.
"""


import numpy as np
import matplotlib.pyplot as plt
import time
from IPython.utils import io
with io.capture_output() as captured:
    import CommonRoutines as CR
    import StericSeaLevel as SSL
    
    
def ComputeStericSeaLevelEvolution(fmesh,yr_pi1,f_pi1,yr_pi2,f_pi2,yr_ref,f_ref,yr_i,f_i,f,RestrictedColorbars=False):
    display_elapsed_time = True
    if display_elapsed_time:
        start_time = time.time()
    myGlobalConstants = CR.GlobalConstants()
    # Load the MPAS-Ocean base mesh fields as needed.
    latCell = fmesh.variables['latCell'][:]*180.0/myGlobalConstants.pii
    lonCell = fmesh.variables['lonCell'][:]*180.0/myGlobalConstants.pii
    #
    # Drift correction
    #
    # We first estimate the PI drift by taking the difference between two 10-year averages. The 10-year averages were 
    # calculated with NCO manually from ten years of monthly averages. In the papers we have looked at, they do not 
    # explain exactly how they do this drift correction. Should we be fitting a line to the whole PI time series? 
    # Should we be averaging over more than 10 years?
    #
    SSL_pi1 = SSL.ComputeStericSeaLevel(fmesh,f_pi1)
    SSL_pi2 = SSL.ComputeStericSeaLevel(fmesh,f_pi2)
    drift = (SSL_pi2 - SSL_pi1)/(yr_pi2 - yr_pi1) # m/year
    #
    # Historical SSLC
    #
    # Here again we are using 10-year averages calculated offline by NCO.
    #
    SSL_ref = SSL.ComputeStericSeaLevel(fmesh,f_ref)
    SSL_i = SSL.ComputeStericSeaLevel(fmesh,f_i)
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
    # Plot the PI steric sea levels in years yr_pi1 and yr_pi2, the change in these PI steric sea levels, and the rate 
    # of change (drift).
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
    titles = ['PI Steric Sea Level (m)\nin Year %d' %yr_pi1,'PI Steric Sea Level (m)\nin Year %d' %yr_pi2,
              'PI Steric Sea Level\nChange (mm), %d to %d' %(yr_pi1,yr_pi2),
              'PI Steric Sea Level Change\nRate or Drift (mm/yr), %d to %d' %(yr_pi1,yr_pi2)]
    FileName = 'PI_StericSeaLevel_Change_Rate_%d-%d' %(yr_pi1,yr_pi2)
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
                                        labelpads,tickfontsizes,useGivenColorBarLimits,ColorBarLimits,nColorBarTicks,
                                        cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,fig_size,
                                        set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,set_xticks_manually,
                                        xticks_set_manually,set_yticks_manually,yticks_set_manually,hspace,wspace,
                                        FigureFormat,bbox_inches)
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
    titles = ['Steric Sea Level (m)\nin Year %d' %yr_ref,'Steric Sea Level (m)\nin Year %d' %yr_i,
              'Steric Sea Level\nChange (mm), %d to %d' %(yr_ref,yr_i),
              'Steric Sea Level Change\nRate (mm/yr), %d to %d' %(yr_ref,yr_i)]
    FileName = 'StericSeaLevel_Change_Rate_%d-%d' %(yr_ref,yr_i)
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
    # Plot the drift-corrected and demeaned steric sea level change from 1900 to 2000, and the rate of change.
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
    titles = ['Drift-Corrected Steric Sea\nLevel Change (mm), %d to %d' %(yr_ref,yr_i),
              'Drift-Corrected Steric Sea Level\nChange Rate (mm/yr), %d to %d' %(yr_ref,yr_i),
              'Drift-Corrected and Demeaned Steric\nSea Level Change (mm), %d to %d' %(yr_ref,yr_i),
              'Drift-Corrected and Demeaned Steric Sea\nLevel Change Rate (mm/yr), %d to %d' %(yr_ref,yr_i)]
    FileName = 'DriftCorrected_Demeaned_StericSeaLevelChange_Rate_%d-%d' %(yr_ref,yr_i)
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
    DriftCorrected_Demeaned_StericSeaLevelChange_Rate[2,:] = (SSLChangeRate - drift 
                                                              - (SSLChangeRate - drift).mean())*1000.0*(yr_i - yr_ref)
    DriftCorrected_Demeaned_StericSeaLevelChange_Rate[3,:] = (SSLChangeRate - drift 
                                                              - (SSLChangeRate - drift).mean())*1000.0
    CR.ScatterAndContourPlotsAsSubPlots(plot_type,output_directory,lonCell,latCell,nRows,nCols,
                                        DriftCorrected_Demeaned_StericSeaLevelChange_Rate,markersizes,nContours,labels,
                                        labelfontsizes,labelpads,tickfontsizes,useGivenColorBarLimits,ColorBarLimits,
                                        nColorBarTicks,cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,
                                        fig_size,set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,
                                        set_xticks_manually,xticks_set_manually,set_yticks_manually,yticks_set_manually,
                                        hspace,wspace,FigureFormat,bbox_inches)
    #
    # We finally plot the pressure-adjusted SSH and the difference between its decadal means across a century. We 
    # believe this represents the dynamic sea level. It has nothing to do with steric, but is the other ocean component 
    # we want. It looks reasonable compared to previous papers.
    #
    PressureAdjustedSSH = f.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
    PressureAdjustedSSHRef = f_ref.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
    plot_type = 'ScatterPlot' # Choose plot_type to be 'ScatterPlot' or 'FilledContourPlot'.
    nSubPlots = 3
    ColorBarLimits = np.zeros((nSubPlots,2))
    if RestrictedColorbars:
        useGivenColorBarLimits = [True,True,True]
        ColorBarLimits[0,:] = np.array([-1.7,1.7])
        ColorBarLimits[1,:] = np.array([-1.7,1.7])
        ColorBarLimits[2,:] = np.array([-0.1,0.1])
    else:
        useGivenColorBarLimits = [False,False,False]
    markersizes = [4.0,4.0,4.0]
    nContours = [300,300,300]
    cbarShrinkRatio = 0.65
    titles = ['Pressure Adjusted SSH (m)\nin Year %d' %(yr_ref+5),'Pressure Adjusted SSH (m)\nin Year %d' %(yr_i+5),
              'Change in Pressure Adjusted\nSSH (m), %d to %d' %(yr_ref+5,yr_i+5)]
    FileName = 'PressureAdjustedSSH_Change_%d_%d' %(yr_ref+5,yr_i+5)
    fig_size = [20.0,20.0]
    set_aspect_equal = [False,False,False]
    colormaps = [plt.cm.RdBu_r,plt.cm.RdBu_r,plt.cm.RdBu_r]
    cbarlabelformats = ['%.1f','%.1f','%.1f']
    hspace = 0.05 # height of the padding between subplots i.e. the vertical spacing between subplots
    wspace = 0.50 # width of the padding between subplots i.e. the horizontal spacing between subplots
    FigureFormat = 'png'
    bbox_inches = 'tight'
    PressureAdjustedSSH_yr_ref_yr_i = np.zeros((nSubPlots,len(PressureAdjustedSSH)))
    PressureAdjustedSSH_yr_ref_yr_i[0,:] = PressureAdjustedSSHRef
    PressureAdjustedSSH_yr_ref_yr_i[1,:] = PressureAdjustedSSH
    PressureAdjustedSSH_yr_ref_yr_i[2,:] = PressureAdjustedSSH - PressureAdjustedSSHRef
    CR.ScatterAndContourPlotsAs3SubPlots(plot_type,output_directory,lonCell,latCell,PressureAdjustedSSH_yr_ref_yr_i,
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
        
        
def ComputeStericSeaLevelEvolutionOnZLevelAndZStarVerticalCoordinates(
fmesh,yr_ref,f_ref,yr_i,f_i,f,VerticalCoordinate='zStar',RestrictedColorbars=False):
    display_elapsed_time = True
    if display_elapsed_time:
        start_time = time.time()
    if VerticalCoordinate == 'zStar':
        title_prefix = 'z* Coordinate: '
    elif VerticalCoordinate == 'zLevel':
        title_prefix = 'z Coordinate: '
    myGlobalConstants = CR.GlobalConstants()
    # Load the MPAS-Ocean base mesh fields as needed.
    latCell = fmesh.variables['latCell'][:]*180.0/myGlobalConstants.pii
    lonCell = fmesh.variables['lonCell'][:]*180.0/myGlobalConstants.pii
    SSL_ref = SSL.ComputeStericSeaLevel(fmesh,f_ref)
    SSL_i = SSL.ComputeStericSeaLevel(fmesh,f_i)
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
    # Plot the steric sea levels in the January of years yr_ref and yr_i, the change in these steric sea levels, and 
    # the rate of change.
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
    titles = [title_prefix + 'Steric Sea\nLevel (m) in Year %d January' %yr_ref,
              title_prefix + 'Steric Sea\nLevel (m) in Year %d January' %yr_i,
              title_prefix + '\nSteric Sea Level Change (mm),\nYear %d January to Year %d January' %(yr_ref,yr_i),
              (title_prefix + '\nSteric Sea Level Change Rate (mm/yr),\nYear %d January to Year %d January'
               %(yr_ref,yr_i))]
    FileName = VerticalCoordinate + '_StericSeaLevel_Change_Rate_Year_%d_Jan_Year_%d_Jan' %(yr_ref,yr_i)
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
    # Plot the demeaned steric sea level change from Year yr_ref January to Year yr_i January, and the rate of change.
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
    titles = [(title_prefix + 'Demeaned\nSteric Sea Level Change (mm),\nYear %d January to Year %d January' 
               %(yr_ref,yr_i)),
              (title_prefix + 'Demeaned Steric\nSea Level Change Rate (mm/yr),\nYear %d January to Year %d January' 
               %(yr_ref,yr_i))]
    FileName = VerticalCoordinate + '_Demeaned_StericSeaLevelChange_Rate_Year_%d_Jan_Year_%d_Jan' %(yr_ref,yr_i)
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
    titles = [title_prefix + 'Pressure Adjusted SSH (m)\nin Year %d January' %yr_ref,
              title_prefix + 'Pressure Adjusted SSH (m)\nin Year %d January' %yr_i,
              title_prefix + 'Change in Pressure Adjusted SSH (m),\nYear %d January to Year %d January' %(yr_ref,yr_i)]
    FileName = VerticalCoordinate + '_PressureAdjustedSSH_Change_Year_%d_Jan_Year_%d_Jan' %(yr_ref,yr_i)
    fig_size = [20.0,20.0]
    set_aspect_equal = [False,False,False]
    colormaps = [plt.cm.RdBu_r,plt.cm.RdBu_r,plt.cm.RdBu_r]
    cbarlabelformats = ['%.1f','%.1f','%.1f']
    hspace = 0.05 # height of the padding between subplots i.e. the vertical spacing between subplots
    wspace = 0.50 # width of the padding between subplots i.e. the horizontal spacing between subplots
    FigureFormat = 'png'
    bbox_inches = 'tight'
    PressureAdjustedSSH_1900_2000 = np.zeros((nSubPlots,len(PressureAdjustedSSH)))
    PressureAdjustedSSH_1900_2000[0,:] = PressureAdjustedSSHRef
    PressureAdjustedSSH_1900_2000[1,:] = PressureAdjustedSSH
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