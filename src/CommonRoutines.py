"""
Name: CommonRoutines.py
Author: Sid Bishnu
Details: This script contains customized functions for writing output to text files, plotting figures etc.
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os


class GlobalConstants:
    
    def __init__(myGlobalConstants):
        myGlobalConstants.pii = 4.0*np.arctan(1.0)
        myGlobalConstants.g = 9.8101
        # Define rho_ref from e.g. Griffies et al. (2014) Eq. 54. The results are not sensitive to the choice because
        # the choices (and their impact on the results) only vary by ~1%. Griffies uses 1035. See Eq. 6.
        myGlobalConstants.rho_ref = 1035.0 # reference Boussinesq ocean density
        myGlobalConstants.rho_sw = 1026.0 # E3SM rho_sw i.e. average ocean density in E3SM


def ScatterAndContourPlotsAsSubPlots(plot_type,output_directory,x,y,nRows,nCols,phi,markersizes,nContours,labels,
                                     labelfontsizes,labelpads,tickfontsizes,useGivenColorBarLimits,ColorBarLimits,
                                     nColorBarTicks,cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,
                                     fig_size,set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,
                                     set_xticks_manually=False,xticks_set_manually=[],set_yticks_manually=False,
                                     yticks_set_manually=[],hspace=1.5,wspace=0.3,FigureFormat='pdf',
                                     bbox_inches='tight'):
    cwd = os.getcwd()
    path = cwd + '/' + output_directory + '/'
    if not os.path.exists(path):
        os.mkdir(path) # os.makedir(path)
    os.chdir(path)
    fig = plt.figure(figsize=(fig_size[0],fig_size[1]))
    iSubPlot = 0
    for iRow in range(0,nRows):
        for iCol in range(0,nCols):
            ax = fig.add_subplot(nRows,nCols,iSubPlot+1)
            if set_aspect_equal[iSubPlot]:
                ax.set_aspect('equal')
            else:
                xMin = min(x[:])
                xMax = max(x[:])
                yMin = min(y[:])
                yMax = max(y[:])        
                aspect_ratio = (xMax - xMin)/(yMax - yMin)
                ax.set_aspect(aspect_ratio,adjustable='box')
            if useGivenColorBarLimits[iSubPlot]:
                cbar_min = ColorBarLimits[iSubPlot,0]
                cbar_max = ColorBarLimits[iSubPlot,1]
            else:
                cbar_min = np.min(phi[iSubPlot,:])
                cbar_max = np.max(phi[iSubPlot,:])
            cbarlabels = np.linspace(cbar_min,cbar_max,num=nColorBarTicks,endpoint=True)
            if plot_type == 'ScatterPlot':
                plt.scatter(x,y,s=markersizes[iSubPlot],c=phi[iSubPlot,:],vmin=cbar_min,vmax=cbar_max,
                            cmap=colormaps[iSubPlot])
            elif plot_type == 'FilledContourPlot':
                FCP = plt.tricontourf(x,y,phi[iSubPlot,:],nContours[iSubPlot],vmin=cbar_min,vmax=cbar_max,
                                      cmap=colormaps[iSubPlot])
            plt.title(titles[iSubPlot],fontsize=titlefontsize,fontweight='bold',y=1.035)
            cbar = plt.colorbar(shrink=cbarShrinkRatio)
            cbar.set_ticks(cbarlabels)
            cbar.set_ticklabels(cbarlabels)
            cbarlabels_final = cbar.get_ticks()
            cbar.ax.set_yticklabels([cbarlabelformats[iSubPlot] %x for x in cbarlabels_final],fontsize=cbarfontsize)
            plt.xlabel(labels[0],fontsize=labelfontsizes[0],labelpad=labelpads[0])
            plt.ylabel(labels[1],fontsize=labelfontsizes[1],labelpad=labelpads[1])
            plt.xticks(fontsize=tickfontsizes[0])
            plt.yticks(fontsize=tickfontsizes[1])
            if set_xticks_manually:
                ax.set_xticks(xticks_set_manually,minor=False)
            if set_yticks_manually:
                ax.set_yticks(yticks_set_manually,minor=False)
            iSubPlot += 1
    plt.subplots_adjust(hspace=hspace,wspace=wspace)
    if SaveAsPDF:
        plt.savefig(FileName+'.'+FigureFormat,format=FigureFormat,bbox_inches=bbox_inches)
    if Show:
        plt.show()
    plt.close()
    os.chdir(cwd)
    
    
def ScatterAndContourPlotsAs3SubPlots(plot_type,output_directory,x,y,phi,markersizes,nContours,labels,labelfontsizes,
                                      labelpads,tickfontsizes,useGivenColorBarLimits,ColorBarLimits,nColorBarTicks,
                                      cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,fig_size,
                                      set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,
                                      set_xticks_manually=False,xticks_set_manually=[],set_yticks_manually=False,
                                      yticks_set_manually=[],hspace=1.5,wspace=0.3,FigureFormat='pdf',
                                      bbox_inches='tight'):
    cwd = os.getcwd()
    path = cwd + '/' + output_directory + '/'
    if not os.path.exists(path):
        os.mkdir(path) # os.makedir(path)
    os.chdir(path)
    fig = plt.figure(figsize=(fig_size[0],fig_size[1]))
    gs = gridspec.GridSpec(4,4,hspace=hspace,wspace=wspace)
    for iSubPlot in range(0,3):
        if iSubPlot == 0:
            ax = plt.subplot(gs[:2,:2])
        elif iSubPlot == 1:
            ax = plt.subplot(gs[:2,2:])
        elif iSubPlot == 2: 
            ax = plt.subplot(gs[2:4, 1:3])
        if set_aspect_equal[iSubPlot]:
            ax.set_aspect('equal')
        else:
            xMin = min(x[:])
            xMax = max(x[:])
            yMin = min(y[:])
            yMax = max(y[:])        
            aspect_ratio = (xMax - xMin)/(yMax - yMin)
            ax.set_aspect(aspect_ratio,adjustable='box')
        if useGivenColorBarLimits[iSubPlot]:
            cbar_min = ColorBarLimits[iSubPlot,0]
            cbar_max = ColorBarLimits[iSubPlot,1]
        else:
            cbar_min = np.min(phi[iSubPlot,:])
            cbar_max = np.max(phi[iSubPlot,:])
        cbarlabels = np.linspace(cbar_min,cbar_max,num=nColorBarTicks,endpoint=True)
        if plot_type == 'ScatterPlot':
            plt.scatter(x,y,s=markersizes[iSubPlot],c=phi[iSubPlot,:],vmin=cbar_min,vmax=cbar_max,
                        cmap=colormaps[iSubPlot])
        elif plot_type == 'FilledContourPlot':
            FCP = plt.tricontourf(x,y,phi[iSubPlot,:],nContours[iSubPlot],vmin=cbar_min,vmax=cbar_max,
                                  cmap=colormaps[iSubPlot])
        plt.title(titles[iSubPlot],fontsize=titlefontsize,fontweight='bold',y=1.035)
        cbar = plt.colorbar(shrink=cbarShrinkRatio)
        cbar.set_ticks(cbarlabels)
        cbar.set_ticklabels(cbarlabels)
        cbarlabels_final = cbar.get_ticks()
        cbar.ax.set_yticklabels([cbarlabelformats[iSubPlot] %x for x in cbarlabels_final],fontsize=cbarfontsize)
        plt.xlabel(labels[0],fontsize=labelfontsizes[0],labelpad=labelpads[0])
        plt.ylabel(labels[1],fontsize=labelfontsizes[1],labelpad=labelpads[1])
        plt.xticks(fontsize=tickfontsizes[0])
        plt.yticks(fontsize=tickfontsizes[1])
        if set_xticks_manually:
            ax.set_xticks(xticks_set_manually,minor=False)
        if set_yticks_manually:
            ax.set_yticks(yticks_set_manually,minor=False)
    if SaveAsPDF:
        plt.savefig(FileName+'.'+FigureFormat,format=FigureFormat,bbox_inches=bbox_inches)
    if Show:
        plt.show()
    plt.close()
    os.chdir(cwd)