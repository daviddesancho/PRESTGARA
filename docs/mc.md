# Monte Carlo simulation of an Ising model

The [Ising model](https://en.wikipedia.org/wiki/Ising_model) is very useful as a model for
 magnetization that will allow for exploring the Monte Carlo method. In the Ising model
we consider a two-dimensional lattice of particles, each of which has only two possible 
spins, "up" and "down". In our particular example we will consider that interactions 
are limited to nearest neighbours. A parallel pair results in a lower energy than an
antiparallel pair. Ideally, we would also consider the effect of an external field on the
results, but today we will focus on the effects of the temperature only.

For this exercise we use the code developed by Frans Pretorius and William East (Princeton 
University). The first thing we need to do is download two pieces of Python code: 
[```ising_MHMC.py```](https://github.com/daviddesancho/PRESTGARA/blob/master/code/Ising_2d/ising_MHMC.py) 
and [```ising.py```](https://github.com/daviddesancho/PRESTGARA/blob/master/code/Ising_2d/ising.py).

### Moving around

In order to start getting some intuition on we will start working on a 
[jupyter-notebook](http://jupyter.org/). Assuming that the ```jupyter``` package is 
properly installed in your anaconda Python distribution of your machine, you just have
 to open your terminal and move to the directory where your files are located. The 
files you downloaded are probably in the ```Downloads``` folder of your machine, so in 
your terminal type the following:

	$> mkdir Ising
	$> mv ~/Downloads/ising.py Ising  
	$> jupyter-notebook ising.py

### Generating an Ising model
In a text editor we will open the ```ising.py``` file itself. The Python code we are using
contains a class (called ```Ising_lattice```) that allows generating 2D Ising models of size NxN.
 Although you do not need to understand everything in this file it is useful to go through
 some bits of code.

	def __init__(self,N,J=1.0,H=0.0):
	   self._N=N
	   self._J=J
	   self._H=H
	   #self.aligned_spins()
	   self.random_spins()
	   self._compute_E_M()

This is the method that initializes instances of the ```Ising_lattice``` class, which 
needs to know the size of the lattice (```N```),  the strength of the interactions 
(```J```) and the external magnetization (```H```). Also, we are initializing 
the lattice by randomizing the spin directions (using the method ```random_spins()```) and
 computing the energies and magnetization (```_comput_E_M()```).

Let's then initialize an instance of this class in our jupyter-notebook. First, in a cell
we will first import a number of packages writing and executing the following lines 

	import numpy as np
	import ising as I
	import matplotlib.pyplot as plt
	%matplotlib inline

To run this cell we need to either click ```Shift+Enter``` or use the Play button. Then
we can generate an instance of the class of *N=*5.

	a = I.Ising_lattice(5)

This generates a 5x5 lattice with randomized spins. To get a simple visualization of this
you can use another method written in the class.

	a.diagram()

This should result in output like the following 

	Lattice properties: 5^2 cells, E=-2.000000, M=-1, <E>=-0.080000, <M>=-0.040000
	
	[['@' ' ' ' ' ' ' '@']
	 [' ' ' ' ' ' ' ' '@']
	 ['@' '@' '@' ' ' '@']
	 ['@' ' ' ' ' ' ' '@']
	 ['@' '@' ' ' '@' ' ']]

If you want to flip a specific spin then you can use another method for that:

	a.spin_flip(0,1)
	a.diagram()

And you will get an output corresponding to the flipped spin

	[['@' '@' ' ' ' ' '@']
	 [' ' ' ' ' ' ' ' '@']
	 ['@' '@' '@' ' ' '@']
	 ['@' ' ' ' ' ' ' '@']
	 ['@' '@' ' ' '@' ' ']]

So far we know how to generate an Ising lattice, flip its spins and recover its energy 
and magnetization. But this specific configuration would in principle be as representative
of the magnet as any other configuration. In order to get a more faithful representation of 
the system that allows calculating average properties we need to sample from the ensemble
of possible configurations. This is done using the Monte Carlo method.

### The MC algorithm
We will run our MC algorithm in the Jupyter notebook. First we will define the 
size of the lattice and generate the initial configuration, which in this case 
will be of size 8x8.  

	N = 5
	a = I.Ising_lattice(N)

Next we will define the MC loop, which in this case will do 1000 iterations trying
to sample from the ensemble of possibilities 

	nflips = 1000
	n = 0
	while n < nflips:
	   i = np.random.random()*N
	   j = np.random.random()*N
	   a.cond_spin_flip(i,j,T);
	   energy.append(a._E)
	   magnet.append(a._M)
	   n+=1

Here we are doing random flips in our lattice in positions ```i``` and
```j``` and accepting them depending on the Metropolis criterion. The
flipping, the calculation of the energy and the acceptance or rejection
are encoded in the ```Ising_lattice``` class.
