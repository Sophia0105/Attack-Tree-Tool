from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import easygui
import read_json
import display_graph
import data_input

def append_node(filename, nr_vertices, edges, nodes, nodeTypes, nr_vertices_old):
    f_json = read_json.open_file(filename)
    last_node = f_json[-1]
    id = last_node["id"] + 1
    new_node = []

    options_dropdown2 = []
    for i in range(nr_vertices_old):
        text = "Node " + str(i)
        options_dropdown2.append({"label": text, "value": i})


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
                # options=[
                #     {"label": "Node 1", "value": 1},
                #     {"label": "Node 2", "value": 2},
                #     {"label": "Node 3", "value": 3},
                # ],
                options=options_dropdown2,
            ), width=10),
        ],
        className="mb-3",
    )

    insert_button = dbc.Row(
        [
            dbc.Label("Insert node with these attributes now", width=2),
            dbc.Col(html.Button("Insert", id='submit-val', n_clicks=0), width=5),
            dbc.Col(html.Div(id='container-button-basic', children='No node inserted untill now'), width=5)
        ]
    )

    @callback(
        Output('container-button-basic', 'children'),
        Input('submit-val', 'n_clicks'), 
        State('node_text', 'value'),
        State('dropdown_1', 'value'),
        State('dropdown_2', 'value'),
        prevent_inital_call=True
    )
    def update_output(n_clicks, value1, value2, value3):
        if n_clicks > 0:
            new_node.append(value1)
            new_node.append(value2)
            new_node.append(id)
            new_node.append(True)
            new_node.append(value3)
            data_input.append_node(filename, new_node)
            return "Inserted {}. node: (id: {}), (text: {}), (type: {}), (parent: {})".format(n_clicks, id, value1, str(value2), str(value3))
        else: 
            pass

    fig = display_graph.show_plot_numbers(nr_vertices, edges, nodes, nodeTypes)
    figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig),width=12))

    form = dbc.Form([node_text, dropdown_1, dropdown_2, insert_button])
    app.layout = dbc.Container([html.H1("Insert a new node"), form, figure], fluid=True)
    app.run(debug=True)



