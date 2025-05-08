import re
def NetlistGen(OrgNetlist,NewNetlist,ParamName,ParamVal,AddNoise,NoiseTemp):
    
    temperature = NoiseTemp
    ParamNum = len(ParamVal)
    tlines = []
    KBolt = 1.38e-23
    with open(OrgNetlist, 'r') as file:
        for line in file:
            tlines.append(line.strip())
    if not ParamName:
        print('No parameter is selected!')
        ReturnVal = 0
    else:
        ReturnVal = 1
        for paramCNTR in range(ParamNum):
            SearchVal = f'@{ParamName[paramCNTR]}@'
            for i, line in enumerate(tlines):
                match = re.search(SearchVal,line)
                if match:
                    tlines[i] = line.replace(SearchVal, str(ParamVal[paramCNTR]))

    with open(NewNetlist, 'wt') as fid:
        eqnLinesR = [line for line in tlines if 'ohm' in line]
        eqnLineMaskR = [bool(line) for line in eqnLinesR]
        eqnLinesR2 = [line for line in tlines if 'Rtype' in line]
        eqnLineMaskR2 = [bool(line) for line in eqnLinesR2]
        eqnLinesR3 = [line for line in tlines if 'NON' in line.upper()]
        eqnLineMaskR3 = [bool(line) for line in eqnLinesR3]
        ResMasks = [int(a) - int(b) - int(c) for a, b, c in zip(eqnLineMaskR, eqnLineMaskR2, eqnLineMaskR3)]

        ResistorPlace = [i for i, value in enumerate(ResMasks) if value > 0]
        jj = 0
        for ii, line in enumerate(tlines):
            fid.write(line + '\n')
            ifcond = ii in ResistorPlace

            # Add noise on any resistor that program finds in the netlist
            if AddNoise and ifcond:
                SplitedLineRes = tlines[ResistorPlace[jj]].split()
                ResCells = ''.join(SplitedLineRes)
                rvalstr = ResCells[3].split('ohm')
                rval = float(rvalstr[0])
                noise = round(1000 * (pow((4 * KBolt * temperature) / rval, 0.5) * 1e12)) / 1000
                NoiseLine = f'I{ResCells[0]} {ResCells[1]} {ResCells[2]} NOISE({noise}p 0.0 1.0p)'
                fid.write(NoiseLine + '\n')
                jj += 1
        
    return ReturnVal