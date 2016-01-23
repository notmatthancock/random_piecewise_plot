import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline

def random_piecewise_plot(
    ax,
    n_segments=3,
    n_continuous=1,
    max_degree=3,
    n_jump_holes=2,
    degrees=None ):
    """
    Generate a random piecewise plot on the interval: [0,n_segments].

    ax: matplotlib axis
        The function will plot to this axis.

    n_segments: int
        Number of segments the function will span. A segment is of unit length.

    n_continuous: int
        The plot will be continuous across the n_continuous intervals, meaning n_continuous interval partition points will be chosen at random, and the function will be continuous across the adjoining intervals.

    degrees: list, default None
        If degrees is None, the degree of the spline on each interval is of random degree between 1 and max_degree. Otherwise, degrees should be a list specifying the degree on each interval.

    n_jump_holes: int
        This will place random single point discontinuities in the middle of random intervals
    """
    assert n_continuous <= n_segments-1
    if degrees is not None:
        assert len(degrees) == n_segments
    else:
        degrees = np.random.randint(1,max_degree+1,size=n_segments)
    assert n_jump_holes <= n_segments

    N = 100 # resample resolution on each interval
    x = np.linspace(0,n_segments,n_segments*N)
    y = np.zeros_like(x)

    continuous_points = np.sort(np.random.choice(range(n_segments-1), size=n_continuous, replace=False))
    knots = []

    # Create the knots.
    for i in range(n_segments):
        xi = np.linspace(i,i+1,degrees[i]+1)
        yi = np.zeros_like(xi)
        yi[[0,-1]] = np.random.randint(-6,7,size=2) / 2.0
        if xi.shape[0] > 2:
            yi[1:-1] = np.random.randn(xi.shape[0]-2)
        knots.append((xi,yi))

    # Tie knots, and evaluate function points via spline to create y array.
    for i in range(n_segments):
        if i in continuous_points:
            knots[i][1][-1] = knots[i+1][1][0] # tie the knot
        elif i != n_segments-1:
            s = 0.5 if np.random.rand() < 0.5 else -0.5
            s *= np.random.randint(1,4)
            knots[i][1][-1] = knots[i+1][1][0] + s
        y[i*N:(i+1)*N] = spline(knots[i][0],knots[i][1],x[i*N:(i+1)*N],order=degrees[i])

    # Determine connected segments.
    segments = [[i,i+1] for i in range(n_segments)]
    pop_list = []

    # By collecting connected segments, we can plot according to these
    # segments, so that the graph appears continuous visually across segments.
    for j in range(n_segments):
        check_c_pts = True
        for s in segments[:j]:
            if s[1] >= segments[j][1]:
                pop_list.append(j)
                check_c_pts = False
                break
        if check_c_pts and j in continuous_points:
            segments[j][1] += 1
            k = j+1; i = np.where(continuous_points==j)[0][0]+1
            while i < len(continuous_points) and k==continuous_points[i]:
                segments[j][1] += 1
                i += 1
                k += 1
    segments = [s for j,s in enumerate(segments) if j not in pop_list]
            
    for s in segments:
        ax.plot(x[s[0]*N:s[1]*N], y[s[0]*N:s[1]*N],'-k',lw=3)

    # Draw open / closed interval markers.
    for i in range(n_segments-1):
        if i in continuous_points: continue

        # Otherwise, randomly choose the left / right segment to be open / closed
        if np.random.rand() < 0.5: L,R = 'w','k'
        else:            L,R = 'k','w'
        ax.plot(knots[ i ][0][-1],knots[ i ][1][-1],'o',ms=10,markeredgecolor='k',markerfacecolor=L)
        ax.plot(knots[i+1][0][ 0],knots[i+1][1][ 0],'o',ms=10,markeredgecolor='k',markerfacecolor=R)

    # Draw jump holes
    for i in np.random.choice(range(n_segments),size=n_jump_holes,replace=False):
        jx = i+0.5; jy = y[i*N+N/2].round(); 
        r = 0.5*(np.random.randint(1,4))
        jy += -r if np.random.rand() < 0.5 else r
        if np.random.rand()<0.5:
            ax.plot(jx, jy, 'o', ms=10, markeredgecolor='k', markerfacecolor='k')
        ax.plot(jx, y[i*N+N/2], 'o', ms=10, markeredgecolor='k', markerfacecolor='w')
        y[i*N+N/2] = jy

    ax.set_xlim(-0.5,n_segments+0.5)
    ax.set_xticks(np.arange(0,n_segments+0.5,0.5))

    ymin = y.min().round()-0.5
    ymax = y.max().round()+0.5

    ax.set_ylim(y.min()-0.5,y.max()+0.5)
    ax.set_yticks(np.arange(ymin,ymax+0.5,0.5))
    ax.set_xlabel('$x$',fontsize=20); ax.set_ylabel('$f(x)$',fontsize=20)
    ax.set_axisbelow(True)
    ax.grid('on')
