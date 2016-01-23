import matplotlib.pyplot as plt
import random_piecewise_plot as rpp

fig = plt.figure()
ax  = fig.add_subplot(111)
rpp.random_piecewise_plot(ax, n_segments=3, degrees=[1,2,3], n_continuous=1, n_jump_holes=1)
plt.tight_layout()
plt.show()
