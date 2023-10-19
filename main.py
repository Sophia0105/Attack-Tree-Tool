import read_json
import display_graph
import easygui 
import dash_input
import data_input
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from pick import pick

def generate_layout(filename, option):
    data = read_json.load(filename)
    nr_vertices = len(read_json.create_nodes(data))
    nodes = read_json.create_nodes(data)
    node_types = read_json.get_nodeTypes(data)
    edges = read_json.create_edges(data)

    if int(option) == 1:
        # open attack tree
        new_stuff = display_graph.insert_node_types(nr_vertices, node_types, nodes, edges)
        nr_vertices = new_stuff[0]
        nodes = new_stuff[1]
        node_types = new_stuff [2]
        edges = new_stuff[3]

        fig = display_graph.show_plot(nr_vertices, edges, nodes, node_types)
        figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig),width=12))

        layout = dbc.Container([html.H1("Current Attack Tree"), figure], fluid=True)
        return layout

    elif int(option) == 2: 
        #insert new node
        full_info = []
        for i in range(nr_vertices):
            full_info.append(str(i) +  ": " +nodes[i])

        new_stuff = display_graph.insert_node_types(nr_vertices, node_types, full_info, edges)
        nr_vertices_old = nr_vertices
        nr_vertices = new_stuff[0]
        nodes = new_stuff[1]
        node_types = new_stuff [2]
        edges = new_stuff[3]

        layout = dash_input.append_node(filename, nr_vertices, edges, nodes, node_types, nr_vertices_old)
        return layout

    elif int(option) == 3:
        full_info = []
        for i in range(nr_vertices):
            full_info.append(str(i) +  ": " +nodes[i])

        new_stuff = display_graph.insert_node_types(nr_vertices, node_types, full_info, edges)
        nr_vertices_old = nr_vertices
        nr_vertices = new_stuff[0]
        nodes = new_stuff[1]
        node_types = new_stuff [2]
        edges = new_stuff[3]

        layout = dash_input.delete_node(filename, nr_vertices, edges, nodes, node_types, nr_vertices_old)
        return layout

    else: 
        print("Invalid Input")


def main():
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    filename=easygui.fileopenbox()

    options = ['look at existing attack tree', 'insert new node', 'delete node']
    _, option_idx = pick(options, 'What do you want to do?')

    layout = generate_layout(filename, option_idx)
    
    app.layout = layout
    app.run(debug=True)


if __name__=='__main__':
    main()