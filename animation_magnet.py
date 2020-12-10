import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from IsingLattice_magnet import *
from matplotlib import animation

N = 8
T = 0.1

il = IsingLattice(N,N)
spins = N*N

e_list = []
mag_abs = []
mag_ang = []
#l_list = []

def animate(runs,temperature):
    for _ in range(runs):
        energy, magnetisation,shape = il.montecarlostep(temperature)
        e_list.append(energy)
        mag_abs.append(magnetisation[0])
        mag_ang.append(magnetisation[1])
        #l_list.append(shape)

cycles = 10000
animate(cycles,T)

mag_ang = np.array(mag_ang)
mag_abs = np.array(mag_abs)/spins
e_list = np.array(e_list)

xval = np.arange(0, 2*np.pi, 0.01)
yval = np.ones_like(xval)

colormap = plt.get_cmap('hsv')
norm = mpl.colors.Normalize(0.0, 2*np.pi)

fig = plt.figure()
ax = plt.subplot(1, 1, 1, polar=True)

ax.scatter(xval, yval, c=xval, s=300, cmap=colormap, norm=norm, linewidths=0)
ax.set_yticks([0.5,1])

line1, = ax.plot(mag_ang[0],mag_abs[0],c='black',linestyle='',marker='x',markersize=10)
line2, = ax.plot(mag_ang[0],mag_abs[0],c='black',linestyle='-',marker='',linewidth = 1)

def update(i):
    line2.set_data(mag_ang[:i],mag_abs[:i])
    line1.set_data(mag_ang[i],mag_abs[i])
    return line1, line2,

anim = animation.FuncAnimation(fig, update,interval=0, save_count=cycles, blit=True, repeat=False)
anim.save('roubntrail2.mp4',fps=30)
