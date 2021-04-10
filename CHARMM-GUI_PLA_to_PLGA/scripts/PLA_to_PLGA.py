'''
Transform poly-DL-lactic acid PDB file from CHARMM-GUI Polymer Builder to
PDB file of minimized poly-DL-lactic-co-glycolic acid 50:50.
'''

import os
import subprocess
import sys
import numpy as np


def read_pdb(infile):
    '''
    Read pdb file.
    '''

    with open(infile, 'r') as fid:
        data = np.array(fid.readlines())

    return data

def replace_methyls(infile, data):
    '''
    Replace methyl side chains with a hydrogen with a 50% probability.
    '''

    outfile = infile.replace('PLA', 'PLGA')

    # Replace CH3 with H randomly
    ind = np.ones(data.shape[0], dtype=bool)
    iline = 0

    while iline < data.shape[0]:

        data[iline] = data[iline].replace('LACT', 'LAA ')

        line = data[iline]
        if line[:4] == 'ATOM' and line[13:16] == 'C3 ' and line[17:20] == 'LAA':
            if np.random.choice([0, 1]) == 0:
                for i in range(iline-5, iline):
                    data[i] = data[i].replace('LAA ', 'GLA ')
                if data[iline-1][13:16] != 'H22':
                    data[iline] = data[iline].replace('C3 ', 'H22')
                else:
                    data[iline] = data[iline].replace('C3 ', 'H23')
                ind[iline+1:iline+4] = 0
                iline += 3

        iline += 1

    data = data[ind]

    # Write data to new pdb file
    with open(outfile, 'w') as fid:
        for line in data:
            fid.write(line)

    # Run through Open Babel to renumber atoms
    str_in = 'obabel -ipdb ' + outfile + ' -opdb -O ' + outfile
    subprocess.call(str_in.split())

    # Read in data for pdb file
    with open(outfile, 'r') as fid:
        data = fid.readlines()

    # Determine bonds to create with TopoTools
    bonds_list = []
    for iline, line in enumerate(data):
        if line[:4] == 'ATOM' and line[17:20] == 'GLA':
            if line[13:16] == 'C2 ':
                ind1 = int(data[iline][4:11]) - 1
                ind2 = int(data[iline+2][4:11]) - 1
                bonds_list.append([ind1, ind2])
            elif line[13:16] == 'H23':
                ind1 = int(data[iline-3][4:11]) - 1
                ind2 = int(data[iline][4:11]) - 1
                bonds_list.append([ind1, ind2])

    return (data, bonds_list, outfile)

def add_bonds(infile, bonds_list):
    '''
    Add bonds to new hydrogens using TopoTools VMD plugin since they are too long to be
    recognized automatically with VMD or Open Babel. Write to mol2 format which contains
    connectivity information.
    '''

    outfile = infile.replace('.pdb', '_bonded.mol2')

    with open('temp.tcl', 'w') as fid:
        fid.write('package require topotools\n')
        fid.write('set basemol [mol new ' + infile + ']\n')
        for bond in bonds_list:
            fid.write('topo addbond ' + str(bond[0]) + ' ' + str(bond[1]) + '\n')
        fid.write('set sel [atomselect $basemol all]\n')
        fid.write('$sel set type [$sel get element]\n')
        fid.write('$sel writemol2 ' + outfile + '\n')
        fid.write('exit\n')

    subprocess.call('vmd -dispdev none -e temp.tcl'.split())
    os.remove('temp.tcl')

    return outfile

def minimize(infile):
    '''
    Minimize using Open Babel obminimize tool using the GAFF force field.
    '''

    outfile = infile.replace('.mol2', '_minimized.pdb')
    str_in = 'obminimize -ff GAFF ' + infile + ' > ' + outfile
    subprocess.run(str_in, shell=True, check=True)

def main(infile):

    data = read_pdb(infile)
    (data, bonds_list, plga_file) = replace_methyls(infile, data)
    bonded_file = add_bonds(plga_file, bonds_list)
    minimize(bonded_file)

if __name__ == '__main__':

    INFILE = sys.argv[1]
    main(INFILE)
