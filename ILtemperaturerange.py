from IsingLattice import *
from matplotlib import pylab as pl
import numpy as np

n_rows = 8
n_cols = 8
il = IsingLattice(n_rows, n_cols)
il.lattice = np.ones((n_rows, n_cols))
spins = n_rows*n_cols
runtime = 100000
times = range(runtime)
temps = np.arange(1.0, 3.0, 0.5)
energies = []
magnetisations = []
energysq = []
magnetisationsq = []
for t in temps:
    for i in times:
        #if i % 100 == 0:
            #print(t, i)
        energy, magnetisation = il.montecarlostep(t)
    aveE, aveE2, aveM, aveM2, n_cycles = il.statistics()
    energies.append(aveE)
    energysq.append(aveE2)
    magnetisations.append(aveM)
    magnetisationsq.append(aveM2)
    #reset the IL object for the next cycle
    il.E = 0.0
    il.E2 = 0.0
    il.M = 0.0
    il.M2 = 0.0
    il.n_cycles = 0
fig = pl.figure()

e_err = (np.array(energysq) - np.array(energies)**2)**0.5
m_err = (np.array(magnetisationsq) - np.array(magnetisations)**2)**0.5

enerax = fig.add_subplot(2,1,1)
enerax.set_ylabel("Energy per spin")
enerax.set_xlabel("Temperature")
enerax.set_ylim([-2.1, 2.1])
magax = fig.add_subplot(2,1,2)
magax.set_ylabel("Magnetisation per spin")
magax.set_xlabel("Temperature")
magax.set_ylim([-1.1, 1.1])
enerax.plot(temps, np.array(energies)/spins)
enerax.errorbar(temps, np.array(energies)/spins,yerr=e_err/spins)

magax.plot(temps, np.array(magnetisations)/spins)
magax.errorbar(temps, np.array(magnetisations)/spins,yerr=m_err/spins)
pl.show()
pl.savefig('trial1.svg',bbox_inches='tight')
final_data = np.column_stack((temps, energies, energysq, magnetisations, magnetisationsq))
np.savetxt("8x8.dat", final_data)