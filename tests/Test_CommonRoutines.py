"""
Name: Test_CommonRoutines.py
Author: Sid Bishnu
Details: As the name implies, this script tests the various functions of ../src/CommonRoutines.py.
"""


from operator import isub
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.realpath('..') + '/src/')
from IPython.utils import io
with io.capture_output() as captured:
    import CommonRoutines as CR
    
    
def TestWriteCurve1D():
    x = np.arange(0.0,10.0,1.0)
    y = np.arange(0.0,20.0,2.0)
    output_directory = '../output/'
    CR.WriteCurve1D(output_directory,x,y,'TestWriteCurve1D')
    

do_TestWriteCurve1D = False
if do_TestWriteCurve1D:
    TestWriteCurve1D()


def TestReadCurve1D():
    x1 = np.arange(0.0,10.0,1.0)
    y1 = np.arange(0.0,20.0,2.0)
    print('Write to file:')
    for i in range(0,np.size(x1)):
        print('%4.2f %5.2f' %(x1[i],y1[i]))
    output_directory = '../output/'
    CR.WriteCurve1D(output_directory,x1,y1,'TestWriteCurve1D')
    x2, y2 = CR.ReadCurve1D(output_directory,'TestWriteCurve1D.curve')
    print(' ')
    print('Read from file:')
    for i in range(0,np.size(x2)):
        print('%4.2f %5.2f' %(x2[i],y2[i]))
    
    
do_TestReadCurve1D = False
if do_TestReadCurve1D:
    TestReadCurve1D()
    
    
def TestPythonPlot1DSaveAsPDF():
    x = np.arange(0.0,10.0,1.0) # Syntax is x = np.arange(First Point, Last Point, Interval).
    y = np.arange(0.0,20.0,2.0)
    output_directory = '../output/'
    CR.PythonPlot1DSaveAsPDF(output_directory,'regular',x,y,2.0,'-','k',True,'s',10.0,['x','y'],[22.5,22.5],[10.0,10.0],
                             [15.0,15.0],'Python Plot 1D',27.5,True,'PythonPlot1D',False)


do_TestPythonPlot1DSaveAsPDF = False
if do_TestPythonPlot1DSaveAsPDF:
    TestPythonPlot1DSaveAsPDF()
    
    
def TestPythonPlots1DAsSubplots():
    output_directory = '../output/'
    plot_type = 'regular'
    nRows = 2
    nCols = 3
    nSubPlots = nRows*nCols
    x = np.arange(0.0,10.0,1.0) # Syntax is x = np.arange(First Point, Last Point, Interval).
    xAll = []
    yAll = []
    for iSubPlot in range(0,nSubPlots):
        xAll.append(x[:])
        yAll.append(0.5*float(iSubPlot+1)*x[:])
    linewidths = 2.0*np.ones(nSubPlots)
    linestyles = ['-','-','-','-','-','-']
    colors = ['k','k','k','k','k','k']
    markers = np.ones(nSubPlots,dtype=bool)
    markertypes = ['s','s','s','s','s','s']
    markersizes = 10.0*np.ones(nSubPlots)
    xLabels = ['x','x','x','x','x','x']
    yLabels = ['y','y','y','y','y','y']
    labelfontsizes = [17.5,17.5]
    labelpads = [10.0,10.0]
    tickfontsizes = [15.0,15.0]
    titles = ['Python Plot 1','Python Plot 2','Python Plot 3','Python Plot 4','Python Plot 5','Python Plot 6']
    titlefontsize = 22.5
    SaveAsPDF = True
    FileName = 'PythonPlots1DAsSubplots'
    Show = False
    fig_size = [21.0,14.0]
    hspace = 0.35 # height of the padding between subplots i.e. the vertical spacing between subplots
    wspace = 0.25 # width of the padding between subplots i.e. the horizontal spacing between subplots
    CR.PythonPlots1DAsSubplots(output_directory,plot_type,nRows,nCols,xAll,yAll,linewidths,linestyles,colors,markers,
                               markertypes,markersizes,xLabels,yLabels,labelfontsizes,labelpads,tickfontsizes,titles,
                               titlefontsize,SaveAsPDF,FileName,Show,fig_size=fig_size,hspace=hspace,wspace=wspace)


do_TestPythonPlots1DAsSubplots = False
if do_TestPythonPlots1DAsSubplots:
    TestPythonPlots1DAsSubplots()
    
    
