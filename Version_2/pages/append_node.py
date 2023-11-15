import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import os

dash.register_page(__name__, path='/append')


storage = str(os.getcwd()) + "\Storage.txt"
file = open(storage, "r")
filename= file.read()
data = read_json.load(filename)
nr_vertices = len(read_json.create_nodes(data))
last_node = data[-1]
id = last_node["id"] + 1


options_dropdown2 = []
for i in range(nr_vertices):
    text = "Node " + str(i)
    options_dropdown2.append({"label": text, "value": i})

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

dropdown_2 = dbc.Row(
    [
        dbc.Label("Parent Node Number", html_for="dropdown", width=2),
        dbc.Col(dcc.Dropdown(
            id="dropdown_2",
            options=options_dropdown2,
        ), width=10),
    ],
    className="mb-3",
)

insert_button = dbc.Row(
    [
        dbc.Label("Insert node with these attributes now", width=2),
        dbc.Col(dbc.Button("Insert", id='submit-val', n_clicks=0, href="/show_tree"), width=5),
        dbc.Col(html.Div(id='container-button-basic', children='No node inserted untill now'), width=5)
    ]
)

@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'), 
    State('node_text', 'value'),
    State('dropdown_2', 'value'),
    prevent_inital_call=True
)
def update_output(n_clicks, value1, value3):
    if n_clicks > 0:
        storage = str(os.getcwd()) + "\Storage.txt"
        file = open(storage, "r")        
        filename= file.read()
        new_node = [value1, "end", id, True, value3]
        data_input.append_node(filename, new_node)
        data_input.correct_node_types(filename)
        return "Inserted {}. node: (id: {}), (text: {}), (type: {}), (parent: {})".format(n_clicks, id , value1, "end", str(value3))
    else: 
        pass

fig = display_graph.show_plot(filename)
figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig, id="append_graph"),width=12))

update_button_append = dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='update_append', n_clicks=0), width=5),
    ]
)

@callback(Output('append_graph', 'figure'), Input('update_append', 'n_clicks'))
def update_graph_append(n):
    storage = str(os.getcwd()) + "\Storage.txt"
    file = open(storage, "r")
    filename= file.read()
    fig = display_graph.show_plot(filename)
    return fig

form = dbc.Form([node_text, dropdown_2, insert_button])
layout = dbc.Container([html.H1("Insert a new node", className='app-header'), form, update_button_append, figure], fluid=True)