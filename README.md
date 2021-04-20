# MD_simulation_setup

Scripts to help with setting up molecular dynamics simulations.

## gzmat_to_polymod.py ([docs](https://github.com/bnovak1/MD_simulation_setup/wiki/gzmat_to_polymod.py))

Convert a Gaussian gzmat file (```infile```) for a monomer with ```nbackbone``` backbone atoms to a Z-matrix file for use with NanoHUB Polymer Modeler.

## CHARMM-GUI_PLA_to_PLGA ([docs](https://github.com/bnovak1/MD_simulation_setup/wiki/CHARMM-GUI_PLA_to_PLGA))

Convert polylactic acid built with <a href="https://www.charmm-gui.org/?doc=input/polymer">CHARMM-GUI Polymer Builder</a> to poly(lactic-*co*-gylcolic acid) 50:50. Could easily be extended to arbitrary ratios of monomer types. Also see this [post](https://wp.me/p9QWVm-2F).

## LigninBuilder_GROMACS ([docs](https://github.com/bnovak1/MD_simulation_setup/wiki/LigninBuilder_GROMACS))

Build chosen library(ies) that come with LigninBuilder, sort structures by number of monomers, create GROMACS .top files for structures with desired sizes, energy minimize structures with GROMACS. Also see this [post](https://wp.me/p9QWVm-3x).
