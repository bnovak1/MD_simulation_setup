'''
Convert a Gaussian gzmat file (infile) for a monomer with nbackbone backbnone atoms to a Z-matrix
file for use with NanoHUB Polymer Modeler.
'''
import sys

# Command line inputs
infile = sys.argv[1]
nbackbone = sys.argv[2]

# Read input file
with open(infile, 'r') as f:
    data_in = f.readlines()

# Determine where Variables section starts
for iline,line in enumerate(data_in):
    if line == 'Variables:\n':
        line_start = iline + 1
        break

# Split data from file into part with atom data and part with variable data
atom_data = ''.join(data_in[6:line_start-1])
variable_data = data_in[line_start:-1]

# Put variables into a dictionary
variables = {}
for line in variable_data:
    v = line.split('\n')[0].split('= ')
    variables[v[0]] = v[1]

# Replace variables in atom data with their values
for key in variables:
    atom_data = atom_data.replace(key, variables[key])
atom_data = nbackbone + '\n' + atom_data

# Prepend number of backbone atoms to atom data and write to output file
infile_prefix = infile.split('.gzmat')[0]
outfile = infile_prefix + '.polymodzmat'
with open(outfile, 'w') as f:
    f.write(atom_data)
