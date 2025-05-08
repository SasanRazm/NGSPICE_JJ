import numpy as np
import subprocess
import time, os
import re

def OutputRM(file_path):
    # Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print(f"The file {file_path} has been deleted.")
    else:
        print(f"The file {file_path} does not exist.")

def Add_thermal_noise(filename):
    """
    Replaces resistor lines in a SPICE netlist with rthermal subcircuit instances.

        .subckt rthermal n1 n2 rval=1
        VNoiw n3 0 DC 0 TRNOISE(1 0.1ps 0 0)
        Rthermal1 n3 0 1
        Rthermal2 n1 n2 {rval}
        B1 n1 n2 I = v(n3) * sqrt(1e13 * 4 * KB * 4.2 / {rval})
        .ends
    """
    with open(filename, 'r') as f:
        netlist = f.read()

    # Regex to match resistor lines: Rname node1 node2 value
    resistor_pattern = re.compile(r'^\s*(R\w+)\s+(\S+)\s+(\S+)\s+([\d.eE+-]+[a-zA-Z]*)\s*$', re.MULTILINE)

    def subckt_replacement(match):
        rname, n1, n2, rval = match.groups()
        if (rname == "Rthermal1") | (rname == "Rthermal2") | (rname == "Rleak"):
            return f"{rname} {n1} {n2} {rval}"
        else:
            return f"X{rname} {n1} {n2} rthermal rval={rval}"

    modified_netlist = resistor_pattern.sub(subckt_replacement, netlist)
    if '.subckt rthermal' not in modified_netlist:
        rthermal_subckt = (
            "\n* Subcircuit to model resistor with thermal noise\n"
            ".subckt rthermal n1 n2 rval=1\n"
            "VNoiw n3 0 DC 0 TRNOISE(1 0.1p 0 0)\n"
            "Rthermal1 n3 0 1\n"
            "Rthermal2 n1 n2 {rval}\n"
            "B1 n1 n12I = v(n3) * sqrt(1e13 * 4 * KB * 4.2 / {rval})\n"
            ".ends\n"
        )
        modified_netlist += rthermal_subckt
        
    base, ext = os.path.splitext(filename)
    output_filename = f"{base}_modified{ext}"
    
    with open(output_filename, 'w') as f:
        f.write(modified_netlist)
    
    print(f"Modified netlist written to: {output_filename}")
    return output_filename
       
def RunSpice(OrgNetlist, outputfilename, AddNoise):
    
    #SimCommand = f'ngspice {OrgNetlist}'
    #cmdout = subprocess.getoutput(SimCommand)
    
    if AddNoise:
        ModNetlist = Add_thermal_noise(OrgNetlist)
        OrgNetlist = ModNetlist
        

    SimCommand = ['ngspice', OrgNetlist]
    process = subprocess.Popen(SimCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    start_time = time.time()
    counter = 0

    while process.poll() is None:
        elapsed_time = int(time.time() - start_time)
        print(f"Elapsed Time: {elapsed_time} seconds", end='\r')  # \r is used to overwrite the same line in the terminal
        time.sleep(1)
        counter += 1

    print("\n Simulation finished.")

    # if printon:
    #     print(cmdout)

    
    if os.path.exists(outputfilename):
        data = np.loadtxt(outputfilename)
    else:
        print("************************************")
        print("*** Bad Data, simulation failed! ***")
        print("************************************")
        data = np.loadtxt('sample.dat')
        
    return data