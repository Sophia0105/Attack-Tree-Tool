
import numpy as np

import pyqtgraph as pg

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

w = pg.GraphicsLayoutWidget(show=True)
w.setWindowTitle('pyqtgraph example: GraphItem')
v = w.addViewBox()
v.setAspectLocked()

g = pg.GraphItem()
v.addItem(g)

pos = np.array([[0,0],[10,0],[10,10], [20,0], [20,10]])
adj= np.array([[0,1], [0,2], [1,3], [2,4]])
# symbols = ['text','text','text','text','text']
symbols = ['s', 's', 's','s','s']
# name = ['virus infects a file', 'a', 'a', 'a', 'a']

g.setData(pos=pos, adj=adj, size=1, symbol=symbols, pxMode=False)

if __name__ == '__main__':
    pg.exec()