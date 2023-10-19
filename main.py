import read_json
import display_graph
import easygui 
import dash_input
import data_input
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

def main(filename, option, app):
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
        app.run(debug=True)


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
        app.layout = layout
        app.run(debug=True)

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
        app.layout = layout
        app.run(debug=True)

    else: 
        print("Invalid Input")


if __name__=='__main__':
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    filename=easygui.fileopenbox()
    option = input("What do you want to do? \n1 look at existing attack tree \n2 insert new node\n3 delete node\n")
    main(filename, option, app)