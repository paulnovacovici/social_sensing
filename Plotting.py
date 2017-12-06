import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

class Plotting(object):
    style.use('fivethirtyeight')
    def __init__(self, xs=None,ys=None):
        self.fig = plt.figure()
        self.axl = self.fig.add_subplot(1,1,1)
        self.xs = xs if xs is not None else []
        self.ys = ys if ys is not None else []

    def animate(self, i):
        # Pull from database in future
        self.axl.clear()
        self.axl.plot(self.xs,self.ys)

    def set_xy(self, xs, ys):
        self.xs = xs
        self.ys = ys

    def get_xs(self):
        print(self.xs)
        return self.xs

    def get_ys(self):
        return self.ys

    def start_plotting(self):
        ani = animation.FuncAnimation(self.fig,self.animate, interval=1000)
        plt.show()
