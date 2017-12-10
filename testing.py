from random import randint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use ('fivethirtyeight')

fig = plt.figure()
axl = fig.add_subplot(1,1,1)

def randints(num):
    arr = []
    for i in range(num):
        arr += [randint(1,100)]
    return arr


def animate(i):
    global xs, ys
    xs.append(xs[-1]+1)
    ys.append(randint(1,100))
    axl.clear()
    axl.plot(xs,ys)

xs = [1,2,3,4,5,6,7,8,9]
ys = randints(9)

ani = animation.FuncAnimation(fig,animate, interval=1000)
plt.show()