def TestPythonDoublePlots1DAsSubplots():
    output_directory = '../output/'
    plot_type = 'regular'
    nRows = 1
    nCols = 2
    nSubPlots = nRows*nCols*2
    x = np.arange(0.0,10.0,1.0) # Syntax is x = np.arange(First Point, Last Point, Interval).
    xAll = []
    yAll = []
    for iSubPlot in range(0,nSubPlots):
        xAll.append(x[:])
        yAll.append(0.5*float(iSubPlot+1)*x[:])
    linewidths = 2.0*np.ones(nSubPlots)
    linestyles = ['-','--','-','--']
    colors = ['r','b','r','b']
    markers = np.ones(nSubPlots,dtype=bool)
    markertypes = ['s','o','s','o']
    markersizes = [10.0,12.5,10.0,12.5]
    xLabels = ['x','x']
    yLabels = ['y','y']
    labelfontsizes = [22.5,22.5]
    labelpads = [10.0,10.0]
    tickfontsizes = [15.0,15.0]
    legends = ['y11','y12','y21','y22']
    legendfontsize = 17.5
    legendposition = 'upper left'
    titles = ['Python Plots 1','Python Plots 2']
    titlefontsize = 27.5
    SaveAsPDF = True
    FileName = 'PythonDoublePlots1DAsSubplots'
    Show = False
    fig_size = [20.0,9.25]
    legendWithinBox = True
    legendpads = [1.0,0.5]
    hspace = 0.0 # height of the padding between subplots i.e. the vertical spacing between subplots
    wspace = 0.25 # width of the padding between subplots i.e. the horizontal spacing between subplots
    CR.PythonDoublePlots1DAsSubplots(output_directory,plot_type,nRows,nCols,xAll,yAll,linewidths,linestyles,colors,
                                     markers,markertypes,markersizes,xLabels,yLabels,labelfontsizes,labelpads,
                                     tickfontsizes,legends,legendfontsize,legendposition,titles,titlefontsize,SaveAsPDF,
                                     FileName,Show,fig_size=fig_size,legendWithinBox=legendWithinBox,
                                     legendpads=legendpads,hspace=hspace,wspace=wspace)


do_TestPythonDoublePlots1DAsSubplots = False
if do_TestPythonDoublePlots1DAsSubplots:
    TestPythonDoublePlots1DAsSubplots()
    
    
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
    FileFormat = 'pdf'
    bbox_inches = 'tight'
    CR.ScatterAndContourPlotsAsSubPlots(plot_type,output_directory,xUnstructured,yUnstructured,nRows,nCols,
                                        phiUnstructured,markersizes,nContours,labels,labelfontsizes,labelpads,
                                        tickfontsizes,useGivenColorBarLimits,ColorBarLimits,nColorBarTicks,
                                        cbarShrinkRatio,titles,titlefontsize,SaveAsPDF,FileName,Show,fig_size,
                                        set_aspect_equal,colormaps,cbarlabelformats,cbarfontsize,set_xticks_manually,
                                        xticks_set_manually,set_yticks_manually,yticks_set_manually,hspace,wspace,
                                        FileFormat,bbox_inches)
    
    
do_TestScatterAndContourPlotsAsSubPlots_ScatterPlot = False
if do_TestScatterAndContourPlotsAsSubPlots_ScatterPlot:
    TestScatterAndContourPlotsAsSubPlots(plot_type='ScatterPlot')
    
    
do_TestScatterAndContourPlotsAsSubPlots_FilledContourPlot = False
if do_TestScatterAndContourPlotsAsSubPlots_FilledContourPlot:
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
    FileFormat = 'pdf'
    bbox_inches = 'tight'
    CR.ScatterAndContourPlotsAs3SubPlots(plot_type,output_directory,xUnstructured,yUnstructured,phiUnstructured,
                                         markersizes,nContours,labels,labelfontsizes,labelpads,tickfontsizes,
                                         useGivenColorBarLimits,ColorBarLimits,nColorBarTicks,cbarShrinkRatio,titles,
                                         titlefontsize,SaveAsPDF,FileName,Show,fig_size,set_aspect_equal,colormaps,
                                         cbarlabelformats,cbarfontsize,set_xticks_manually,xticks_set_manually,
                                         set_yticks_manually,yticks_set_manually,hspace,wspace,FileFormat,bbox_inches)
    

do_TestScatterAndContourPlotsAs3SubPlots_ScatterPlot = False
if do_TestScatterAndContourPlotsAs3SubPlots_ScatterPlot:
    TestScatterAndContourPlotsAs3SubPlots(plot_type='ScatterPlot')
    
    
do_TestScatterAndContourPlotsAs3SubPlots_FilledContourPlot = False
if do_TestScatterAndContourPlotsAs3SubPlots_FilledContourPlot:
    TestScatterAndContourPlotsAs3SubPlots(plot_type='FilledContourPlot')