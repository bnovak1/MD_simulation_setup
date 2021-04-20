# MD_simulation_setup

Scripts to help with setting up molecular dynamics simulations.

## gzmat_to_polymod.py 

Convert a Gaussian gzmat file (```infile```) for a monomer with ```nbackbone``` backbone atoms to a Z-matrix file for use with NanoHUB Polymer Modeler.

Usage: ```python gzmat_to_polymod.py infile nbackbone```

```nbackbone``` is the number of backbone atoms in the monomer plus 2 hydrogens on each end. The output file has the same prefix as the input file with the extension .polymodzmat.

See examples for building PLA and PLGA polymers which use this script [here](https://molecularsimulation148022533.wordpress.com/2021/03/26/building-polymers-not-included-in-the-nanohub-polymer-modeler-tool/).

## CHARMM-GUI_PLA_to_PLGA

Convert polylactic acid built with <a href="https://www.charmm-gui.org/?doc=input/polymer">CHARMM-GUI Polymer Builder</a> to poly(lactic-*co*-gylcolic acid) 50:50. Could easily be extended to arbitrary ratios of monomer types.

### scripts/PLA_chains_to_PDB.tcl

Tcl script for splitting multiple PLA chains from a PDB file into separate PDB files for each chain. Requires [Visual Molecular Dynamics (VMD)](https://www.ks.uiuc.edu/Research/vmd/).

### scripts/PLA_to_PLGA.py

Python script for converting PLA to PLGA 50:50 by replacing each methyl side chain of PLA with hydrogen with a 50% probability. Requires [numpy](https://numpy.org/), [Open Babel](http://openbabel.org/wiki/Main_Page), and [Visual Molecular Dynamics (VMD)](https://www.ks.uiuc.edu/Research/vmd/).

### input/build.Snakefile

Snakefile for applying the 2 scripts above. Independent usage of the scripts can also be determined from here. Requires [snakemake](https://snakemake.readthedocs.io/).

## LigninBuilder_GROMACS

Build chosen library(ies) that come with LigninBuilder, sort structures by number of monomers, create GROMACS .top files for structures with desired sizes, energy minimize structures with GROMACS. Also see this [post](https://wp.me/p9QWVm-3x).

## scripts/sort_by_size.py

Sort structures by monomer number by creating subdirectiories in the input directory for each monomer number with symbolic links the original files in the input directory.

## scripts/size_lists.py

Create dictionary with lists of file names for each lignin size (number of monomers).  Write to a new file in the directory input called size_lists.json, and add to config.json.

## input/build.Snakefile

Build a set of lignin structures with specified sizes from specified Lignin Builder libraries, and sort structures by number of lignin monomers. Must run the size_listss rule before using input/minimize.Snakefile. Requires [Visual Molecular Dynamics (VMD)](https://www.ks.uiuc.edu/Research/vmd/), [LigninBuilder](https://github.com/jvermaas/LigninBuilder/tree/master/LigninBuilderPlugin), and [snakemake](https://snakemake.readthedocs.io/). Uses scripts/sort_by_size.py and scripts/size_lists.py.

## input/minimize.Snakefile

Minimize structures using GROMACS. Currently the size_listss rule in build.Snakefile must be
run to update config.json before using this Snakefile. Requires [Visual Molecular Dynamics (VMD)](https://www.ks.uiuc.edu/Research/vmd/), [TopoTools 1.6](https://github.com/akohlmey/topotools), and [snakemake](https://snakemake.readthedocs.io/). TopoTools 1.7 does not work. TopoTools 1.8 has not been tested.

