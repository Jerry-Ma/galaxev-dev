from __future__ import print_function
from matplotlib.pyplot import figure, show
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text
from matplotlib.image import AxesImage
import numpy as np
from numpy.random import rand

 # picking on a scatter plot (matplotlib.collections.RegularPolyCollection)

x, y, c, s = rand(4, 100)

def onmove(event):
   # if col.contains(event):
    #   # print ('in')
    #else:
        #print ('out')
    #col.pick(event)
    pass
def onpick3(event):
    ind = event.ind

    colors = col.get_facecolor()
    colors[ind] = np.abs([[1, 1, 1, 0]] - colors[ind])
    col.set_facecolor(colors)
    fig.canvas.draw()
    #print (colors)
#    1 - col.get_facecolor()[ind]
    #print ('onpick3 scatter:', ind, np.take(x, ind), np.take(y, ind))

fig = figure()
ax1 = fig.add_subplot(111)
col = ax1.scatter(x, y, 100 * s, c, picker=True)
col.in_o = False
col.in_new = True
#fig.savefig('pscoll.eps')
fig.canvas.mpl_connect('pick_event', onpick3)
#col.pick()
fig.canvas.mpl_connect('motion_notify_event', col.pick)
show()