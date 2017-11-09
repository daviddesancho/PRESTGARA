#!/usr/bin/env python

import numpy as np
import ising as I

#   Code by Frans Pretorius and William East (Princeton)

#
# Search for a ground state using the Metropolis-Hastings algorithm
#

import sys,os,shutil
    
# Call the main routine with all the command-line arguments
# This is the Python idiom for a free-standing script.

if __name__ == '__main__':
	try: N = int(sys.argv[1])
	except IndexError: N = 8
	    
	try: nflips  = int(sys.argv[2])
	except IndexError: 
		nflips = 2000000
	    
	try: T     = float(sys.argv[3])
	except IndexError: T=0.0
	
	try: H     = float(sys.argv[4])
	except IndexError: H = 0.0
	
	try: J     = float(sys.argv[5])
	except IndexError: J = 1.0

	# remove everything in pngs dir
	if os.path.isdir('pngs'):
		shutil.rmtree('pngs')
	os.mkdir('pngs')	
	
	# ... your code here!
	a = I.Ising_lattice(N)

	command = "convert -delay 1 -size 100x100"
	n = 0
	k = 0
	fout = open("output_T%g_H%g.dat"%(T,H),"w")
	while n < nflips:
		i = np.random.random()*N
		j = np.random.random()*N
		a.cond_spin_flip(i,j,T); 		

		if n % 1000 == 0 and n > 200000:
			fout.write ("%8i %8i %8i %8i\n"%(n,a._E,a._M,abs(a._M)))
		if n % 10000 == 0:
			k +=1
			a.plot(k)
			command += " pngs/ising%g.png"%k
		n+=1
	
	command +=" animation_T%g_H%g.gif"%(T,H)
	os.system(command)
	fout.close()
