Create random piecewise plots with Python. Dependencies are `matplotlib`, `numpy`, and `scipy`.

### example1.py

    import matplotlib.pyplot as plt
    import random_piecewise_plot as rpp

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    rpp.random_piecewise_plot(ax, n_segments=3, degrees=[1,2,3], n_continuous=1, n_jump_holes=1)
    plt.tight_layout()
    plt.show()

![](https://raw.githubusercontent.com/notmatthancock/random_piecewise_plot/master/example1.png)

### example2.py

    import matplotlib.pyplot as plt
    import random_piecewise_plot as rpp

    fig = plt.figure(figsize=(11,10))
    for i in range(9):
        ax  = fig.add_subplot(3,3,i+1)
        rpp.random_piecewise_plot(ax)
    plt.tight_layout()
    plt.show()

![](https://raw.githubusercontent.com/notmatthancock/random_piecewise_plot/master/example2.png)
