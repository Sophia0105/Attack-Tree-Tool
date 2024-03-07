import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/alter_probability', name='Alter Probability')

data = read_json.load()
nr_vertices = len(read_json.create_nodes(data))
last_node = data[-1]
id = last_node["id"] + 1

options_dropdown = []
for i in range(nr_vertices):
    text = "Node " + str(i)
    options_dropdown.append({"label": text, "value": i})

dropdown = dbc.Row(
    [
        dbc.Label("Node Number", html_for="dropdown_prob", width=2),
        dbc.Col(dcc.Dropdown(
            id='dropdown_prob',
            options=options_dropdown,
        ), width=8),
        dbc.Col(dbc.Button("Update Options", id='update_dropdown_prob', n_clicks=0, class_name="button"),width=2)
    ],
    className="mb-3",
)

@callback(
    Output('dropdown_prob', 'options'),
    Input('update_dropdown_prob', 'n_clicks')
)
def update_dropdown_prob(n):
    data = read_json.load()
    new_options = []
    for i in range(len(data)):
        text = "Node " + str(i)
        new_options.append({"label": text, "value": i})
    return new_options

prob_weight = dbc.Row(
    [
        dbc.Label("Enter altered probability for the node", html_for="input_prob", width=2),
        dbc.Col(dbc.Input(
            id="input_prob",
            type = "number",
            placeholder= "Input Number"
            ),
            width=10)
    ]
)

insert_button = dbc.Row(
    [
        dbc.Label("Alter the node now", width=2),
        dbc.Col(dbc.Button("Alter", id='submit-prob', n_clicks=0, class_name="button"), width=5),
        dbc.Col(html.Div(id='container-prob', children='No node altered untill now'), width=5)
    ]
)

@callback(
    Output('container-prob', 'children'),
    Input('submit-prob', 'n_clicks'), 
    State('input_prob', 'value'),
    State('dropdown_prob', 'value'),
    prevent_inital_call=True
)
def alter_output(n_clicks, prob_w, node_nr):
    if n_clicks > 0:
        data_input.alter_probability(node_nr, prob_w)
        return "Altered"
    else: 
        pass

fig = display_graph.show_plot()
figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig, id="prob_graph"),width=12))

update_button_alter= dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='update_prob', n_clicks=0, class_name="button"), width=5),
    ]
)

@callback(Output('prob_graph', 'figure'), Input('update_prob', 'n_clicks'))
def update_graph_alter(n):
    fig = display_graph.show_plot()
    return fig

form = dbc.Form([dropdown, prob_weight, insert_button])
layout = dbc.Container([html.H1("Alter the node probability", className='app-header'), form, update_button_alter, figure], fluid=True)