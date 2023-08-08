from pyqtgraph.flowchart import Flowchart
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

app = pg.mkQApp("Flowchart Example")

## Create main window with grid layout
win = QtWidgets.QMainWindow()
win.setWindowTitle('pyqtgraph example: Flowchart')
cw = QtWidgets.QWidget()
win.setCentralWidget(cw)
layout = QtWidgets.QGridLayout()
cw.setLayout(layout)

## Create flowchart, define input/output terminals
fc = Flowchart(terminals={
    'dataIn': {'io': 'in'},
    'dataOut': {'io': 'out'},
    'dataOut2' : {'io': 'out2'}    
})
w = fc.widget()

# node1 = fc.createNode('Add')

layout.addWidget(fc.widget(), 0, 0, 2, 1)
win.show()
fc.setInput(dataIn='newValue')
output = fc.output()
output = fc.process(dataIn='newValue')

if __name__ == '__main__':
    pg.exec()