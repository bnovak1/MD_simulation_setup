'''
Build a set of lignin structures with specified sizes from specified Lignin Builder libraries.
'''

import glob
import os

configfile: 'config.json'

# Create structures. Write Tcl file and execute with VMD
rule build_library:
    input:
        lib = os.path.join(config['BUILDER_DIRECTORY'], 'libraries', '{species}_Library.txt')
    output:
        built = touch(os.path.join('..', 'output', '{species}_built'))
    params:
        outdir = os.path.join('..', 'output', '{species}_Library'),
        temp = 'temp_{species}.tcl'
    shell:
        '''
        echo "package require ligninbuilder" > {params.temp}
        echo "::ligninbuilder::buildfromlibrary {input.lib} {params.outdir}" >> {params.temp}
        echo "exit" >> {params.temp}
        vmd -e {params.temp}
        rm {params.temp}
        '''

rule build_libraries:
    input:
        expand(rules.build_library.output, species=config['SPECIES_LIST'])

# Create directories for each lignin size (number of monomers) containing symbolic links to the
# pdb & psf files
rule sort_by_size:
    input:
        built = rules.build_library.output.built,
        script = os.path.join('..', 'scripts', 'sort_by_size.py')
    output:
        sorted = touch(os.path.join('..', 'output', '{species}_sorted'))
    params:
        indir = rules.build_library.params.outdir
    shell:
        'python {input.script} {params.indir}'

rule sort_by_sizes:
    input:
        expand(rules.sort_by_size.output, species=config['SPECIES_LIST'])

rule size_lists:
    input:
        sorted = rules.sort_by_size.output.sorted,
        script = os.path.join('..', 'scripts', 'size_lists.py'),
    output:
        json = os.path.join('..', 'output', '{species}_Library', 'size_lists.json')
    params:
        directory = os.path.join('..', 'output', '{species}_Library')
    shell:
        'python {input.script} {wildcards.species} {params.directory}'

rule size_listss:
    input:
        expand(rules.size_lists.output, species=config['SPECIES_LIST'])
