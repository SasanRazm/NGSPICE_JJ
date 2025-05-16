# NGSPICE_JJ
Example for modeling superconductor circuits with NGSPICE

NGJJSim.py is the main file, you can add your netlist name to "OrgNetlist", output to "Out_file_path", and the output columns you want to plot to "dsets". For example:

-- OrgNetlist = 'PI_AND_HighJc.cir'
-- Out_file_path = 'PiOut.dat'
-- dsets = [0,1,3,5,7,9] 
