#!puzlet

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

# Plot vector as line segement will ball at one end.
def plot_vec(start,end,label,color):
    ax.plot([start[0],end[0]],[start[1],end[1]],[start[2],end[2]],
        label=label,color=color,linewidth=2)
    ax.scatter(end[0],end[1],end[2],marker='o',color=color)

def set_axes():
    ax.set_autoscale_on(False)
    ax.set_xlabel(r'$x_0$',fontsize=20)
    ax.set_ylabel(r'$x_1$',fontsize=20)
    ax.set_zlabel(r'$x_2$',fontsize=20)
    ax.set_xlim(-0.8, 1.2)
    ax.set_ylim(-0.2, 1.2)
    ax.set_zlim(0, 1.4)
    ax.set_xticks([-0.5,0,0.5,1])
    ax.set_yticks([0,0.5,1])
    ax.set_zticks([0,0.5,1])
    
fig = plt.figure()
ax = fig.gca(projection='3d')
set_axes()
origin=[0,0,0]

plot_vec(origin,[1,0,0],label='constant',color='blue')
plot_vec(origin,[0,1,0],label='line',color='green')
plot_vec(origin,[0,0,1],label='parabola',color='red')
ax.legend()

fig.savefig("recon1_1.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)

ax.text(1.3,0,0.9, r'$Ax=b$', backgroundcolor='#fcffc9', 
        ha='center', va='bottom', size=18, zorder=10)

# Ax=b
A = np.array([[1, -1, 1], [1, 2, 4]])
b = np.array([1, 4])

# planes
x0 = np.arange(-1, 1, 0.1)
x1 = np.arange(-1, 1, 0.1)
xx0, yy0 = np.meshgrid(x0, x1)
ax.plot_surface(xx0, yy0, 1-xx0+yy0, 
    rstride=2, cstride=2, alpha=0.1, color='y')
ax.plot_surface(xx0, yy0, 1-xx0/4.-yy0/2.,
    rstride=2, cstride=2, alpha=0.1,color='m')

# solutuon to Ax=b
pinvA = np.linalg.pinv(A)
U = np.array([0,0,1]) # np.dot(pinvA,b)  # One solution
w = np.array([1.5, 0, 0]) # Arbitrary vector to get another solution
N = np.dot((np.eye(3) - np.dot(pinvA,A)),w)
ax.plot(*zip(U+N*2/3.,U-N*4/3.),color='k',linewidth=3,
    label=r'$x$ (not sparse)')

ax.legend()

fig.savefig("recon1_2.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)

ax.text(0,0,1.2, r'1-sparse $x$', backgroundcolor='#fcffc9', 
        ha='center', va='bottom', size=16, zorder=10)

ax.scatter(0,0,1,marker='*',s=400,color='r',label=r'$x$ (1-sparse)')
ax.legend()

fig.savefig("recon1_3.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)

def plot_norms(l, h, U):
    Nl = len(l)
    f, axarr = plt.subplots(Nl, 1)
    
    def plot(l, n):
        ax.set_title('$l_%s$-norm' % str(n))
        ax.scatter(np.array(h), np.array(l))
        # Show U value for minimum of norm
        #m = np.argmin(l)
        #l_min = l[m]
        #h_min = h[m]
        #U_min = U[m]        
        #ax_lim = ax.axis()
        #offset = -0.05*(ax_lim[3] - ax_lim[2])
        #v = lambda d: '{0:.2f}'.format(U_min[d])
        #label = "U=[%s, %s, %s]" % (v(0), v(1), v(2))
        #ax.text(h_min, l_min+offset, label, va='top')
    for n in range(Nl):
        ax = axarr[n]
        plot(l[n], n)
    plt.tight_layout()

Np = 201 # number of points to plot (Must be odd to include 0!)
h = np.array(np.linspace(-1, 1, Np))  # null vector multiplier
Y=U.reshape(3,1)+np.dot(N.reshape(3,1),h.reshape(1,Np)) 
# 3xNp array of x candidates

l=np.zeros((3,Np))
for n in range(3): 
    l[n,:] = np.apply_along_axis(np.linalg.norm, 0, Y, n)

# See: http://matplotlib.org/examples/axes_grid/demo_parasite_axes2.html

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

plt.clf()

host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=0.75)

par1 = host.twinx()
par2 = host.twinx()

offset = 60
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right",
                                    axes=par2,
                                    offset=(offset, 0))

par2.axis["right"].toggle(all=True)

host.set_xlim(-1, 1)
host.set_ylim(1, 3.5)

host.set_xlabel("Distance from Sparse Sorution ($d$)")
host.set_ylabel(r"$\||x\||_0$")
par1.set_ylabel(r"$\||x\||_1$")
par2.set_ylabel(r"$\||x\||_2$")

p1, = host.plot(h, l[0], label=r"$\||x\||_0$")
p2, = par1.plot(h, l[1], label=r"$\||x\||_1$")
p3, = par2.plot(h, l[2], label=r"$\||x\||_2$")

par1.set_ylim(1, 3)
par2.set_ylim(0, 2)

host.legend()

host.axis["left"].label.set_color(p1.get_color())
host.axis["left"].label.set_fontsize(20)
par1.axis["right"].label.set_color(p2.get_color())
par1.axis["right"].label.set_fontsize(20)
par2.axis["right"].label.set_color(p3.get_color())
par2.axis["right"].label.set_fontsize(20)

fig.savefig("norms.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)


