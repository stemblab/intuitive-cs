import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from itertools import cycle
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.axes_grid1.inset_locator \
    import inset_axes, zoomed_inset_axes
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

eps=np.finfo(float).eps
 
def inset(ax,instants,values,x,y,delta,ylim,colors):
    ax2 = inset_axes(ax, width=2, height=1, loc=2, bbox_to_anchor=(x,y), 
                    bbox_transform=ax.figure.transFigure)
    ax2.spines['right'].set_color('none')
    ax2.spines['top'].set_color('none')
    ax2.spines['left'].set_color('none')
    ax2.spines['bottom'].set_position(('data', 0))
    ax2.spines['bottom'].set_color('grey')
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_xlim(instants[0]-0.5,instants[-1]+0.5)
    ax2.set_ylim(ylim[0],ylim[1])

    color_cycle = cycle(colors)
    for ii in range(len(instants)):
        c=next(color_cycle)
        ax2.scatter(instants[ii],values[ii], marker='o', s=50,
            facecolor=c, edgecolor=c,zorder=2)
        hack = 0.0001 # avoid browser SVG rendering bug
        ax2.plot([instants[ii],instants[ii]+hack],[0,values[ii]],
            linestyle='-', color=c)
        ax2.text(instants[ii],values[ii]+delta*np.sign(values[ii]+eps),
            r'$b_%s=%s$'%(ii,values[ii]),ha='center',va='center',color=c)

    return ax2

def new_fig():

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.set_xlabel(r'$b_0$',color='k',fontsize=16)
    ax.set_ylabel(r'$b_1$',color='k',fontsize=16)
    ax.set_zlabel(r'$b_2$',color='k',fontsize=16)
    ax.w_xaxis.set_rotate_label(False)
    ax.w_yaxis.set_rotate_label(False)
    ax.w_zaxis.set_rotate_label(False)

    ax.tick_params(axis='x', colors='grey')
    ax.tick_params(axis='y', colors='grey')
    ax.tick_params(axis='z', colors='grey')

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_zlim(-0.25, 2.75)

    ax.view_init(30,330)
    ax.set_autoscale_on(False)
    
    return fig,ax

def vector(ax,y, label):
    colors = ['r', 'b', 'g']
    v = [0, 0, 0]
    w = v[:]
    for n, yp in enumerate(y):
        color = colors[n]
        x = v[n] + yp
        w[n] = x
        ax.plot([v[0], w[0]], [v[1], w[1]], [v[2], w[2]], color=color, 
                linestyle='--',linewidth=2)
        v[n] = x
    ax.plot([0, y[0]], [0, y[1]], [0, y[2]], color='k', linewidth=2)
    ax.scatter(y[0],y[1],y[2], marker='o', s=40, color='k')
    ax.text(0.5*y[0], 0.5*y[1], 0.5*y[2], label, backgroundcolor='#fcffc9', 
        ha='center', va='center', size=14)

def project_b1(ax, y, v):
    ax.plot([y[0],y[0]], [y[1], v], [y[2], y[2]], color='y', 
        linestyle=':')
    ax.plot([0, y[0]], [v, v], [0, y[2]], color='y', linewidth=2)
    ax.scatter(y[0], v, y[2], color='y', marker="*", s=100)

instants = np.array([-1,0,2])
constant = np.array([1,1,1]) 
line, parabola = np.array([-1,0,2]), np.array([1,0,4])
colors = ['r','b','g']
fig, ax = new_fig()

vector(ax, constant, r'$f(t)=x_0$')
inset(ax,instants,constant,x=0.55,y=0.65,delta=0.25,
    ylim=[-0.25,1.25], colors=colors)

fig.savefig("geom_1.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)

vector(ax, line, r'$f(t)=x_1 t$')
inset(ax,instants,line,x=0.05,y=0.55,delta=0.5,
    ylim=[-1.25,2.25],colors=colors)

fig.savefig("geom_2.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)

vector(ax, parabola, r'$f(t)=x_2 t^2$')
inset(ax,instants,parabola,x=0.225,y=0.9,delta=1,
    ylim=[-1.25,4.25],colors=colors)

fig.savefig("geom_3.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)

fig2, ax2 = new_fig()

ax2.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

vector(ax2, constant, r'$f(t)=x_0$')
vector(ax2, line, r'$f(t)=x_1 t$')
vector(ax2, parabola, r'$f(t)=x_2 t^2$')

plane = 1  # u1 plane
v = 1.5  # plane at b1=1.5
project_b1(ax2, constant, v)
project_b1(ax2, line, v)
project_b1(ax2, parabola, v)

fig.savefig("geom_4.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)

fig2 = plt.figure()
ax2 = fig2.gca()
ax2.set_ylim(-2,5)
colors=['r','#d3d3d3','g']
X=np.linspace(instants[0],instants[-1])

# left axis
ax2.spines['left'].set_color('green')
ax2.yaxis.label.set_color('green')
ax2.tick_params(axis='y', colors='green')
ax2.set_ylabel(r'$b_2$',color='green',fontsize='24')

# bottom axis
ax2.spines['bottom'].set_color('red')
ax2.xaxis.label.set_color('red')
ax2.tick_params(axis='x', colors='red')
ax2.set_xlabel(r'$b_0$',color='red',fontsize='24')

# stars
ax2.scatter(constant[0],constant[2], color='y', marker='*', s=200)
ax2.scatter(line[0],line[2], color='y', marker='*', s=200)
ax2.scatter(parabola[0],parabola[2], color='y', marker='*', s=200)

# lines
ax2.plot([0,constant[0]],[0,constant[2]], color='y')
ax2.plot([0,line[0]],[0,line[2]], color='y')
ax2.plot([0,parabola[0]],[0,parabola[2]], color='y')

# labels
ax2.text(0.5*constant[0], 0.5*constant[2], r'$x_0$', 
    backgroundcolor='#fcffc9', ha='center', va='center', size=18)
ax2.text(0.5*line[0], 0.5*line[2], r'$x_1 t$',
    backgroundcolor='#fcffc9', ha='center', va='center', size=18)
ax2.text(0.5*parabola[0], 0.5*parabola[2], r'$x_2 t^2$', 
    backgroundcolor='#fcffc9', ha='center', va='center', size=18)

# coordinates
ax2.text(constant[0]+0.1, constant[2], r'$[1,1]^T$', 
    backgroundcolor='w', ha='left', va='center', size=16)
ax2.text(line[0], line[2]+0.3, r'$[-1,2]^T$', 
    backgroundcolor='w', ha='center', va='bottom', size=16)
ax2.text(parabola[0]+0.1, parabola[2], r'$[1,4]^T$',
    backgroundcolor='w', ha='left', va='center', size=16)

# constant, line, parabola
ax_ins=inset(ax2,instants,constant,x=0.6,y=0.3,delta=0.25,
    ylim=[-0.25,1.25],colors=colors)
ax_ins.plot(X,X**0,linestyle='--',color='k')
ax_ins=inset(ax2,instants,line,x=0.15,y=0.35,delta=0.5,
    ylim=[-1.25,2.25],colors=colors)
ax_ins.plot(X,X**1,linestyle='--',color='k')
ax_ins=inset(ax2,instants,parabola,x=0.4,y=0.825,delta=1,
    ylim=[-1.25,4.25],colors=colors)
ax_ins.plot(X,X**2,linestyle='--',color='k')

fig.savefig("spark_1.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)
