# Monte Carlo simulation of an Ising model

The [Ising model](https://en.wikipedia.org/wiki/Ising_model) is very useful 
for the study of magnetization and also for exploring some basic features of
 the Monte Carlo method. 

In the Ising model we consider a two-dimensional 
lattice of spins, each of which has only two possible configurations, "up" and 
"down". In our particular example we will consider that interactions are 
limited to nearest neighbours. In the case of a ferromagnet, a parallel pair 
results in a lower energy than an antiparallel pair, while for an antiferromagnet
things work the other way around. Ideally, we would also consider the effect 
of an external field on the results, but today we will focus on the effects 
of temperature only in a ferromagnetic 2D material.

For this exercise we use the code developed by Frans Pretorius and William 
East (Princeton 
University). The first thing we need to do is download two pieces of Python 
code: 
[```ising_MHMC.py```](https://github.com/daviddesancho/PRESTGARA/blob/master/code/Ising_2d/ising_MHMC.py) 
and [```ising.py```](https://github.com/daviddesancho/PRESTGARA/blob/master/code/Ising_2d/ising.py). For downloading the files, you will need to click on the "Raw"
tab and then proceed with the download.

### Moving around

We will first start developing some intuition on what the code can do. 
The files you downloaded are probably in your ```Downloads``` folder, so 
in your terminal please type the following:

	$> mkdir Ising
	$> cd Ising
	$> mv ../Downloads/ising* .

In a text editor we will open the ```ising.py``` file. You can use your favourite
text editor (a good one you will find in your macOS or Linux is called "nano").

	$> nano ising.py

Now we can read the Python code we will be using, although you do not need
to worry about the syntax. At first side you will see that the 
```ising.py``` file contains something called a "class", which we 
define in the statement 

	class Ising_lattice(object):

This class allows generating 2D Ising models of size NxN. Although you do not 
need to understand everything in will be useful to go through the following 
snippet:

	def __init__(self,N,J=1.0,H=0.0):
	   self._N=N
	   self._J=J
	   self._H=H
	   #self.aligned_spins()
	   self.random_spins()
	   self._compute_E_M()

What you read above is called a "method", a part of a class which in this case
initializes an instance of the ```Ising_lattice``` class. The information it 
needs to get from the user is the size of the lattice (```N```),  the strength
 of the interactions (```J```) and the external magnetization (```H```). Also,
 we are initializing the lattice by randomizing the spin directions (using the
 method ```random_spins()```) and computing the energies and magnetization 
(```_compute_E_M()```).


### Generating an Ising model
Let's then initialize an instance of this class in our jupyter-notebook. 
To work with this class we will work on a [jupyter-notebook](http://jupyter.org/).
Assuming that the ```jupyter``` package is properly installed in your anaconda 
Python installation, you just have to open your terminal and move to the directory
 where your files are located. There, type the following

	$> jupyter-notebook

This should open a page of your web browser and offer you the possibility 
to create a new notebook using the ```New``` tab.  In your newly created 
notebook we will first import a number of packages, for which we will need
to writing and execute the following lines

	import os
	import numpy as np
	import matplotlib.pyplot as plt
	%matplotlib inline
	import ising as I

For these actions to take place we need to "run" the cell. To do it, we just 
need to either click ```Shift+Enter``` or use the Play button on the top bar. 
Next, we can generate an instance of the class with size *N=*5.

	a = I.Ising_lattice(5)

This generates a 5x5 lattice with randomized spins. To get a simple 
visualization of this you can use another method included in the class.

	a.diagram()

This should result in output like the following 

	Lattice properties: 5^2 cells, E=-2.000000, M=-1, <E>=-0.0200000, <M>=-0.040000
	
	[['@' ' ' ' ' ' ' '@']
	 [' ' ' ' ' ' ' ' '@']
	 ['@' '@' '@' ' ' '@']
	 ['@' ' ' ' ' ' ' '@']
	 ['@' '@' ' ' '@' ' ']]

In this way we get a rough representation of your magnet, with different symbols
corresponding to up and down spins. We also get the value for the energy, which 
will be useful later. If you want to flip a specific spin then you can use another 
method for that:

	a.spin_flip(0,1)
	a.diagram()

And you will get an output corresponding to the flipped spin

	[['@' '@' ' ' ' ' '@']
	 [' ' ' ' ' ' ' ' '@']
	 ['@' '@' '@' ' ' '@']
	 ['@' ' ' ' ' ' ' '@']
	 ['@' '@' ' ' '@' ' ']]

Depending of your specific case, the energy in your lattice may have changed
so that you have a more or less stable configuration.


### The MC algorithm
So far we know how to generate an Ising lattice, flip its spins and recover
 its energy and magnetization. But the configurations we are generating
would be, in principle, as representative of the magnet as any other 
configuration (out of 2<sup>25 </sup>possible options!). Clearly, generating
configurations at random does not seem to be a very good way of understanding
average properties of the system, like the magnetization at a given temperature.
In order to get a more faithful representation we need to sample from the ensemble
of possible configurations. This is done using the Monte Carlo method.

We will run our MC algorithm in the Jupyter notebook. First we will define 
the size of the lattice and generate the initial configuration, in
 this case will be of size 20x20.  

	N = 20
	a = I.Ising_lattice(N)

Next we will define the MC loop, which in this case will do 1000 iterations 
trying to sample from the ensemble of possibilities 

	nflips = 1000
	n = 0
	temp = 0
	energy = []
	magnet = []
	while n < nflips:
	   i = int(np.random.random()*N)
	   j = int(np.random.random()*N)
	   a.cond_spin_flip(i,j,temp);
	   energy.append(a._E)
	   magnet.append(a._M)
	   n+=1

In each MC iteration we are attempting a random flip in our lattice. 
The change is done in positions ```i``` and ```j``` and acceptance or 
rejection of the move depends on the Metropolis criterion. We can plot
the results very easily typing and running the following lines

	fig, ax = plt.subplots(2,1, sharex=True)
	ax[0].plot(energy)
	ax[1].plot(magnet)
	ax[1].set_xlabel('MC step')
	ax[0].set_ylabel('Energy')
	ax[1].set_ylabel('Magnetization') 

What are the trends you observe? Is that the behaviour you would expect
from an MC algorithm? 

### The Metropolis acceptance criterion
The flipping, the calculation of the energy and the acceptance or rejection
 are encoded in the ```cond_spin_flip()``` method of the ```Ising_lattice```
 class. The latter part (i.e. the Metropolis rule) deserves some more 
attention. It is encoded in the following line:

	 if (dE < 0.0 or (T>0.0 and (np.random.random()<np.exp(-dE/T)))):

This line is asking whether any of two conditions are being fulfilled: 
whether the change in the energy is favourable, or whether being unfavourable
it is permisible given the available thermal energy. In case any of these is
true, the attempted move will be accepted. Otherwise it will be rejected.

Based on this explanation, do the results you have obtained before make sense?

### Exploring thermal effects in the algorithm
To finalize with our investigation of the Ising model we are going to explore 
what the thermal effects are in our magnet. For that we will run the algorithm
at different final temperatures. Type the following lines in a Jupyter cell

	command = "convert -delay 1 -size 100x100"
	temp = 1
	H = 0
	fout = open("output_T%g_H%g.dat"%(temp,H),"w")
	n = 0
	k = 0
	nflips = 10000
	while n < nflips:
	    i = int(np.random.random()*N)
	    j = int(np.random.random()*N)
	    a.cond_spin_flip(i,j,temp)
	
	    if n % 1000 == 0:
	        fout.write ("%8i %8i %8i %8i\n"%(n,a._E,a._M,abs(a._M)))
	    if n % 1000 == 0:
	        k +=1
	        try: 
	            a.plot(k)
	        except IOError:
	            os.mkdir("pngs")
	        command += " pngs/ising%g.png"%k
	    n+=1
	    
	
	command +=" animation_T%g_H%g.gif"%(temp,H)
	os.system(command)
	fout.close()

You will see that here we have some additional complexity. On one hand 
there are some mysterious ```command``` statements. They are there to allow
for us to create a small animated gif with the time evolution of our Ising 
model at different temperatures. 

After running these lines at different temperatures by varying the final 
temperature (```temp```) do the results make sense? Do they give a hint
of why there is such thing as a [Curie temperature](https://en.wikipedia.org/wiki/Curie_temperature)?
