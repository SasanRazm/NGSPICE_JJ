import numpy as np
import RunNGSPICE as RNG
import plotWaveform as PLW

AddNoise = 0
OrgNetlist = 'PI_AND_HighJc.cir'
Out_file_path = 'PiOut.dat'
dsets = [0,1,3,5] 

RNG.OutputRM(Out_file_path)
data = RNG.RunSpice(OrgNetlist, Out_file_path, AddNoise)

pltFile = "JJModel.png"
showPlot = True
plotTitle = "10X JTLs with noise simulation"
PLW.Plotwaves(data, dsets, pltFile, showPlot, plotTitle)
