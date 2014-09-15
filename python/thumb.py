#!puzlet

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

# parabola
X = np.linspace(-3, 3, 50, endpoint=True)
Y = 0.5*X**2 # functions(X)

# samples
a = np.array([-1, 0, 2]) # instants
b = np.array([1,0,1]) # values

fig = plt.figure(figsize=(2,2))
ax = fig.add_subplot(1,1,1)

# no spines on right/top
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# axes
def set_axis(axis, pos):
    axis.set_ticks_position(pos)
    spines = ax.spines[pos]
    spines.set_position(('data', 0))
    spines.set_color('black')
    spines.set_zorder(0)  # place axis beneath everything else
set_axis(ax.xaxis, 'bottom')
set_axis(ax.yaxis, 'left')

# line and markers
ax.plot(X, Y, color="black", linewidth=4, linestyle="-", zorder=1)
sz = 300
ax.scatter(-1,0.5,marker="o",s=sz,facecolor='r',edgecolor='r',zorder=2)
ax.scatter(0,0,marker="o",s=sz,facecolor='b',edgecolor='b',zorder=2)
ax.scatter(2,2,marker="o",s=sz,facecolor='g',edgecolor='g',zorder=2)

# limits, ticks, text
ax.set_xlim(a[0]-1, a[-1]+1)
ax.set_ylim(-1, 3)
ax.set_xticks([])
ax.set_yticklabels([])
ax.set_yticks([])
ax.set_yticklabels([])

fig.savefig("thumb.png", transparent=True, bbox_inches='tight', pad_inches=0.15)
