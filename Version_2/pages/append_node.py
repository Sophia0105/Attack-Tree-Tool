import dash
import read_json
import dash_input
import display_graph
from dash import dcc, html
import dash_bootstrap_components as dbc
import easygui


dash.register_page(__name__, path='/append')

filename=easygui.fileopenbox()
data = read_json.load(filename)
nr_vertices = len(read_json.create_nodes(data))
nodes = read_json.create_nodes(data)
node_types = read_json.get_nodeTypes(data)
edges = read_json.create_edges(data)

full_info = []
for i in range(nr_vertices):
    full_info.append(str(i) +  ": " +nodes[i])
nr_vertices_old = nr_vertices

new_stuff = display_graph.insert_node_types(nr_vertices, node_types, nodes, edges)
nr_vertices = new_stuff[0]
nodes = new_stuff[1]
node_types = new_stuff [2]
edges = new_stuff[3]

layout = dash_input.append_node(filename, nr_vertices, edges, nodes, node_types, nr_vertices_old)
