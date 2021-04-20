'''
Minimize structures using GROMACS. Currently the size_listss rule in build.Snakefile must be
run to update config.json before using this Snakefile.
'''

import os

configfile: 'config.json'

# Use TopoTools VMD plugin to create GROMACS .top files for specified sizes.
rule get_CHARMMM_carbo:
    '''
    CHARMM carbohydrate parameters are needed.
    '''
    output:
        carb_params = os.path.join('toppar_c36_jul20', 'par_all36_carb.prm')
    shell:
        '''
        wget http://mackerell.umaryland.edu/download.php?filename=CHARMM_ff_params_files/toppar_c36_jul20.tgz \
             -O toppar_c36_jul20.tgz
        tar -zxf toppar_c36_jul20.tgz
        rm toppar_c36_jul20.tgz
        '''

rule create_top:
    '''
    Does not work with TopoTools 1.7. Replaced topotools1.7 folder with topotools1.6 folder from
    https://github.com/akohlmey/topotools/releases for VMD 1.9.3. Did not test TopoTools 1.8.
    '''
    input:
        pdb = os.path.join('..', 'output', '{species}_Library', '{size}', 'L{n}.pdb'),
        psf = os.path.join('..', 'output', '{species}_Library', '{size}', 'L{n}.psf'),
        prms = [str(rules.get_CHARMMM_carbo.output.carb_params),
                os.path.join(config['BUILDER_DIRECTORY'], 'LigninBuilderPlugin', 'par_lignin.prm'),
                os.path.join(config['BUILDER_DIRECTORY'], 'LigninBuilderPlugin',
                             'extraterms-par_lignin.prm')]
    output:
        top = os.path.join('..', 'output', '{species}_Library', '{size}', 'L{n}.top')
    params:
        temp = 'temp_{species}_{size}_{n}.tcl'
    shell:
        '''
        echo "package require topotools" > {params.temp}
        echo "set basemol [mol new {input.psf}]" >> {params.temp}
        echo "mol addfile {input.pdb} \$basemol" >> {params.temp}
        echo "topo writegmxtop {output.top} [list {input.prms}]" >> {params.temp}
        echo "exit" >> {params.temp}
        vmd -dispdev none -e {params.temp}
        rm {params.temp}
        '''

rule create_tops:
    input:
        [re.sub('{[a-z0-9]*}', '{}', str(rules.create_top.output.top)).format(species, size, n) \
         for species in config['SPECIES_LIST'] for size in config['LIGNIN_SIZES'] \
         for n in config['SIZE_LISTS'][species][size]]

# Minimize using GROMACS
rule grompp:
    input:
        pdb = rules.create_top.input.pdb,
        top = rules.create_top.output.top,
        mdp = 'min.mdp'
    output:
        tpr = os.path.join('..', 'output', '{species}_Library',
                           'minimization', '{size}', 'L{n}.tpr'),
    shell:
        'gmx grompp -f {input.mdp} -c {input.pdb} -p {input.top} -o {output.tpr}'

rule grompps:
    input:
        [re.sub('{[a-z0-9]*}', '{}', str(rules.grompp.output.tpr)).format(species, size, n) \
         for species in config['SPECIES_LIST'] for size in config['LIGNIN_SIZES'] \
         for n in config['SIZE_LISTS'][species][size]]

rule minimization:
    input:
        tpr = rules.grompp.output.tpr
    output:
        gro = os.path.join('..', 'output', '{species}_Library',
                           'minimization', '{size}', 'L{n}.gro'),
    params:
        prefix = os.path.join('..', 'output', '{species}_Library', 'minimization', '{size}', 'L{n}')
    shell:
        '''
        export OMP_NUM_THREADS=1
        mdrun -s {input.tpr} -deffnm {params.prefix} -ntmpi 1 -ntomp 1
        '''

rule minimizations:
    input:
        [re.sub('{[a-z0-9]*}', '{}', str(rules.minimization.output.gro)).format(species, size, n) \
         for species in config['SPECIES_LIST'] for size in config['LIGNIN_SIZES'] \
         for n in config['SIZE_LISTS'][species][size]]
