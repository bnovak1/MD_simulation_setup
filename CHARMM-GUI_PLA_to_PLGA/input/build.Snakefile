import os

configfile: 'config.json'

rule PLA_chains_to_PDB:
    input:
        pdb = os.path.join(config['CHARM-GUI_DIRECTORY'], 'step2.6_solvator.pdb'),
        script = os.path.join('..', 'scripts', 'PLA_chains_to_PDB.tcl')
    output:
        pdbs = expand(os.path.join('..', 'output', 'PLA_{n}.pdb'), n=range(config['NCHAINS']))
    params:
        outprefix = os.path.join('..', 'output', 'PLA_')
    shell:
        '''
        echo "source {input.script}" > temp.tcl
        echo "split_LACT_chains {input.pdb} {params.outprefix}" >> temp.tcl
        echo "exit" >> temp.tcl
        vmd -dispdev none -e temp.tcl
        '''

rule PLA_to_PLGA:
    input:
        pdb = os.path.join('..', 'output', 'PLA_{n}.pdb'),
        script = os.path.join('../scripts', 'PLA_to_PLGA.py')
    output:
        pdb = os.path.join('..', 'output', 'PLGA_{n}_bonded_minimized.pdb')
    shell:
        '''
        python {input.script} {input.pdb}
        '''

rule PLA_to_PLGAs:
    input:
        expand(rules.PLA_to_PLGA.output.pdb, n=range(config['NCHAINS']))
