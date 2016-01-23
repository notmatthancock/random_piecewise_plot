import matplotlib.pyplot as plt
import random_piecewise_plot as rpp

fig = plt.figure(figsize=(11,10))
for i in range(9):
    ax  = fig.add_subplot(3,3,i+1)
    rpp.random_piecewise_plot(ax)
plt.tight_layout()
plt.show()
