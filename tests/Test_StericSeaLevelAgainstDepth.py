"""
Name: Test_StericSeaLevelAgainstDepth.py
Author: Sid Bishnu
Details: As the name implies, this script tests the various functions of ../src/StericSeaLevelAgainstDepth.py
"""


import os
import sys
import netCDF4
import numpy as np
import time
sys.path.append(os.path.realpath('..') + '/src/')
from IPython.utils import io
with io.capture_output() as captured:
    import CommonRoutines as CR
    import StericSeaLevelAgainstDepth as SSLAD
    
    
myGlobalConstants = CR.GlobalConstants()
    
    
def SpecifyMeshAndOutputFileNames(ReturnOnlyYears=False):
    # WC v1
    fmesh = (
    netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/oEC60to30v3_60layer.restartFrom_anvil0926.171101.nc'))
    yr_pi1 = 405 # nominal year
    f_pi1 = netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/piControl/0400-0410/mpaso.hist.0400-0410.nc','r')
    yr_pi2 = 495 # nominal year
    f_pi2 = netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/piControl/0490-0500/mpaso.hist.0490-0500.nc','r')
    # Historical SSLC: We are using 10-year averages calculated offline by NCO.
    yr_ref = 1900
    f_ref = (
    netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/lowres_hist_ens/ensMn/mpaso.hist.1900-1909.nc','r'))
    yr_i = 2000
    f_i = netCDF4.Dataset('/global/cscratch1/sd/hoffman2/SLR_tests/lowres_hist_ens/ensMn/mpaso.hist.2000-2009.nc','r')
    if ReturnOnlyYears:
        return yr_pi1, yr_pi2, yr_ref, yr_i
    else:
        return fmesh, yr_pi1, f_pi1, yr_pi2, f_pi2, yr_ref, f_ref, yr_i, f_i


def TestComputeContributionToStericSeaLevelAsAFunctionOfDepth(NearestToASpecificLocation,Latitude,Longitude,Radius,
                                                              AverageWithinWithinGivenRadius,TitlePrefix,
                                                              FileNamePrefix,display_elapsed_time,MakePlotsAtEachLocationAndYear=False):
    fmesh, yr_pi1, f_pi1, yr_pi2, f_pi2, yr_ref, f_ref, yr_i, f_i = SpecifyMeshAndOutputFileNames()
    LatitudeInDegrees = Latitude
    LongitudeInDegrees = Longitude
    pii = myGlobalConstants.pii
    Latitude *= pii/180.0
    Longitude *= pii/180.0
    yrs = [yr_pi1,yr_pi2,yr_ref,yr_i]
    fs = [f_pi1,f_pi2,f_ref,f_i]
    output_directory = '../output/'
    if display_elapsed_time:
        start_time = time.time()
    zCenters = []
    Temperatures = []
    Salinities = []
    RhoByRhoRefs = []
    StericSeaLevels = []
    StericSeaLevelCumSums = []
    for i in range(0,len(yrs)):
        if i > 0:
            yr_last = yrs[i-1]
        yr = yrs[i]
        f = fs[i]
        zCenter, Temperature, Salinity, RhoByRhoRef, StericSeaLevel, StericSeaLevelCumSum = (
        SSLAD.ComputeContributionToStericSeaLevelAsAFunctionOfDepth(fmesh,f,NearestToASpecificLocation,Latitude,
                                                                    Longitude,AverageWithinWithinGivenRadius,Radius))
        if np.mod(float(i),2.0) == 0.0:
            StericSeaLevelLast = StericSeaLevel
        else: # if np.mod(float(i),2.0) == 1.0:
            StericSeaLevelChange = StericSeaLevel - StericSeaLevelLast
        plot_type = 'regular'
        linewidth = 2.0
        linestyle = '-'
        color = 'k'
        marker = True
        markertype = 's'
        markersize = 7.5
        xLabel = 'Contribution to Steric Sea Level (m)'
        yLabel = 'Depth (km)'
        labels = [xLabel,yLabel]
        labelfontsizes = [22.5,22.5]
        labelpads = [10.0,10.0]
        tickfontsizes = [15.0,15.0]
        title = (TitlePrefix + '\nLatitude %.1f$^\circ$, Longitude %.1f$^\circ$, Year %d'
                 %(LatitudeInDegrees,LongitudeInDegrees,yr) + '\nContribution to Steric Sea Level versus Depth')
        titlefontsize = 25.0
        SaveAsPDF = True
        FileName = FileNamePrefix + '_%d_ContributionToStericSeaLevelVersusDepth' %yr
        Show = False
        if MakePlotsAtEachLocationAndYear:
            CR.WriteCurve1D(output_directory,zCenter/1000.0,StericSeaLevel,FileName)
            CR.PythonPlot1DSaveAsPDF(output_directory,plot_type,StericSeaLevel,zCenter/1000.0,linewidth,linestyle,color,
                                     marker,markertype,markersize,labels,labelfontsizes,labelpads,tickfontsizes,title,
                                     titlefontsize,SaveAsPDF,FileName,Show)
        if np.mod(float(i),2.0) == 1.0:
            xLabel = 'Contribution to Steric Sea Level Change (mm)'
            labels = [xLabel,yLabel]
            title = (TitlePrefix + '\nLatitude %.1f$^\circ$, Longitude %.1f$^\circ$, Years %d to %d'
                     %(LatitudeInDegrees,LongitudeInDegrees,yr_last,yr) 
                     + '\nContribution to Steric Sea Level Change versus Depth')
            FileName = FileNamePrefix + '_%d-%d_ContributionToStericSeaLevelChangeVersusDepth' %(yr_last,yr)
            if MakePlotsAtEachLocationAndYear:
                CR.WriteCurve1D(output_directory,zCenter/1000.0,StericSeaLevelChange*1000.0,FileName)
                CR.PythonPlot1DSaveAsPDF(output_directory,plot_type,StericSeaLevelChange*1000.0,zCenter/1000.0,
                                         linewidth,linestyle,color,marker,markertype,markersize,labels,labelfontsizes,
                                         labelpads,tickfontsizes,title,titlefontsize,SaveAsPDF,FileName,Show)
        zCenters.append(zCenter)
        Temperatures.append(Temperature)
        Salinities.append(Salinity)
        RhoByRhoRefs.append(RhoByRhoRef)
        StericSeaLevels.append(StericSeaLevel)
        StericSeaLevelCumSums.append(StericSeaLevelCumSum)
    if display_elapsed_time:
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_minutes = np.floor(elapsed_time/60.0)
        elapsed_time_seconds = np.mod(elapsed_time,60.0)
        print('The elapsed time is %d minutes %d seconds.' %(elapsed_time_minutes,elapsed_time_seconds))
    return zCenters, Temperatures, Salinities, RhoByRhoRefs, StericSeaLevels, StericSeaLevelCumSums
        
        
def TestComputeContributionToStericSeaLevelAsAFunctionOfDepthAtGivenLocations(
PlotPreIndustrialAndHistorialDataOnSameGraph=True):
    NearestToASpecificLocation = True
    # [Latitude,Longitude] of the chosen location in the North Pacific Ocean Continental Shelf is [48.0,-127.0].
    # [Latitude,Longitude] of the chosen location in the Deep North Pacific Deep is [27.0,163.0].
    # [Latitude,Longitude] of the chosen location in the North Atlantic Ocean Continental Shelf is [35.5,-75.0].
    # [Latitude,Longitude] of the chosen location in the Deep North Atlantic Ocean is [22.0,-33.0].
    # [Latitude,Longitude] of the chosen location in the Indian Ocean Continental Shelf is [-4.5,101.0].
    # [Latitude,Longitude] of the chosen location in the Deep Indian Ocean is [-15.0,80.0].
    Latitudes = np.array([48.0,27.0,35.5,22.0,-4.5,-15.0])
    Longitudes = np.array([-127.0,163.0,-75.0,-33.0,101.0,80.0])
    Radii = np.array([20000.0,100.0,10000.0,6000.0,100.0,100.0])*1000.0
    AverageWithinWithinGivenRadius = False
    TitlePrefixes = ['North Pacific Ocean Continental Shelf','Deep North Pacific Ocean',
                     'North Atlantic Ocean Continental Shelf','Deep North Atlantic Ocean',
                     'Indian Ocean Continental Shelf','Deep Indian Ocean']
    FileNamePrefixes = ['ShallowNorthPacificOcean','DeepNorthPacificOcean','ShallowNorthAtlanticOcean',
                        'DeepNorthAtlanticOcean','ShallowIndianOcean','DeepIndianOcean']
    FileNamePrefixes_SubPlots = ['PacificOcean','AtlanticOcean','IndianOcean']
    nLocations = len(Latitudes)
    display_elapsed_time = True
    yr_pi1, yr_pi2, yr_ref, yr_i = SpecifyMeshAndOutputFileNames(ReturnOnlyYears=True)
    yrs = [yr_pi1,yr_pi2,yr_ref,yr_i]
    legends = ['Preindustrial Year %d' %yrs[1],'Historical Year %d' %yrs[3],
               'Preindustrial Year %d' %yrs[1],'Historical Year %d' %yrs[3]]
    legendfontsize = 17.5
    legendpads = [1.0,0.5]
    output_directory = '../output/'
    if display_elapsed_time:
        start_time = time.time()
    for iLocation in range(0,nLocations):
        Latitude = Latitudes[iLocation]
        Longitude = Longitudes[iLocation]
        Radius = Radii[iLocation]
        TitlePrefix = TitlePrefixes[iLocation]
        FileNamePrefix = FileNamePrefixes[iLocation]
        if np.mod(float(iLocation),2.0) == 0.0:
            zCenters_s, Temperatures_s, Salinities_s, RhoByRhoRefs_s, StericSeaLevels_s, StericSeaLevelCumSums_s = (
            TestComputeContributionToStericSeaLevelAsAFunctionOfDepth(
            NearestToASpecificLocation,Latitude,Longitude,Radius,AverageWithinWithinGivenRadius,TitlePrefix,
            FileNamePrefix,display_elapsed_time))
            TitlePrefix_s = TitlePrefixes[iLocation]
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                Title_Location_s = '\nLatitude %.1f$^\circ$, Longitude %.1f$^\circ$' %(Latitude,Longitude)
            else:
                Title_Location_s = '\nLatitude %.1f$^\circ$, Longitude %.1f$^\circ$, Year ' %(Latitude,Longitude)
            Title_Locations_s = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                Title_Locations_s.extend([Title_Location_s])
            else:
                Title_Locations_s.extend([Title_Location_s + '%d' %yrs[0],Title_Location_s + '%d' %yrs[1],
                                          Title_Location_s + '%d' %yrs[2],Title_Location_s + '%d' %yrs[3]])
        else: # if np.mod(float(iLocation),2.0) == 1.0:
            zCenters_d, Temperatures_d, Salinities_d, RhoByRhoRefs_d, StericSeaLevels_d, StericSeaLevelCumSums_d = (
            TestComputeContributionToStericSeaLevelAsAFunctionOfDepth(
            NearestToASpecificLocation,Latitude,Longitude,Radius,AverageWithinWithinGivenRadius,TitlePrefix,
            FileNamePrefix,display_elapsed_time))
            TitlePrefix_d = TitlePrefixes[iLocation]
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                Title_Location_d = '\nLatitude %.1f$^\circ$, Longitude %.1f$^\circ$' %(Latitude,Longitude)
            else:
                Title_Location_d = '\nLatitude %.1f$^\circ$, Longitude %.1f$^\circ$, Year ' %(Latitude,Longitude)
            Title_Locations_d = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                Title_Locations_d.extend([Title_Location_d])
            else:
                Title_Locations_d.extend([Title_Location_d + '%d' %yrs[0],Title_Location_d + '%d' %yrs[1],
                                          Title_Location_d + '%d' %yrs[2],Title_Location_d + '%d' %yrs[3]])
            plot_type = 'regular'
            nRows = 2
            nRows_2 = 1
            nCols = 2
            nSubPlots = nRows*nCols
            zCenters = []
            Temperatures = []
            Salinities = []
            RhoByRhoRefs = []
            StericSeaLevels = []
            StericSeaLevelCumSums = []
            zCenters.extend([zCenters_s[1]/1000.0,zCenters_s[3]/1000.0,zCenters_d[1]/1000.0,zCenters_d[3]/1000.0])
            Temperatures.extend([Temperatures_s[1],Temperatures_s[3],Temperatures_d[1],Temperatures_d[3]])
            Salinities.extend([Salinities_s[1],Salinities_s[3],Salinities_d[1],Salinities_d[3]])
            RhoByRhoRefs.extend([RhoByRhoRefs_s[1],RhoByRhoRefs_s[3],RhoByRhoRefs_d[1],RhoByRhoRefs_d[3]])
            StericSeaLevels.extend([StericSeaLevels_s[1],StericSeaLevels_s[3],StericSeaLevels_d[1],
                                    StericSeaLevels_d[3]])
            StericSeaLevelCumSums.extend([StericSeaLevelCumSums_s[1],StericSeaLevelCumSums_s[3],
                                          StericSeaLevelCumSums_d[1],StericSeaLevelCumSums_d[3]])
            linewidths = 2.0*np.ones(nSubPlots)
            linestyles_1 = ['-','--','-','--']
            linestyles_2 = ['-','-','-','-']
            colors_1 = ['r','b','r','b']
            colors_2 = ['k','k','k','k']
            markers = np.ones(nSubPlots,dtype=bool)
            markertypes_1 = ['s','o','s','o']
            markertypes_2 = ['s','s','s','s']
            markersizes_1 = [7.5,10.0,7.5,10.0]
            markersizes_2 = 10.0*np.ones(nSubPlots)
            yLabel = 'Depth (km)'
            yLabels = []
            yLabels.extend([yLabel,yLabel,yLabel,yLabel])
            labelfontsizes_1 = [22.5,22.5]
            labelfontsizes_2 = [20.0,20.0]
            labelpads = [10.0,10.0]
            tickfontsizes = [15.0,15.0]
            titlefontsize_1 = 22.5
            titlefontsize_2 = 22.5
            SaveAsPDF = True
            FileNamePrefix_SubPlots = FileNamePrefixes_SubPlots[int((iLocation - 1)/2)]
            Show = False
            fig_size_1 = [20.0,9.25]
            fig_size_2 = [20.0,20.0]
            hspace = 0.35 # height of the padding between subplots i.e. the vertical spacing between subplots
            wspace = 0.25 # width of the padding between subplots i.e. the horizontal spacing between subplots
            xLabel = 'Temperature (Celsius)'
            xLabels = []
            xLabels.extend([xLabel,xLabel,xLabel,xLabel])
            titles = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                titles.extend([TitlePrefix_s + Title_Locations_s[0],TitlePrefix_d + Title_Locations_d[0]])
            else:
                titles.extend([TitlePrefix_s + Title_Locations_s[1],TitlePrefix_s + Title_Locations_s[3],
                               TitlePrefix_d + Title_Locations_d[1],TitlePrefix_d + Title_Locations_d[3]])
            for iTitle in range(0,len(titles)):
                titles[iTitle] += '\nTemperature versus Depth'
            FileName = FileNamePrefix_SubPlots + '_%d_%d_TemperatureVersusDepth' %(yrs[1],yrs[3])
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                legendposition = 'lower right'
                CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows_2,nCols,Temperatures,zCenters,
                                                 linewidths,linestyles_1,colors_1,markers,markertypes_1,markersizes_1,
                                                 xLabels,yLabels,labelfontsizes_1,labelpads,tickfontsizes,legends,
                                                 legendfontsize,legendposition,titles,titlefontsize_1,SaveAsPDF,
                                                 FileName,Show,fig_size=fig_size_1,legendWithinBox=True,
                                                 legendpads=legendpads,hspace=0.0,wspace=0.25)
            else:
                CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,Temperatures,zCenters,linewidths,
                                           linestyles_2,colors_2,markers,markertypes_2,markersizes_2,xLabels,yLabels,
                                           labelfontsizes_2,labelpads,tickfontsizes,titles,titlefontsize_2,SaveAsPDF,
                                           FileName,Show,fig_size=fig_size_2,hspace=hspace,wspace=wspace)
            xLabel = 'Salinity (gm per kg)'
            xLabels = []
            xLabels.extend([xLabel,xLabel,xLabel,xLabel])
            titles = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                titles.extend([TitlePrefix_s + Title_Locations_s[0],TitlePrefix_d + Title_Locations_d[0]])
            else:
                titles.extend([TitlePrefix_s + Title_Locations_s[1],TitlePrefix_s + Title_Locations_s[3],
                               TitlePrefix_d + Title_Locations_d[1],TitlePrefix_d + Title_Locations_d[3]])
            for iTitle in range(0,len(titles)):
                titles[iTitle] += '\nSalinity versus Depth'
            FileName = FileNamePrefix_SubPlots + '_%d_%d_SalinityVersusDepth' %(yrs[1],yrs[3])
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                legendposition = 'lower center'
                CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows_2,nCols,Salinities,zCenters,
                                                 linewidths,linestyles_1,colors_1,markers,markertypes_1,markersizes_1,
                                                 xLabels,yLabels,labelfontsizes_1,labelpads,tickfontsizes,legends,
                                                 legendfontsize,legendposition,titles,titlefontsize_1,SaveAsPDF,
                                                 FileName,Show,fig_size=fig_size_1,legendWithinBox=True,
                                                 legendpads=legendpads,hspace=0.0,wspace=0.25)
            else:
                CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,Salinities,zCenters,linewidths,
                                           linestyles_2,colors_2,markers,markertypes_2,markersizes_2,xLabels,yLabels,
                                           labelfontsizes_2,labelpads,tickfontsizes,titles,titlefontsize_2,SaveAsPDF,
                                           FileName,Show,fig_size=fig_size_2,hspace=hspace,wspace=wspace)
            xLabel = 'Ratio of Density to Reference Density'
            xLabels = []
            xLabels.extend([xLabel,xLabel,xLabel,xLabel])
            titles = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                titles.extend([TitlePrefix_s + Title_Locations_s[0],TitlePrefix_d + Title_Locations_d[0]])
            else:
                titles.extend([TitlePrefix_s + Title_Locations_s[1],TitlePrefix_s + Title_Locations_s[3],
                               TitlePrefix_d + Title_Locations_d[1],TitlePrefix_d + Title_Locations_d[3]])
            for iTitle in range(0,len(titles)):
                titles[iTitle] += '\nRatio of Density to Reference Density\nversus Depth'
            FileName = FileNamePrefix_SubPlots + '_%d_%d_DensityByReferenceDensityVersusDepth' %(yrs[1],yrs[3])
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                legendposition = 'lower left'
                CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows_2,nCols,RhoByRhoRefs,zCenters,
                                                 linewidths,linestyles_1,colors_1,markers,markertypes_1,markersizes_1,
                                                 xLabels,yLabels,labelfontsizes_1,labelpads,tickfontsizes,legends,
                                                 legendfontsize,legendposition,titles,titlefontsize_1,SaveAsPDF,
                                                 FileName,Show,fig_size=fig_size_1,legendWithinBox=True,
                                                 legendpads=legendpads,hspace=0.0,wspace=0.25)
            else:
                CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,RhoByRhoRefs,zCenters,linewidths,
                                           linestyles_2,colors_2,markers,markertypes_2,markersizes_2,xLabels,yLabels,
                                           labelfontsizes_2,labelpads,tickfontsizes,titles,titlefontsize_2,SaveAsPDF,
                                           FileName,Show,fig_size=fig_size_2,hspace=hspace+0.075,wspace=wspace)
            xLabel = 'Contribution to Steric Sea Level (m)'
            xLabels = []
            xLabels.extend([xLabel,xLabel,xLabel,xLabel])
            titles = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                titles.extend([TitlePrefix_s + Title_Locations_s[0],TitlePrefix_d + Title_Locations_d[0]])
            else:
                titles.extend([TitlePrefix_s + Title_Locations_s[1],TitlePrefix_s + Title_Locations_s[3],
                               TitlePrefix_d + Title_Locations_d[1],TitlePrefix_d + Title_Locations_d[3]])
            for iTitle in range(0,len(titles)):
                titles[iTitle] += '\nContribution to Steric Sea Level\nversus Depth'
            FileName = FileNamePrefix_SubPlots + '_%d_%d_ContributionToStericSeaLevelVersusDepth' %(yrs[1],yrs[3])
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                legendposition = 'lower right'
                CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows_2,nCols,StericSeaLevels,zCenters,
                                                 linewidths,linestyles_1,colors_1,markers,markertypes_1,markersizes_1,
                                                 xLabels,yLabels,labelfontsizes_1,labelpads,tickfontsizes,legends,
                                                 legendfontsize,legendposition,titles,titlefontsize_1,SaveAsPDF,
                                                 FileName,Show,fig_size=fig_size_1,legendWithinBox=True,
                                                 legendpads=legendpads,hspace=0.0,wspace=0.25)
            else:            
                CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,StericSeaLevels,zCenters,linewidths,
                                           linestyles_2,colors_2,markers,markertypes_2,markersizes_2,xLabels,yLabels,
                                           labelfontsizes_2,labelpads,tickfontsizes,titles,titlefontsize_2,SaveAsPDF,
                                           FileName,Show,fig_size=fig_size_2,hspace=hspace+0.075,wspace=wspace)
            xLabel = 'Cumulative Steric Sea Level (m)'
            xLabels = []
            xLabels.extend([xLabel,xLabel,xLabel,xLabel])
            titles = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                titles.extend([TitlePrefix_s + Title_Locations_s[0],TitlePrefix_d + Title_Locations_d[0]])
            else:
                titles.extend([TitlePrefix_s + Title_Locations_s[1],TitlePrefix_s + Title_Locations_s[3],
                               TitlePrefix_d + Title_Locations_d[1],TitlePrefix_d + Title_Locations_d[3]])
            for iTitle in range(0,len(titles)):
                titles[iTitle] += '\nCumulative Steric Sea Level\nversus Depth'
            FileName = FileNamePrefix_SubPlots + '_%d_%d_CumulativeStericSeaLevelVersusDepth' %(yrs[1],yrs[3])
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                legendposition = 'lower right'
                CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows_2,nCols,StericSeaLevelCumSums,
                                                 zCenters,linewidths,linestyles_1,colors_1,markers,markertypes_1,
                                                 markersizes_1,xLabels,yLabels,labelfontsizes_1,labelpads,tickfontsizes,
                                                 legends,legendfontsize,legendposition,titles,titlefontsize_1,SaveAsPDF,
                                                 FileName,Show,fig_size=fig_size_1,legendWithinBox=True,
                                                 legendpads=legendpads,hspace=0.0,wspace=0.25)
            else:        
                CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,StericSeaLevelCumSums,zCenters,
                                           linewidths,linestyles_2,colors_2,markers,markertypes_2,markersizes_2,xLabels,
                                           yLabels,labelfontsizes_2,labelpads,tickfontsizes,titles,titlefontsize_2,
                                           SaveAsPDF,FileName,Show,fig_size=fig_size_2,hspace=hspace+0.075,
                                           wspace=wspace)
            # Now plot the change between two different times.
            ChangeInTemperatures = []
            ChangeInSalinities = []
            ChangeInRhoByRhoRefs = []
            ChangeInStericSeaLevels = []
            ChangeInStericSeaLevelCumSums = []
            ChangeInTemperatures.extend([Temperatures_s[1]-Temperatures_s[0],Temperatures_s[3]-Temperatures_s[2],
                                         Temperatures_d[1]-Temperatures_d[0],Temperatures_d[3]-Temperatures_d[2]])
            ChangeInSalinities.extend([Salinities_s[1]-Salinities_s[0],Salinities_s[3]-Salinities_s[2],
                                       Salinities_d[1]-Salinities_d[0],Salinities_d[3]-Salinities_d[2]])
            ChangeInRhoByRhoRefs.extend([(RhoByRhoRefs_s[1]-RhoByRhoRefs_s[0])*10**5,
                                         (RhoByRhoRefs_s[3]-RhoByRhoRefs_s[2])*10**5,
                                         (RhoByRhoRefs_d[1]-RhoByRhoRefs_d[0])*10**5,
                                         (RhoByRhoRefs_d[3]-RhoByRhoRefs_d[2])*10**5])
            ChangeInStericSeaLevels.extend([StericSeaLevels_s[1]-StericSeaLevels_s[0],
                                            StericSeaLevels_s[3]-StericSeaLevels_s[2],
                                            StericSeaLevels_d[1]-StericSeaLevels_d[0],
                                            StericSeaLevels_d[3]-StericSeaLevels_d[2]])
            ChangeInStericSeaLevelCumSums.extend([StericSeaLevelCumSums_s[1]-StericSeaLevelCumSums_s[0],
                                                  StericSeaLevelCumSums_s[3]-StericSeaLevelCumSums_s[2],
                                                  StericSeaLevelCumSums_d[1]-StericSeaLevelCumSums_d[0],
                                                  StericSeaLevelCumSums_d[3]-StericSeaLevelCumSums_d[2]])
            xLabel = 'Change in Temperature (Celsius)'
            xLabels = []
            xLabels.extend([xLabel,xLabel,xLabel,xLabel])
            titles = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                titles.extend([TitlePrefix_s + Title_Locations_s[0],TitlePrefix_d + Title_Locations_d[0]])
            else:
                titles.extend([TitlePrefix_s + Title_Locations_s[1],TitlePrefix_s + Title_Locations_s[3],
                               TitlePrefix_d + Title_Locations_d[1],TitlePrefix_d + Title_Locations_d[3]])
            for iTitle in range(0,len(titles)):
                titles[iTitle] += '\nChange in Temperature versus Depth'
            FileName = FileNamePrefix_SubPlots + '_%d_%d_TemperatureChangeVersusDepth' %(yrs[1],yrs[3])
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                legendposition = 'lower center'
                CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows_2,nCols,ChangeInTemperatures,zCenters,
                                                 linewidths,linestyles_1,colors_1,markers,markertypes_1,markersizes_1,
                                                 xLabels,yLabels,labelfontsizes_1,labelpads,tickfontsizes,legends,
                                                 legendfontsize,legendposition,titles,titlefontsize_1,SaveAsPDF,
                                                 FileName,Show,fig_size=fig_size_1,legendWithinBox=True,
                                                 legendpads=legendpads,hspace=0.0,wspace=0.25)
            else:
                CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,ChangeInTemperatures,zCenters,
                                           linewidths,linestyles_2,colors_2,markers,markertypes_2,markersizes_2,xLabels,
                                           yLabels,labelfontsizes_2,labelpads,tickfontsizes,titles,titlefontsize_2,
                                           SaveAsPDF,FileName,Show,fig_size=fig_size_2,hspace=hspace,wspace=wspace)
            xLabel = 'Change in Salinity (gm per kg)'
            xLabels = []
            xLabels.extend([xLabel,xLabel,xLabel,xLabel])
            titles = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                titles.extend([TitlePrefix_s + Title_Locations_s[0],TitlePrefix_d + Title_Locations_d[0]])
            else:
                titles.extend([TitlePrefix_s + Title_Locations_s[1],TitlePrefix_s + Title_Locations_s[3],
                               TitlePrefix_d + Title_Locations_d[1],TitlePrefix_d + Title_Locations_d[3]])
            for iTitle in range(0,len(titles)):
                titles[iTitle] += '\nChange in Salinity versus Depth'
            FileName = FileNamePrefix_SubPlots + '_%d_%d_SalinityChangeVersusDepth' %(yrs[1],yrs[3])
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                legendposition = 'lower right'
                CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows_2,nCols,ChangeInSalinities,zCenters,
                                                 linewidths,linestyles_1,colors_1,markers,markertypes_1,markersizes_1,
                                                 xLabels,yLabels,labelfontsizes_1,labelpads,tickfontsizes,legends,
                                                 legendfontsize,legendposition,titles,titlefontsize_1,SaveAsPDF,
                                                 FileName,Show,fig_size=fig_size_1,legendWithinBox=True,
                                                 legendpads=legendpads,hspace=0.0,wspace=0.25)
            else:
                CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,ChangeInSalinities,zCenters,
                                           linewidths,linestyles_2,colors_2,markers,markertypes_2,markersizes_2,xLabels,
                                           yLabels,labelfontsizes_2,labelpads,tickfontsizes,titles,titlefontsize_2,
                                           SaveAsPDF,FileName,Show,fig_size=fig_size_2,hspace=hspace,wspace=wspace)
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                xLabel = 'Change in Ratio of Density\nto Reference Density x 10^5'
            else:
                xLabel = 'Change in Ratio of Density to Reference Density x 10^5'
            xLabels = []
            xLabels.extend([xLabel,xLabel,xLabel,xLabel])
            titles = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                titles.extend([TitlePrefix_s + Title_Locations_s[0],TitlePrefix_d + Title_Locations_d[0]])
            else:
                titles.extend([TitlePrefix_s + Title_Locations_s[1],TitlePrefix_s + Title_Locations_s[3],
                               TitlePrefix_d + Title_Locations_d[1],TitlePrefix_d + Title_Locations_d[3]])
            for iTitle in range(0,len(titles)):
                titles[iTitle] += '\nChange in Ratio of Density to\nReference Density versus Depth'
            FileName = FileNamePrefix_SubPlots + '_%d_%d_DensityByReferenceDensityChangeVersusDepth' %(yrs[1],yrs[3])
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                legendposition = 'lower center'
                CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows_2,nCols,ChangeInRhoByRhoRefs,zCenters,
                                                 linewidths,linestyles_1,colors_1,markers,markertypes_1,markersizes_1,
                                                 xLabels,yLabels,labelfontsizes_1,labelpads,tickfontsizes,legends,
                                                 legendfontsize,legendposition,titles,titlefontsize_1,SaveAsPDF,
                                                 FileName,Show,fig_size=fig_size_1,legendWithinBox=True,
                                                 legendpads=legendpads,hspace=0.0,wspace=0.25)
            else:
                CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,ChangeInRhoByRhoRefs,zCenters,
                                           linewidths,linestyles_2,colors_2,markers,markertypes_2,markersizes_2,xLabels,
                                           yLabels,labelfontsizes_2,labelpads,tickfontsizes,titles,titlefontsize_2,
                                           SaveAsPDF,FileName,Show,fig_size=fig_size_2,hspace=hspace+0.075,
                                           wspace=wspace)
            xLabel = 'Change in Contribution to Steric Sea Level (m)'
            xLabels = []
            xLabels.extend([xLabel,xLabel,xLabel,xLabel])
            titles = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                titles.extend([TitlePrefix_s + Title_Locations_s[0],TitlePrefix_d + Title_Locations_d[0]])
            else:
                titles.extend([TitlePrefix_s + Title_Locations_s[1],TitlePrefix_s + Title_Locations_s[3],
                               TitlePrefix_d + Title_Locations_d[1],TitlePrefix_d + Title_Locations_d[3]])
            for iTitle in range(0,len(titles)):
                titles[iTitle] += '\nChange in Contribution to\nSteric Sea Level versus Depth'
            FileName = FileNamePrefix_SubPlots + '_%d_%d_ContributionToStericSeaLevelChangeVersusDepth' %(yrs[1],yrs[3])
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                legendposition = 'lower left'
                CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows_2,nCols,ChangeInStericSeaLevels,
                                                 zCenters,linewidths,linestyles_1,colors_1,markers,markertypes_1,
                                                 markersizes_1,xLabels,yLabels,labelfontsizes_1,labelpads,tickfontsizes,
                                                 legends,legendfontsize,legendposition,titles,titlefontsize_1,SaveAsPDF,
                                                 FileName,Show,fig_size=fig_size_1,legendWithinBox=True,
                                                 legendpads=legendpads,hspace=0.0,wspace=0.25)
            else:
                CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,ChangeInStericSeaLevels,zCenters,
                                           linewidths,linestyles_2,colors_2,markers,markertypes_2,markersizes_2,xLabels,
                                           yLabels,labelfontsizes_2,labelpads,tickfontsizes,titles,titlefontsize_2,
                                           SaveAsPDF,FileName,Show,fig_size=fig_size_2,hspace=hspace+0.075,
                                           wspace=wspace)
            xLabel = 'Change in Cumulative Steric Sea Level (m)'
            xLabels = []
            xLabels.extend([xLabel,xLabel,xLabel,xLabel])
            titles = []
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                titles.extend([TitlePrefix_s + Title_Locations_s[0],TitlePrefix_d + Title_Locations_d[0]])
            else:
                titles.extend([TitlePrefix_s + Title_Locations_s[1],TitlePrefix_s + Title_Locations_s[3],
                               TitlePrefix_d + Title_Locations_d[1],TitlePrefix_d + Title_Locations_d[3]])
            for iTitle in range(0,len(titles)):
                titles[iTitle] += '\nChange in Cumulative Steric Sea Level\nversus Depth'
            FileName = FileNamePrefix_SubPlots + '_%d_%d_CumulativeStericSeaLevelChangeVersusDepth' %(yrs[1],yrs[3])
            if PlotPreIndustrialAndHistorialDataOnSameGraph:
                legendposition = 'lower left'
                CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows_2,nCols,ChangeInStericSeaLevelCumSums,
                                                 zCenters,linewidths,linestyles_1,colors_1,markers,markertypes_1,
                                                 markersizes_1,xLabels,yLabels,labelfontsizes_1,labelpads,tickfontsizes,
                                                 legends,legendfontsize,legendposition,titles,titlefontsize_1,SaveAsPDF,
                                                 FileName,Show,fig_size=fig_size_1,legendWithinBox=True,
                                                 legendpads=legendpads,hspace=0.0,wspace=0.25)
            else:
                CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,ChangeInStericSeaLevelCumSums,
                                           zCenters,linewidths,linestyles_2,colors_2,markers,markertypes_2,
                                           markersizes_2,xLabels,yLabels,labelfontsizes_2,labelpads,tickfontsizes,
                                           titles,titlefontsize_2,SaveAsPDF,FileName,Show,fig_size=fig_size_2,
                                           hspace=hspace+0.075,wspace=wspace)
    if display_elapsed_time:
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_minutes = np.floor(elapsed_time/60.0)
        elapsed_time_seconds = np.mod(elapsed_time,60.0)
        print('The total elapsed time is %d minutes %d seconds.' %(elapsed_time_minutes,elapsed_time_seconds))
        
        
do_TestComputeContributionToStericSeaLevelAsAFunctionOfDepthAtGivenLocations = False
if do_TestComputeContributionToStericSeaLevelAsAFunctionOfDepthAtGivenLocations:
    PlotPreIndustrialAndHistorialDataOnSameGraph = True
    TestComputeContributionToStericSeaLevelAsAFunctionOfDepthAtGivenLocations(
    PlotPreIndustrialAndHistorialDataOnSameGraph)