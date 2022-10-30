"""
Name: StericSeaLevelAgainstDepth.py
Authors: Sid Bishnu 
Details: This script computes the contribution to steric sea level as a function of depth.
"""


import sys
import numpy as np
from IPython.utils import io
with io.capture_output() as captured:
    import CommonRoutines as CR
    
    
myGlobalConstants = CR.GlobalConstants()


def ObtainDistanceBetweenTwoPointsOnEarthWithGivenLatitudeAndLongitude(Latitudes,Longitudes):
# Note that Latitudes and Longitudes should be provided in radians.
    # Haversine formula
    LongitudeDifference = Longitudes[1] - Longitudes[0]
    LatitudeDifference = Latitudes[1] - Latitudes[0]
    a = (np.sin(LatitudeDifference/2.0)**2.0 
         + np.cos(Latitudes[0])*np.cos(Latitudes[1])*np.sin(LongitudeDifference/2.0)**2.0)
    c = 2.0*np.arcsin(np.sqrt(a))
    # Calculate the result.
    Distance = c*myGlobalConstants.EarthRadius
    return Distance


def ObtainCellIndexNearestToASpecificLocation(fmesh,Latitude,Longitude):
# Note that Latitude and Longitude should be provided in radians.
    pii = myGlobalConstants.pii
    latCell = fmesh.variables['latCell'][:]
    lonCell = fmesh.variables['lonCell'][:]
    idx = np.nonzero(latCell<99999999999999999)[0] # global ocean
    DistanceFromASpecificLocation = np.zeros(len(idx))
    for i in idx:
        Latitudes = np.array([Latitude,latCell[i]])
        Longitudes = np.array([Longitude,lonCell[i]])
        DistanceFromASpecificLocation[i] = (
        ObtainDistanceBetweenTwoPointsOnEarthWithGivenLatitudeAndLongitude(Latitudes,Longitudes))
    DesiredIndex = np.argmin(DistanceFromASpecificLocation)
    MinimumDistance = DistanceFromASpecificLocation[DesiredIndex]
    print('Given Location: Latitude = %.1f degrees and Longitude = %.1f degrees.' 
          %(Latitude*180.0/pii,Longitude*180.0/pii))
    print('The minimum distance of a cell center from the given location is %.3f km.' %(MinimumDistance/1000.0))
    return DesiredIndex
            
            
def ObtainCellIndicesWithinGivenRadiusOfASpecificLocation(fmesh,Latitude,Longitude,Radius):
    latCell = fmesh.variables['latCell'][:]
    lonCell = fmesh.variables['lonCell'][:]
    idx = np.nonzero(latCell<99999999999999999)[0] # global ocean
    DesiredIndicesMaximum = np.zeros(len(idx),dtype=int)
    cnt = -1
    for i in idx:
        Latitudes = np.array([Latitude,latCell[i]])
        Longitudes = np.array([Longitude,lonCell[i]])
        DistanceFromASpecificLocation = (
        ObtainDistanceBetweenTwoPointsOnEarthWithGivenLatitudeAndLongitude(Latitudes,Longitudes))
        if DistanceFromASpecificLocation <= Radius:
            cnt += 1
            DesiredIndicesMaximum[cnt] = i
    DesiredIndices = np.zeros(cnt+1,dtype=int)                             
    DesiredIndices[:] = DesiredIndicesMaximum[0:cnt+1]
    return DesiredIndices


