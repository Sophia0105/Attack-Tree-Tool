import os
import signal
import PySide6.QtCore
from PySide6.QtWidgets import QApplication, QLabel
from NodeGraphQt import NodeGraph, BaseNode
from NodeGraphQt.constants import PipeLayoutEnum

class FooNode(BaseNode):

    __identifier__ = 'test01'

    NODE_NAME= 'test01'

    def __init__(self):
        super(FooNode, self).__init__()
        self.add_input('in', color=(180,80,0))
        self.add_output('out')

if __name__ == '__main__':
    app = QApplication([])
    label = QLabel('Hello World')
    label.show()
    graph = NodeGraph()
    graph.register_node(FooNode)
    graph_widget = graph.widget
    graph_widget.show()

    node_a = graph.create_node('test01.FooNode', name='node A')
    node_b = graph.create_node('test01.FooNode', name='node B', pos=(300,50))

    node_a.set_output(0, node_b.input(2))
    app.exec_()
