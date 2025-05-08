import matplotlib.pyplot as plt
import os

def Plotwaves(data, dsets, pltFile, showPlot, plotTitle):
    # Tile drawing of the JPO data
    
    plotnum = len(dsets) - 1
    timeData = data[:,dsets[0]] * 1e9
    fig, axs = plt.subplots(plotnum, 1, sharex=True, figsize=(8, 12))
    fig.subplots_adjust(hspace=0.05)
    
    plt.title(plotTitle)
    axs[0].set_title(plotTitle)
    
    for plotcntr in range(1,plotnum+1):
        
        LCData = data[:,dsets[plotcntr]] * 1e3
        axs[plotcntr-1].plot(timeData, LCData, label=f'Data{plotcntr}')
        axs[plotcntr-1].set_ylabel('Amplitude [mV]')
        axs[plotcntr-1].legend(loc='upper right', fontsize='small')
        if plotcntr == plotnum:
            axs[plotcntr-1].set_xlabel('Time [ns]')
    
    subfolder = 'plots'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    
    filename = os.path.join(subfolder, pltFile)
    plt.savefig(filename, bbox_inches='tight')
    
    if showPlot:
        plt.show()
    # Clear the current figure for the next iteration
    plt.clf()