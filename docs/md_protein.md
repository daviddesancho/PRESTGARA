# Molecular dynamics simulations of protein stretching 
In the second part of our tutorial we will look at another 
application of molecular simulations to nanobiotechnology.
In particular we will focus on trying to reproduce 
signatures of single molecule experiments on proteins
with the atomic force microscope (AFM) from a simple toy
model. The protein we will look at, titin, is in fact of great
interest in the study of protein mechanics. You can learn 
more about this protein exploring this 
[link](http://pdb101.rcsb.org/motm/185). For our calculations
we will use an open source package for running simulations called
 [Gromacs](www.gromacs.org).

Instead of running a proper atomistic simulation including physics-based
interactions considering all the atoms of both protein and solvent, we
will use a coarse-grained model. In particular, we will choose the 
widely used [SMOG force field](http://smog-server.org/), which reduces
the representation of the interactions to a design principle (that the
protein will fold to its native state) and conveniently ignores the 
surrounding water. Interestingly, the model retains important 
details of the system. 

### Downloading the protein
First we will look at our system of interest, consisting of six 
immunoglobulin-like domains from the titin molecule from rabbit.
This structure was downloaded from the Protein Data Bank (PDB), and 
you can access a lot of information by inspecting it (each 
experimental structure has a unique id in the PDB, in this case
[3B43](https://www.rcsb.org/pdb/explore.do?structureId=3B43)).
In the webpage for this protein entity, go to the download files
tab and click on ```PDB format```.
Looking at the file is less revealing than visualizing the structure.
This is something we can do running the VMD program. In your terminal
type the following command

	$> vmd 3b43.pdb

This should open the file in a new VMD session, which will allow you
to look at the protein in multiple ways and to generate nice images.

### The simulation model
Using the file for the titin domains and the SMOG server we have generated
files we will need to run our simulation. They are stored in the Git 
repository for this class. The first file we will look at is the ```gro``` 
file, which is very similar to the PDB file. Run the following command in
your terminal 

	$> wget https://raw.githubusercontent.com/daviddesancho/PRESTGARA/master/code/TitinPulling/smog/titin6_longbox.gro
	$> nano titin_longbox.gro

As you can see, the file contains cartesian coordinates for lots of different
atoms. If you move to the end of the directory you will find three numbers.
They define the simulation box, which is very important for running the 
simulations.

The second file we will download is the so-called "topology" file, which
contains all the details of your molecular interactions. You can download
it in the same way. In your terminal, type

	$> wget https://raw.githubusercontent.com/daviddesancho/PRESTGARA/master/code/TitinPulling/smog/titin6.top
	$> nano titin6.top

There are lots of interesting things to see here. The file is divided in 
different sections, where we define the different types of atoms and the
different types of interactions. As you will notice, hydrogen atoms do not
show up because they are not considered in the model. An interesting section
is the ```[ bonds ]``` section. It looks like this:

	 [ bonds ]
	 ;ai     aj      func    r0(nm)  Kb
	        1        2     1 1.452939779e-01 1.000000000e+04
	        2        3     1 1.522609930e-01 1.000000000e+04
	        2        5     1 1.530609356e-01 1.000000000e+04
	 ...

For bonded pairs of atoms in our sequence, it defines the bond distance and 
the interaction strength, which as you will remember is determined by a 
harmonic spring constant. The same is true for the ```[ angles ]``` section,
 but here each angle needs three atoms. Next we  find the torsion angles, 
defined as a periodic function for groups of 4  atoms. 

	[ dihedrals ]
	;ai  aj  ak  al  func  phi0(deg) kd mult
	        1        2        3        4  1 1.137472335e+02 2.287907073e-01 1
	        1        2        3        4  1 3.412417005e+02 1.143953537e-01 3
	        1        2        3        6  1 2.919004930e+02 2.287907073e-01 1
	        1        2        3        6  1 8.757014791e+02 1.143953537e-01 3

The type of function used here is a Fourier series. We will just finalize
mentioning that the non-bonded interactions here are defined in the ```[ pairs ]```
section. These are defined providing the numerators for the 6 and 12 terms in a Lennard-Jones
potential.
All of these interaction terms are defined in great lenghts in the [Gromacs
manual](http://manual.gromacs.org/documentation/). 

Another file we will need to download is the index (or ```ndx``` file). Since
we are pulling from the protein ends in our simulation, we need to tell the program
the indexes of the atoms we will pull from.

### Parameters for the simulation
Of course, so far we just have a static protein structure and all the required
 parameters for the interactions. To run dynamics, we must tell the program many 
details on how the simulation must be run. These parameters are specified in the 
```mdp``` file.

	$> wget https://raw.githubusercontent.com/daviddesancho/PRESTGARA/master/code/TitinPulling/smog/titin6.ndx

### Setting up your run
Usually, preparing a simulation in Gromacs requires [multiple 
steps](http://www.gromacs.org/Documentation/How-tos/Steps_to_Perform_a_Simulation),
 including the minimization of the protein structure, the equilibration of the 
water box and the convergence to a set of pre-defined set of conditions (pressure 
and temperature) at which we want to study our system. In our simple coarse grained 
model things are much simplified. 

The first thing we will do is to source the ```GMXRC.bash``` file, that allows Gromacs
commands to be accessible in our terminal.


	$> source $GROMACS_INSTALL_LOCATION/bin/GMXRC.bash 

Then we will prepare our Gromacs "run input file" using the following command

	$> gro="titin6_longbox.gro"
	$> top="titin6.top"
	$> ndx="titin6.ndx"
	$> mdp="pull.mdp"
	$> tpr="pull.tpr"
	$> gmx grompp -c $gro -f $mdp -p $top -o $tpr -n $ndx -maxwarn 1

This should produce a new ```pull.tpr``` file in your directory. Using this
 ```tpr``` file as input, we can now run our MD simulation.

	$> gmx mdrun -v -s pull.tpr -deffnm pull -nt 1 -pf pullf -px pullx

We will first look at the results using VMD. Again, open a new session from the terminal

	$> vmd smog/titin6_longbox.gro

And now load your trajectory onto the initial structure. For this you will have to type

	vmd $> mol addfile pull.xtc waitfor all

in your VMD session prompt. Chances are that what you see will make you feel
dizzy, as the protein seems to be going across the simulation box. In fact, that
is precisely what you are seen. In order to produce a trajectory without this
effect we can use a Gromacs tool for making transformations on trajectories

	$> gmx trajconv -s $tpr -f $out -pbc nojump

You can now run the resulting ```trajout.xtc``` file. What do you see in the simulation?
