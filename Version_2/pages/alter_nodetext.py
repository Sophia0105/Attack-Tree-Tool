import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import os

dash.register_page(__name__, path='/alter_text', name='Alter Node Text')

# storage = str(os.getcwd()) + "\\Storage.txt"
storage = "Storage.txt"
file = open(storage, "r")
filename= file.read()
data = read_json.load(filename)
nr_vertices = len(read_json.create_nodes(data))
last_node = data[-1]
id = last_node["id"] + 1

options_dropdown = []
for i in range(nr_vertices):
    text = "Node " + str(i)
    options_dropdown.append({"label": text, "value": i})

dropdown = dbc.Row(
    [
        dbc.Label("Node Number", html_for="dropdown_alter", width=2),
        dbc.Col(dcc.Dropdown(
            id='dropdown_alter',
            options=options_dropdown,
        ), width=10),
    ],
    className="mb-3",
)

node_text = dbc.Row(
    [
        dbc.Label("New Node Text", html_for="node_text", width=2),
        dbc.Col(dbc.Input(
            id="node_text", 
            placeholder="Enter the content of the node",
            ), width=10),
    ],
    className="mb-3",
)

insert_button = dbc.Row(
    [
        dbc.Label("Alter the node now", width=2),
        dbc.Col(dbc.Button("Alter", id='submit-val', n_clicks=0, href="/show_tree", class_name="button"), width=5),
        dbc.Col(html.Div(id='container-alter', children='No node altered untill now'), width=5)
    ]
)

@callback(
    Output('container-alter', 'children'),
    Input('submit-val', 'n_clicks'), 
    State('node_text', 'value'),
    State('dropdown_alter', 'value'),
    prevent_inital_call=True
)
def alter_output(n_clicks, n_text, node_nr):
    if n_clicks > 0:
        storage = str(os.getcwd()) + "\Storage.txt"
        storage = "Storage.txt"
        file = open(storage, "r")        
        filename= file.read()
        data_input.alter_text(filename, node_nr, n_text, nr_vertices)
        return "Altered"
    else: 
        pass

fig = display_graph.show_plot(filename)
figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig, id="alter_graph"),width=12))

update_button_alter= dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='update_alter', n_clicks=0, class_name="button"), width=5),
    ]
)

@callback(Output('alter_graph', 'figure'), Input('update_alter', 'n_clicks'))
def update_graph_alter(n):
    # storage = str(os.getcwd()) + "\Storage.txt"
    storage = "Storage.txt"
    file = open(storage, "r")
    filename= file.read()
    fig = display_graph.show_plot(filename)
    return fig

form = dbc.Form([dropdown, node_text, insert_button])
# form = dbc.Form([node_text, dropdown])
layout = dbc.Container([html.H1("Alter the node text", className='app-header'), form, update_button_alter, figure], fluid=True)