def ComputeContributionToStericSeaLevelAsAFunctionOfDepth(fmesh,file,NearestToASpecificLocation=False,
                                                          Latitude=0.0,Longitude=0.0,
                                                          AverageWithinWithinGivenRadius=False,Radius=0.0):
    rho_ref = myGlobalConstants.rho_ref
    latCell = fmesh.variables['latCell'][:]
    bottomDepth = fmesh.variables['bottomDepth'][:]
    maxLevelCell = fmesh.variables['maxLevelCell'][:]
    idx = np.nonzero(latCell<99999999999999999)[0] # global ocean
    EchoNumberOfCells = True
    if EchoNumberOfCells:
        print("Found {} cells in idx." .format(len(idx)))
    rho = file.variables['timeMonthly_avg_density'][0,:,:]
    nVertLevels = rho.shape[1]
    layerThickness = file.variables['timeMonthly_avg_layerThickness'][0,:,:]
    temperature = file.variables['timeMonthly_avg_activeTracers_temperature'][0,:,:]
    salinity = file.variables['timeMonthly_avg_activeTracers_salinity'][0,:,:]
    ssh = file.variables['timeMonthly_avg_ssh'][0,:]
    PressureAdjustedSSH = file.variables['timeMonthly_avg_pressureAdjustedSSH'][0,:]
    if NearestToASpecificLocation:
        DesiredIndex = ObtainCellIndexNearestToASpecificLocation(fmesh,Latitude,Longitude)
        DesiredIndices = np.array([DesiredIndex])
    elif AverageWithinWithinGivenRadius:
        DesiredIndices = ObtainCellIndicesWithinGivenRadiusOfASpecificLocation(fmesh,Latitude,Longitude,Radius)
    nDesiredIndices = len(DesiredIndices)
    print('nDesiredIndices = %d' %nDesiredIndices)
    PrintDesiredIndices = False
    if PrintDesiredIndices:
        print('Outside for loop')
        print('DesiredIndices are')
        for i in range(0,nDesiredIndices):
            print('%3d: %6d' %(i,DesiredIndices[i]))
        print('Inside for loop')
    zCenters = np.zeros((nDesiredIndices,nVertLevels))
    zCenter = np.zeros(nVertLevels)
    Temperatures = np.zeros((nDesiredIndices,nVertLevels))
    Temperature = np.zeros(nVertLevels)
    Salinities = np.zeros((nDesiredIndices,nVertLevels))
    Salinity = np.zeros(nVertLevels)
    RhoByRhoRefs = np.zeros((nDesiredIndices,nVertLevels))
    RhoByRhoRef = np.zeros(nVertLevels)
    StericSeaLevels = np.zeros((nDesiredIndices,nVertLevels))
    StericSeaLevel = np.zeros(nVertLevels)
    StericSeaLevel_UnphysicalValues_LowerLimit = 990.0
    nDesiredCellsPerLevel = np.zeros(nVertLevels)
    MaxLevelOfDesiredCellsMaximum = 0
    MaxLevelOfDesiredCellsMinimum = 10**6
    for i in range(0,nDesiredIndices):
        DesiredIndex = DesiredIndices[i]
        if PrintDesiredIndices:
            print('DesiredIndex is')
            print('%3d: %6d' %(i,DesiredIndex))
        BottomDepthOfDesiredCell = bottomDepth[DesiredIndex]
        MaxLevelOfDesiredCell = maxLevelCell[DesiredIndex]
        if MaxLevelOfDesiredCell > MaxLevelOfDesiredCellsMaximum:
            MaxLevelOfDesiredCellsMaximum = MaxLevelOfDesiredCell
        if MaxLevelOfDesiredCell < MaxLevelOfDesiredCellsMinimum:
            MaxLevelOfDesiredCellsMinimum = MaxLevelOfDesiredCell
        SSHOfDesiredCell = ssh[DesiredIndex]
        PressureAdjustedSSHOfDesiredCell = PressureAdjustedSSH[DesiredIndex]
        thicknessSum = layerThickness[DesiredIndex,0:MaxLevelOfDesiredCell].sum()
        thicknessCumSum = layerThickness[DesiredIndex,0:MaxLevelOfDesiredCell].cumsum()
        zSurf = thicknessSum - BottomDepthOfDesiredCell
        zLayerBot = zSurf - thicknessCumSum 
        zCenters[i,0:MaxLevelOfDesiredCell] = zLayerBot + 0.5*layerThickness[DesiredIndex,0:MaxLevelOfDesiredCell] 
        for k in range(0,nVertLevels):
            if k < MaxLevelOfDesiredCell:
                nDesiredCellsPerLevel[k] += 1
                RhoOfDesiredCell = rho[DesiredIndex,k]
                RhoByRhoRefs[i,k] = RhoOfDesiredCell/rho_ref
                Temperatures[i,k] = temperature[DesiredIndex,k]
                Salinities[i,k] = salinity[DesiredIndex,k]
                LayerThicknessOfDesiredCell = layerThickness[DesiredIndex,k]
                StericSeaLevels[i,k] = -1.0/rho_ref*(RhoOfDesiredCell*LayerThicknessOfDesiredCell)
                # Check for unphysical values.
                if StericSeaLevels[i,k] > StericSeaLevel_UnphysicalValues_LowerLimit:
                    print('Unphysical value of steric sea level detected!')
                    print('i = %d, DesiredIndex = %d, nVertLevels = %d, k = %d' %(i,DesiredIndex,nVertLevels,k))
                    print('BottomDepthOfDesiredCell = %d, MaxLevelOfDesiredCell = %d' 
                          %(BottomDepthOfDesiredCell,MaxLevelOfDesiredCell))
                    print('SSHOfDesiredCell = %.6g, PressureAdjustedSSH = %.6g' 
                          %(SSHOfDesiredCell,PressureAdjustedSSHOfDesiredCell))
                    print('RhoOfDesiredCell = %.6g, LayerThicknessOfDesiredCell = %.6g' 
                          %(RhoOfDesiredCell,LayerThicknessOfDesiredCell))
                    sys.exit()
        # We now take into consideration, the depression due to sea-ice loading in the steric contribution to SSH.
        RhoOfDesiredCellAtSurface = rho[DesiredIndex,0]
        StericSeaLevels[i,0] += -1.0/rho_ref*RhoOfDesiredCellAtSurface*(PressureAdjustedSSHOfDesiredCell 
                                                                        - SSHOfDesiredCell)
        PrintMaxLevelOfDesiredCellsMaximumAndMinimum = False
        if PrintMaxLevelOfDesiredCellsMaximumAndMinimum:
            print('nVertLevels = %d, MaxLevelOfDesiredCellsMaximum = %d, MaxLevelOfDesiredCellsMinimum = %d' 
                  %(nVertLevels,MaxLevelOfDesiredCellsMaximum,MaxLevelOfDesiredCellsMinimum))
    for k in range(0,MaxLevelOfDesiredCellsMaximum):
        zCenter[k] = (zCenters[:,k].sum())/nDesiredCellsPerLevel[k]
        Temperature[k] = (Temperatures[:,k].sum())/nDesiredCellsPerLevel[k]
        Salinity[k] = (Salinities[:,k].sum())/nDesiredCellsPerLevel[k]
        RhoByRhoRef[k] = (RhoByRhoRefs[:,k].sum())/nDesiredCellsPerLevel[k]
        StericSeaLevel[k] = (StericSeaLevels[:,k].sum())/nDesiredCellsPerLevel[k]
    StericSeaLevelCumSum = StericSeaLevel[:].cumsum()
    return (zCenter[0:MaxLevelOfDesiredCellsMaximum-1],Temperature[0:MaxLevelOfDesiredCellsMaximum-1],
            Salinity[0:MaxLevelOfDesiredCellsMaximum-1],RhoByRhoRef[0:MaxLevelOfDesiredCellsMaximum-1],
            StericSeaLevel[0:MaxLevelOfDesiredCellsMaximum-1],StericSeaLevelCumSum[0:MaxLevelOfDesiredCellsMaximum-1])