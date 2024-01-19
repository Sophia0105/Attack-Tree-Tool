import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/alter_parent', name='Alter Parent Node')

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
        dbc.Label("Node Number", html_for="dropdown_nr", width=2),
        dbc.Col(dcc.Dropdown(
            id='dropdown_nr',
            options=options_dropdown,
        ), width=8),
        dbc.Col(dbc.Button("Update Options", id='update_dropdown_options', n_clicks=0, class_name="button"),width=2)
    ],
    className="mb-3",
)

@callback(
    Output('dropdown_nr', 'options'),
    Input('update_dropdown_options', 'n_clicks')
)
def update_dropdown_options(n):
    data = read_json.load()
    new_options = []
    for i in range(len(data)):
        if i > 0:
            text = "Node " + str(i)
            new_options.append({"label": text, "value": i})
    return new_options

options_dropdown_p = []
for i in range(nr_vertices):
    text = "Node " + str(i)
    options_dropdown.append({"label": text, "value": i})

dropdown_parent = dbc.Row(
    [
        dbc.Label("New Parent Node Number", html_for="dropdown_parent", width=2),
        dbc.Col(dcc.Dropdown(
            id='dropdown_parent',
            options=options_dropdown_p,
        ), width=8),
        dbc.Col(dbc.Button("Update Options", id='update_dropdown_parent_options', n_clicks=0, class_name="button"),width=2)
    ],
    className="mb-3",
)

@callback(
    Output('dropdown_parent', 'options'),
    Input('update_dropdown_parent_options', 'n_clicks')
)
def update_dropdown_parent_options(n):
    data = read_json.load()
    new_options = []
    for i in range(len(data)):
        text = "Node " + str(i)
        new_options.append({"label": text, "value": i})
    return new_options

insert_button = dbc.Row(
    [
        dbc.Label("Alter the node now", width=2),
        dbc.Col(dbc.Button("Alter", id='submit-parent', n_clicks=0, class_name="button"), width=5),
        dbc.Col(html.Div(id='container-alter-parent', children='No node altered untill now'), width=5)
    ]
)

@callback(
    Output('container-alter-parent', 'children'),
    Input('submit-parent', 'n_clicks'), 
    State('dropdown_parent', 'value'),
    State('dropdown_nr', 'value'),
    prevent_inital_call=True
)
def alter_output(n_clicks, n_parent, node_nr):
    if n_clicks > 0:
        alteration = data_input.alter_parent(node_nr, n_parent)
        data_input.correct_node_types()
        return alteration
    else: 
        pass

fig = display_graph.show_plot()
figi= dbc.Row(dbc.Col(dcc.Graph(figure=fig, id="alter_parent_graph"),width=12))

update_button_type= dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='update-parent', n_clicks=0, class_name="button"), width=5),
    ]
)

@callback(Output('alter_parent_graph', 'figure'), Input('update-parent', 'n_clicks'))
def update_graph_alter(n):
    fig = display_graph.show_plot()
    return fig

form = dbc.Form([dropdown, dropdown_parent, insert_button])
# form = dbc.Form([dropdown, dropdown_type])
layout = dbc.Container([html.H1("Alter the parent node", className='app-header'), form, update_button_type, figi], fluid=True)