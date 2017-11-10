#  Introduction to molecular simulation techniques
[**David De Sancho**](https://sites.google.com/view/daviddesanchoresearch/home) (ddesancho@nanogune.eu)  
[Ikerbasque Fellow](http://www.ikerbasque.net/), [CIC nanoGUNE](http://www.nanogune.eu/) (Donostia-San Sebastián)

In this tutorial we will explore some of the concepts that we have covered 
about molecular simulation methods. The practical is intended to serve
as an example of how Monte Carlo (MD) and Molecular Dynamics (MD) simulation 
work practically and how they can provide scientific insight at a fundamental
level in the context of the nanosciences.

### Syllabus

1. MC simulation of magnetization in an Ising model
2. MD simulations of a biomolecule stretching

### Setting yourself up
Before the action starts we need to install some software in our computer, 
which we will need for running the calculations. Please follow the instructions
below.
 
1. **The terminal** : 
	+ *Mac:* Although Macs bring a native Terminal app, I recommend using 
iTerm2, which I find more comfortable to use. Follow [this link](https://www.iterm2.com/),
 download and proceed as indicated in the installation instructions.
	+ *Windows:* Here my advice would be to install [git](https://git-for-windows.github.io/),
 which comes with the phenomenal Git BASH terminal. Download and find the executable
file.

2. **Anaconda** : 
	+ For our first practical we will need a working installation of
Python 2.7. Although macOS and Linux should bring it natively, there are distributions
like Anaconda that bring most of the packages you should need. Go to the Anaconda 
[downloads page](https://www.anaconda.com/download/) and install the Python 2.7 version
 following instructions.

3. **Gromacs** :
	+ *Linux:* Installation instructions can be found in the 
[Gromacs documentation website](http://manual.gromacs.org/documentation/5.1.4/install-guide/index.html).
	+ *Mac*: We first need to go to the Gromacs [downloads page](http://www.gromacs.org/Downloads) 
and download the source code for version 5.1.4. You can find some instructions to install the software 
[here](http://daviddesancho.github.io/ResDocs/Gromacs/installation/). We will not need mpi support 
for our practical so you can stick to the simple installation.
	+ *Windows:* I have never tried this but I read that it is possible to 
install Gromacs on Windows. You can find instructions 
[here](http://www.gromacs.org/Documentation/Installation_Instructions_5.0#Building_on_Windows). 

4. **VMD** :
	+ We will need is some visualization software for watching
our molecules wiggle and jiggle. You can download the code and follow the installation
instructions from [this](http://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=VMD) website.

5. **ImageMagick***:
	+ Finally, for some visualization of the properties of the Ising model we will need 
the ImageMagik software which you will be able to install following the instructions in this 
[link](https://www.imagemagick.org/script/index.php).