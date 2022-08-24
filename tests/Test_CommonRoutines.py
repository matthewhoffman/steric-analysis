"""
Name: Test_CommonRoutines.py
Author: Sid Bishnu
Details: As the name implies, this script tests the various functions of ../src/CommonRoutines.py.
"""


import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.realpath('..') + '/src/')
from IPython.utils import io
with io.capture_output() as captured:
    import CommonRoutines as CR
    
    
def TestScatterAndContourPlotsAsSubPlots(plot_type):
    output_directory = '../output/'
    xLeft = -1.0
    xRight = 1.0
    nX = 100
    x = np.linspace(xLeft,xRight,nX+1)
    yBottom = -1.0
    yTop = 1.0
    nY = 100
    y = np.linspace(yBottom,yTop,nY+1)
    nPoints = (nX+1)*(nY+1)
    nRows = 2
    nCols = 2
    nSubPlots = nRows*nCols
    phiUnstructured = np.zeros((nSubPlots,nPoints))
    xUnstructured = np.zeros(nPoints)
    yUnstructured = np.zeros(nPoints)
    for iY in range(0,nY+1):
        for iX in range(0,nX+1):
            i = iY*(nX+1) + iX
            xUnstructured[i] = x[iX]
            yUnstructured[i] = y[iY]
            phiUnstructured[0,i] = xUnstructured[i] + yUnstructured[i]
            phiUnstructured[1,i] = (xUnstructured[i])**2.0 + (yUnstructured[i])**2.0
            phiUnstructured[2,i] = (xUnstructured[i])**3.0 + (yUnstructured[i])**3.0
            phiUnstructured[3,i] = (xUnstructured[i])**4.0 + (yUnstructured[i])**4.0
    markersizes = [1.0,1.0,1.0,1.0]
    nContours = [300,300,300,300]
    labels = ['x','y']
    labelfontsizes = [17.5,17.5]
    labelpads = [10.0,10.0]
    tickfontsizes = [15.0,15.0]
    useGivenColorBarLimits = [False,False,False,False]
    ColorBarLimits = np.zeros((nSubPlots,2))
    nColorBarTicks = 6
    cbarShrinkRatio = 0.65
    titles = ['x + y', 'x^2 + y^2', 'x^3 + y^3', 'x^4 + y^4']
    titlefontsize = 22.5
    SaveAsPDF = True
    FileName = plot_type + 'sAsSubPlots'
    fig_size = [12.0,12.0]
    set_aspect_equal = [False,False,False,False]
    colormaps = [plt.cm.jet,plt.cm.jet,plt.cm.jet,plt.cm.jet]
    cbarlabelformats = ['%.2f','%.2f','%.2f','%.2f']
    cbarfontsize = 13.75
    set_xticks_manually = True
    xticks_set_manually = [-1.0,-0.5,0.0,0.5,1.0]
    set_yticks_manually = True
    yticks_set_manually = [-1.0,-0.5,0.0,0.5,1.0]
    Show = False
    hspace = 0.04 # height of the padding between subplots i.e. the vertical spacing between subplots
    wspace = 0.40 # width of the padding between subplots i.e. the horizontal spacing between subplots
    FigureFormat = 'pdf'
    bbox_inches = 'tight'
    CR.ScatterAndContourPlotsAsSubPlots(plot_type,output_directory,xUnstructured,yUnstructured,nRows,nCols,
                                        phiUnstructured,markersizes,nContours,labels,labelfontsizes,labelpads,
                                        tickfontsizes,useGivenColorBarLimits,ColorBarLimits,nColorBarTicks,
                                        cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,fig_size,
                                        set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,set_xticks_manually,
                                        xticks_set_manually,set_yticks_manually,yticks_set_manually,hspace,wspace,
                                        FigureFormat,bbox_inches)
    
    
TestScatterAndContourPlotsAsSubPlots(plot_type='ScatterPlot')
TestScatterAndContourPlotsAsSubPlots(plot_type='FilledContourPlot')


def TestScatterAndContourPlotsAs3SubPlots(plot_type):
    output_directory = '../output/'
    xLeft = -1.0
    xRight = 1.0
    nX = 100
    x = np.linspace(xLeft,xRight,nX+1)
    yBottom = -1.0
    yTop = 1.0
    nY = 100
    y = np.linspace(yBottom,yTop,nY+1)
    nPoints = (nX+1)*(nY+1)
    nSubPlots = 3
    phiUnstructured = np.zeros((nSubPlots,nPoints))
    xUnstructured = np.zeros(nPoints)
    yUnstructured = np.zeros(nPoints)
    for iY in range(0,nY+1):
        for iX in range(0,nX+1):
            i = iY*(nX+1) + iX
            xUnstructured[i] = x[iX]
            yUnstructured[i] = y[iY]
            phiUnstructured[0,i] = xUnstructured[i] + yUnstructured[i]
            phiUnstructured[1,i] = (xUnstructured[i])**2.0 + (yUnstructured[i])**2.0
            phiUnstructured[2,i] = (xUnstructured[i])**3.0 + (yUnstructured[i])**3.0
    markersizes = [1.0,1.0,1.0]
    nContours = [300,300,300]
    labels = ['x','y']
    labelfontsizes = [17.5,17.5]
    labelpads = [10.0,10.0]
    tickfontsizes = [15.0,15.0]
    useGivenColorBarLimits = [False,False,False]
    ColorBarLimits = np.zeros((nSubPlots,2))
    nColorBarTicks = 6
    cbarShrinkRatio = 0.65
    titles = ['x + y', 'x^2 + y^2', 'x^3 + y^3']
    titlefontsize = 22.5
    SaveAsPDF = True
    FileName = plot_type + 'sAs3SubPlots'
    fig_size = [12.0,12.0]
    set_aspect_equal = [False,False,False]
    colormaps = [plt.cm.jet,plt.cm.jet,plt.cm.jet]
    cbarlabelformats = ['%.2f','%.2f','%.2f']
    cbarfontsize = 13.75
    set_xticks_manually = True
    xticks_set_manually = [-1.0,-0.5,0.0,0.5,1.0]
    set_yticks_manually = True
    yticks_set_manually = [-1.0,-0.5,0.0,0.5,1.0]
    Show = False
    hspace = 0.05 # height of the padding between subplots i.e. the vertical spacing between subplots
    wspace = 1.25 # width of the padding between subplots i.e. the horizontal spacing between subplots
    FigureFormat = 'pdf'
    bbox_inches = 'tight'
    CR.ScatterAndContourPlotsAs3SubPlots(plot_type,output_directory,xUnstructured,yUnstructured,phiUnstructured,
                                         markersizes,nContours,labels,labelfontsizes,labelpads,tickfontsizes,
                                         useGivenColorBarLimits,ColorBarLimits,nColorBarTicks,cbarShrinkRatio,titles,
                                         titlefontsize,SaveAsPDF,FileName,Show,fig_size,set_aspect_equal,colormaps,
                                         cbarlabelformats,cbarfontsize,set_xticks_manually,xticks_set_manually,
                                         set_yticks_manually,yticks_set_manually,hspace,wspace,FigureFormat,bbox_inches)
    

TestScatterAndContourPlotsAs3SubPlots(plot_type='ScatterPlot')
TestScatterAndContourPlotsAs3SubPlots(plot_type='FilledContourPlot')