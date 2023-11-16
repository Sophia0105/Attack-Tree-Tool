import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/alter_weight', name='Alter Edge Weigth')

data = read_json.load()
nr_vertices = len(read_json.create_nodes(data))
last_node = data[-1]
id = last_node["id"] + 1

options_dropdown = []
for i in range(nr_vertices):
    if i > 0:
        text = "Node " + str(i)
        options_dropdown.append({"label": text, "value": i})

dropdown = dbc.Row(
    [
        dbc.Label("Node Number", html_for="dropdown_edge", width=2),
        dbc.Col(dcc.Dropdown(
            id='dropdown_edge',
            options=options_dropdown,
        ), width=8),
        dbc.Col(dbc.Button("Update Options", id='update_dropdown_edge', n_clicks=0),width=2)
    ],
    className="mb-3",
)

@callback(
    Output('dropdown_edge', 'options'),
    Input('update_dropdown_edge', 'n_clicks')
)
def update_dropdown_edge(n):
    data = read_json.load()
    new_options = []
    for i in range(len(data)):
        if i > 0:
            text = "Node " + str(i)
            new_options.append({"label": text, "value": i})
    return new_options

edge_weight = dbc.Row(
    [
        dbc.Label("Enter edge weight for connection to parent node", html_for="input_edge", width=2),
        dbc.Col(dbc.Input(
            id="input_edge",
            type = "number",
            placeholder= "Input Number"
            ),
            width=10)
    ]
)

insert_button = dbc.Row(
    [
        dbc.Label("Alter the node now", width=2),
        dbc.Col(dbc.Button("Alter", id='submit-edge', n_clicks=0, class_name="button"), width=5),
        dbc.Col(html.Div(id='container-edge', children='No node altered untill now'), width=5)
    ]
)

@callback(
    Output('container-edge', 'children'),
    Input('submit-edge', 'n_clicks'), 
    State('input_edge', 'value'),
    State('dropdown_edge', 'value'),
    prevent_inital_call=True
)
def alter_output(n_clicks, edge_w, node_nr):
    if n_clicks > 0:
        data_input.alter_edge(node_nr, edge_w)
        return "Altered"
    else: 
        pass

fig = display_graph.show_plot()
figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig, id="edge_graph"),width=12))

update_button_alter= dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='update_edge', n_clicks=0, class_name="button"), width=5),
    ]
)

@callback(Output('edge_graph', 'figure'), Input('update_edge', 'n_clicks'))
def update_graph_alter(n):
    fig = display_graph.show_plot()
    return fig

form = dbc.Form([dropdown, edge_weight, insert_button])
layout = dbc.Container([html.H1("Alter the node text", className='app-header'), form, update_button_alter, figure], fluid=True)