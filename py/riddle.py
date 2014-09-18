import numpy as np

def plot123(fig,p,X,Y,a,b,labels,col):
    
    ax = fig.add_subplot(1,3,p+1)

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

    # line and markers
    ax.plot(X, Y[p], color="black", linewidth=1.5, linestyle="-", zorder=1)
    sz = 150
    for n in range(len(a)):
        ax.scatter(a[n], b[p][n],marker="o", s=sz, facecolor=col[n], 
                    edgecolor=col[n], zorder=2)

    # limits, ticks, text
    ax.set_xlim(a[0]-1, a[-1]+1)
    ax.set_ylim(np.min(b)-1, np.max(b)+1)
    ax.set_xticks([a[0], a[-1]])
    ax.set_xticklabels([r'$%s$'%a[0], r'$t=%s$'%a[-1]])
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.text(1.03, 0.01, labels[p],
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        color='grey', fontsize=14)
    ax.tick_params(axis='x', colors='grey')
    
if __name__=="__main__":

    # Do not want these imported along with plot123
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    # Three functions
    hack = 0.0001 # avoid browser SVG rendering bug
    functions = lambda x: [1+hack*x, x, 0.5*x**2]

    # Domain (X) and values (Y) for each function
    X = np.linspace(-3, 3, 50, endpoint=True)
    Y = functions(X)

    # Samples
    a = np.array([-1, 0, 2]) # instants
    b = functions(a) # values

    # Labels and sample colors (for each graph)
    labels = [r'$f(t)=x_0$', r'$f(t)=x_1 t$', r'$f(t)=x_2 t^2$']
    col = ['red', 'blue', 'green']  # For sample points in each graph

    fig = plt.figure(figsize=(8,2))
    for p in range(3): plot123(fig,p,X,Y,a,b,labels,col)

    fig.savefig("riddle.svg", transparent=True, bbox_inches='tight', pad_inches=0.15)

