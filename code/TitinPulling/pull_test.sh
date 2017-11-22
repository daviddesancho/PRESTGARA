#!/bin/bash 

set -e

source /usr/local/gromacs/4.6.7/bin/GMXRC.bash

#grompp -c titin.14879.pdb.sb/titin.14879.pdb.gro -p titin.14879.pdb.sb/titin.14879.pdb.top -f allatom.mdp -o allatom.tpr -maxwarn 1

#mdp="smog/allatom_pull_umbrella.mdp"
mdp="smog/all_atom_pull_rate_r0.2_r0.mdp"
gro="smog/titin6_longbox.gro"
top="smog/titin6.top"
ndx="smog/titin6.ndx"
grompp -c $gro -p $top -f $mdp -o pull -maxwarn 1 -n $ndx

mdrun -v -s pull.tpr -deffnm pull -nt 1 -pf pullf -px pullx
