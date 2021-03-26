# MD_simulation_setup

Scripts to help with setting up molecular dynamics simulations.

## gzmat_to_polymod.py 

Convert a Gaussian gzmat file (```infile```) for a monomer with ```nbackbone``` backbone atoms to a Z-matrix file for use with NanoHUB Polymer Modeler.

Usage: ```python gzmat_to_polymod.py infile nbackbone```

```nbackbone``` is the number of backbone atoms in the monomer plus 2 hydrogens on each end. The output file has the same prefix as the input file with the extension .polymodzmat.

See examples here.
