from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import easygui
import read_json
import display_graph

def append_node(filename, nr_vertices, edges, nodes, nodeTypes, numbers):
    f_json = read_json.open_file(filename)
    last_node = f_json[-1]
    id = last_node["id"] + 1
    new_node = []

    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    node_text = dbc.Row(
        [
            dbc.Label("Node Text", html_for="node_text", width=2),
            dbc.Col(dbc.Input(
                id="node_text", 
                placeholder="Enter the content of the node",
                ), width=10),
        ],
        className="mb-3",
    )

    dropdown_1 = dbc.Row(
        [
            dbc.Label("Node Type", html_for="dropdown", width=2),
            dbc.Col(dcc.Dropdown(
                id="dropdown_1",
                options=[
                    {"label": "AND", "value": "and"},
                    {"label": "OR", "value": "or"},
                    {"label": "END", "value": "end"},
                ],
            ), width=10),
        ],
        className="mb-3",
    )

    dropdown_2 = dbc.Row(
        [
            dbc.Label("Parent Node Number", html_for="dropdown", width=2),
            dbc.Col(dcc.Dropdown(
                id="dropdown_2",
                options=[
                    {"label": "Node 1", "value": 1},
                    {"label": "Node 2", "value": 2},
                    {"label": "Node 3", "value": 3},
                ],
            ), width=10),
        ],
        className="mb-3",
    )

    fig = display_graph.show_plot_numbers(nr_vertices, edges, nodes, nodeTypes, numbers)
    figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig),width=12))

    form = dbc.Form([node_text, dropdown_1, dropdown_2])
    app.layout = dbc.Container([html.H1("Insert a new node"), form, figure], fluid=True)
    app.run(debug=True)



if __name__ == '__main__':
    filename = easygui.fileopenbox()
    data = read_json.load(filename)

    nr_vertices = len(read_json.create_nodes(data))
    nodes = read_json.create_nodes(data)
    node_types = read_json.get_nodeTypes(data)
    edges = read_json.create_edges(data)
    numbers = range(0, nr_vertices+1)

    new_stuff = display_graph.insert_node_types(nr_vertices, node_types, nodes, edges)
    nr_vertices = new_stuff[0]
    nodes = new_stuff[1]
    node_types = new_stuff [2]
    edges = new_stuff[3]

    append_node(filename, nr_vertices, edges, nodes, node_types, numbers)


