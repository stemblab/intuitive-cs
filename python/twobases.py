#!puzlet

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

def plot_lagrange(p,X,Y,labels):
    
    ax = fig.add_subplot(1,3,p+1,aspect='equal')

    # no spines on right/top
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    # axes
    def set_axis(axis, pos):
        axis.set_ticks_position(pos)
        spines = ax.spines[pos]
        spines.set_position(('data', 0))
        spines.set_color('grey')
        spines.set_zorder(0)  # place axis beneath everything else
    set_axis(ax.xaxis, 'bottom')
    set_axis(ax.yaxis, 'left')

    # line
    ax.plot(X, Y[p], color="black", linewidth=1, linestyle="-", zorder=1)
    sz = 150

    # limits, ticks, text
    ax.set_xlim(-1.5, 2.5)
    ax.set_ylim(-1,1.5)
    ax.set_xticks([-1,2])
    ax.set_xticklabels([r'$-1$',r'$2$'])
    ax.set_yticks([-1, 1])
    ax.set_yticklabels([])
    
    ax.text(0.4, -0.20, labels[p],
        verticalalignment='bottom', horizontalalignment='center',
        transform=ax.transAxes,
        color='grey', fontsize=14)

if __name__=="__main__":
    
    # Three functions
    functions = lambda x: [x*(x-2)/(-1)/(-1-2), (x+1)*(x-2)/(1.)/(-2.), 
        (x+1)*x/(3.)/(2.)]

    # Domain (X) and values (Y) for each function
    X = np.linspace(-3, 3, 50, endpoint=True)
    Y = functions(X)

    fig = plt.figure()
    labels = [r'$x(x-2)/3$', r'$-(x+1)(x-2)/2$', r'$x(x+1)/6$']

    for p in range(3):
        plot_lagrange(p,X,Y,labels)

    fig.savefig("lagrange_basis.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)

