"""
Name: CommonRoutines.py
Author: Sid Bishnu
Details: This script contains customized functions for writing output to text files, plotting figures etc.
"""


from operator import isub
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os


class GlobalConstants:
    
    def __init__(myGlobalConstants):
        myGlobalConstants.pii = 4.0*np.arctan(1.0)
        myGlobalConstants.g = 9.8101
        myGlobalConstants.EarthRadius = 6371.0*1000.0
        # Define rho_ref from e.g. Griffies et al. (2014) Eq. 54. The results are not sensitive to the choice because
        # the choices (and their impact on the results) only vary by ~1%. Griffies uses 1035. See Eq. 6.
        myGlobalConstants.rho_ref = 1035.0 # reference Boussinesq ocean density
        myGlobalConstants.rho_sw = 1026.0 # E3SM rho_sw i.e. average ocean density in E3SM


def WriteCurve1D(output_directory,x,y,filename):
    cwd = os.getcwd()
    path = cwd + '/' + output_directory + '/'
    if not os.path.exists(path):
        os.mkdir(path) # os.makedir(path)
    os.chdir(path)
    N = len(y)
    filename += '.curve'
    outputfile = open(filename,'w')
    outputfile.write('#phi\n')
    for i in range(0,N):
        outputfile.write('%.15g %.15g\n' %(x[i],y[i]))
    outputfile.close()
    os.chdir(cwd)


def ReadCurve1D(output_directory,filename):
    cwd = os.getcwd()
    path = cwd + '/' + output_directory + '/'
    if not os.path.exists(path):
        os.mkdir(path) # os.makedir(path)
    os.chdir(path)
    data = []
    count = 0
    with open(filename,'r') as infile:
        for line in infile:
            if count != 0:
                data.append(line)
            count += 1
    data = np.loadtxt(data)
    N = data.shape[0]
    x = np.zeros(N)
    y = np.zeros(N)
    for i in range(0,N):
        x[i] = data[i,0]
        y[i] = data[i,1]
    os.chdir(cwd)
    return x, y


def PythonPlot1DSaveAsPDF(output_directory,plot_type,x,y,linewidth,linestyle,color,marker,markertype,markersize,labels,
                          labelfontsizes,labelpads,tickfontsizes,title,titlefontsize,SaveAsPDF,FileName,Show,
                          fig_size=[9.25,9.25],useDefaultMethodToSpecifyTickFontSize=True,drawMajorGrid=True,
                          drawMinorGrid=True,setXAxisLimits=[False,False],xAxisLimits=[0.0,0.0],
                          setYAxisLimits=[False,False],yAxisLimits=[0.0,0.0],plot_label='Python Plot 1D',
                          titlepad=1.035,set_xticks_manually=False,xticks_set_manually=[],FileFormat='pdf'):
    cwd = os.getcwd()
    path = cwd + '/' + output_directory + '/'
    if not os.path.exists(path):
        os.mkdir(path) # os.makedir(path)
    os.chdir(path)    
    fig = plt.figure(figsize=(fig_size[0],fig_size[1])) # Create a figure object.
    ax = fig.add_subplot(111) # Create an axes object in the figure.
    if not(marker):
        markertype = None
    if plot_type == 'regular':
        plt.plot(x,y,linewidth=linewidth,linestyle=linestyle,color=color,marker=markertype,markersize=markersize,
                 label=plot_label)
    elif plot_type == 'semi-log_x':
        plt.semilogx(x,y,linewidth=linewidth,linestyle=linestyle,color=color,marker=markertype,markersize=markersize,
                     label=plot_label)
    elif plot_type == 'semi-log_y':
        plt.semilogy(x,y,linewidth=linewidth,linestyle=linestyle,color=color,marker=markertype,markersize=markersize,
                     label=plot_label)
    elif plot_type == 'log-log':
        plt.loglog(x,y,linewidth=linewidth,linestyle=linestyle,color=color,marker=markertype,markersize=markersize,
                   label=plot_label)
    if plot_type == 'regular':
        if setXAxisLimits[0]:
            ax.set_xlim(bottom=xAxisLimits[0])
        if setXAxisLimits[1]:
            ax.set_xlim(top=xAxisLimits[1])
        if setYAxisLimits[0]:
            ax.set_ylim(bottom=yAxisLimits[0])
        if setYAxisLimits[1]:
            ax.set_ylim(top=yAxisLimits[1])            
    plt.xlabel(labels[0],fontsize=labelfontsizes[0],labelpad=labelpads[0])
    plt.ylabel(labels[1],fontsize=labelfontsizes[1],labelpad=labelpads[1])
    if useDefaultMethodToSpecifyTickFontSize:
        plt.xticks(fontsize=tickfontsizes[0])
        plt.yticks(fontsize=tickfontsizes[1])
    else:
        ax.tick_params(axis='x',labelsize=tickfontsizes[0])
        ax.tick_params(axis='y',labelsize=tickfontsizes[1])
    if set_xticks_manually:
        ax.set_xticks(xticks_set_manually,minor=False)
    ax.set_title(title,fontsize=titlefontsize,fontweight='bold',y=titlepad)
    if drawMajorGrid and not(drawMinorGrid):
        plt.grid(which='major')
    elif not(drawMajorGrid) and drawMinorGrid:
        plt.grid(which='minor')       
    elif drawMajorGrid and drawMinorGrid:
        plt.grid(which='both')
    if SaveAsPDF:
        plt.savefig(FileName+'.'+FileFormat,format=FileFormat,bbox_inches='tight')
    if Show:
        plt.show()
    plt.close()
    os.chdir(cwd)


def PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,xAll,yAll,linewidths,linestyles,colors,markers,
                            markertypes,markersizes,xLabels,yLabels,labelfontsizes,labelpads,tickfontsizes,titles,
                            titlefontsize,SaveAsPDF,FileName,Show,fig_size=[9.25,9.25],
                            useDefaultMethodToSpecifyTickFontSize=True,drawMajorGrid=True,drawMinorGrid=True,hspace=1.5,
                            wspace=0.3,titlepad=1.035,FileFormat='pdf',bbox_inches='tight'):
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
            x = xAll[iSubPlot][:]
            y = yAll[iSubPlot][:]
            if not(markers[iSubPlot]):
                markertype = None
            else:
                markertype = markertypes[iSubPlot]
            if plot_type == 'regular':
                plt.plot(x,y,linewidth=linewidths[iSubPlot],linestyle=linestyles[iSubPlot],color=colors[iSubPlot],
                         marker=markertype,markersize=markersizes[iSubPlot])
            elif plot_type == 'semi-log_x':
                plt.semilogx(x,y,linewidth=linewidths[iSubPlot],linestyle=linestyles[iSubPlot],color=colors[iSubPlot],
                             marker=markertype,markersize=markersizes[iSubPlot])
            elif plot_type == 'semi-log_y':
                plt.semilogy(x,y,linewidth=linewidths[iSubPlot],linestyle=linestyles[iSubPlot],color=colors[iSubPlot],
                             marker=markertype,markersize=markersizes[iSubPlot])
            elif plot_type == 'log-log':
                plt.loglog(x,y,linewidth=linewidths[iSubPlot],linestyle=linestyles[iSubPlot],color=colors[iSubPlot],
                           marker=markertype,markersize=markersizes[iSubPlot])         
            plt.xlabel(xLabels[iSubPlot],fontsize=labelfontsizes[0],labelpad=labelpads[0])
            plt.ylabel(yLabels[iSubPlot],fontsize=labelfontsizes[1],labelpad=labelpads[1])
            if useDefaultMethodToSpecifyTickFontSize:
                plt.xticks(fontsize=tickfontsizes[0])
                plt.yticks(fontsize=tickfontsizes[1])
            else:
                ax.tick_params(axis='x',labelsize=tickfontsizes[0])
                ax.tick_params(axis='y',labelsize=tickfontsizes[1])
            ax.set_title(titles[iSubPlot],fontsize=titlefontsize,fontweight='bold',y=titlepad)
            if drawMajorGrid and not(drawMinorGrid):
                plt.grid(which='major')
            elif not(drawMajorGrid) and drawMinorGrid:
                plt.grid(which='minor')       
            elif drawMajorGrid and drawMinorGrid:
                plt.grid(which='both')
            iSubPlot += 1
    plt.subplots_adjust(hspace=hspace,wspace=wspace)
    if SaveAsPDF:
        plt.savefig(FileName+'.'+FileFormat,format=FileFormat,bbox_inches=bbox_inches)
    if Show:
        plt.show()
    plt.close()
    os.chdir(cwd)
    
    
def PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows,nCols,xAll,yAll,linewidths,linestyles,colors,markers,
                                  markertypes,markersizes,xLabels,yLabels,labelfontsizes,labelpads,tickfontsizes,
                                  legends,legendfontsize,legendposition,titles,titlefontsize,SaveAsPDF,FileName,Show,
                                  fig_size=[9.25,9.25],useDefaultMethodToSpecifyTickFontSize=True,drawMajorGrid=True,
                                  drawMinorGrid=True,legendWithinBox=False,legendpads=[1.0,0.5],hspace=1.5,wspace=0.3,
                                  titlepad=1.035,FileFormat='pdf',bbox_inches='tight'):
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
            iSubPlot1 = 2*iSubPlot
            iSubPlot2 = 2*iSubPlot + 1
            x1 = xAll[iSubPlot1][:]
            y1 = yAll[iSubPlot1][:]
            x2 = xAll[iSubPlot2][:]
            y2 = yAll[iSubPlot2][:]
            if not(markers[iSubPlot1]):
                markertype1 = None
            else:
                markertype1 = markertypes[iSubPlot1]
            if not(markers[iSubPlot2]):
                markertype2 = None
            else:
                markertype2 = markertypes[iSubPlot2]
            if plot_type == 'regular':
                plt.plot(x1,y1,linewidth=linewidths[iSubPlot1],linestyle=linestyles[iSubPlot1],color=colors[iSubPlot1],
                         marker=markertype1,markersize=markersizes[iSubPlot1],label=legends[iSubPlot1])
                plt.plot(x2,y2,linewidth=linewidths[iSubPlot2],linestyle=linestyles[iSubPlot2],color=colors[iSubPlot2],
                         marker=markertype2,markersize=markersizes[iSubPlot2],label=legends[iSubPlot2])
            elif plot_type == 'semi-log_x':
                plt.semilogx(x1,y1,linewidth=linewidths[iSubPlot1],linestyle=linestyles[iSubPlot1],
                             color=colors[iSubPlot1],marker=markertype1,markersize=markersizes[iSubPlot1],
                             label=legends[iSubPlot1])
                plt.semilogx(x2,y2,linewidth=linewidths[iSubPlot2],linestyle=linestyles[iSubPlot2],
                             color=colors[iSubPlot2],marker=markertype2,markersize=markersizes[iSubPlot2],
                             label=legends[iSubPlot2])
            elif plot_type == 'semi-log_y':
                plt.semilogy(x1,y1,linewidth=linewidths[iSubPlot1],linestyle=linestyles[iSubPlot1],
                             color=colors[iSubPlot1],marker=markertype1,markersize=markersizes[iSubPlot1],
                             label=legends[iSubPlot1])
                plt.semilogy(x2,y2,linewidth=linewidths[iSubPlot2],linestyle=linestyles[iSubPlot2],
                             color=colors[iSubPlot2],marker=markertype2,markersize=markersizes[iSubPlot2],
                             label=legends[iSubPlot2])
            elif plot_type == 'log-log':
                plt.loglog(x1,y1,linewidth=linewidths[iSubPlot1],linestyle=linestyles[iSubPlot1],
                           color=colors[iSubPlot1],marker=markertype1,markersize=markersizes[iSubPlot1],
                           label=legends[iSubPlot1])   
                plt.loglog(x2,y2,linewidth=linewidths[iSubPlot2],linestyle=linestyles[iSubPlot2],
                           color=colors[iSubPlot2],marker=markertype2,markersize=markersizes[iSubPlot2],
                           label=legends[iSubPlot2])       
            plt.xlabel(xLabels[iSubPlot],fontsize=labelfontsizes[0],labelpad=labelpads[0])
            plt.ylabel(yLabels[iSubPlot],fontsize=labelfontsizes[1],labelpad=labelpads[1])
            if useDefaultMethodToSpecifyTickFontSize:
                plt.xticks(fontsize=tickfontsizes[0])
                plt.yticks(fontsize=tickfontsizes[1])
            else:
                ax.tick_params(axis='x',labelsize=tickfontsizes[0])
                ax.tick_params(axis='y',labelsize=tickfontsizes[1])
            if legendWithinBox:
                ax.legend(fontsize=legendfontsize,loc=legendposition) 
            else:
                ax.legend(fontsize=legendfontsize,loc=legendposition,bbox_to_anchor=(legendpads[0],legendpads[1]))
            ax.set_title(titles[iSubPlot],fontsize=titlefontsize,fontweight='bold',y=titlepad)
            if drawMajorGrid and not(drawMinorGrid):
                plt.grid(which='major')
            elif not(drawMajorGrid) and drawMinorGrid:
                plt.grid(which='minor')       
            elif drawMajorGrid and drawMinorGrid:
                plt.grid(which='both')
            iSubPlot += 1
    plt.subplots_adjust(hspace=hspace,wspace=wspace)
    if SaveAsPDF:
        plt.savefig(FileName+'.'+FileFormat,format=FileFormat,bbox_inches=bbox_inches)
    if Show:
        plt.show()
    plt.close()
    os.chdir(cwd)


def ScatterAndContourPlotsAsSubPlots(plot_type,output_directory,x,y,nRows,nCols,phi,markersizes,nContours,labels,
                                     labelfontsizes,labelpads,tickfontsizes,useGivenColorBarLimits,ColorBarLimits,
                                     nColorBarTicks,cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,
                                     fig_size,set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,
                                     set_xticks_manually=False,xticks_set_manually=[],set_yticks_manually=False,
                                     yticks_set_manually=[],hspace=1.5,wspace=0.3,FileFormat='pdf',bbox_inches='tight'):
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
        plt.savefig(FileName+'.'+FileFormat,format=FileFormat,bbox_inches=bbox_inches)
    if Show:
        plt.show()
    plt.close()
    os.chdir(cwd)
    
    
def ScatterAndContourPlotsAs3SubPlots(plot_type,output_directory,x,y,phi,markersizes,nContours,labels,labelfontsizes,
                                      labelpads,tickfontsizes,useGivenColorBarLimits,ColorBarLimits,nColorBarTicks,
                                      cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,fig_size,
                                      set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,
                                      set_xticks_manually=False,xticks_set_manually=[],set_yticks_manually=False,
                                      yticks_set_manually=[],hspace=1.5,wspace=0.3,FileFormat='pdf',
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
        plt.savefig(FileName+'.'+FileFormat,format=FileFormat,bbox_inches=bbox_inches)
    if Show:
        plt.show()
    plt.close()
    os.chdir(cwd)