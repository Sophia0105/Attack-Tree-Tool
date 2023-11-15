import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/alter_type', name='Alter Node Type')

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
        dbc.Label("Node Number", html_for="dropdown_nr", width=2),
        dbc.Col(dcc.Dropdown(
            id='dropdown_nr',
            options=options_dropdown,
        ), width=10),
    ],
    className="mb-3",
)

dropdown_type = dbc.Row(
    [
        dbc.Label("Node Number", html_for="dropdown_type", width=2),
        dbc.Col(dcc.Dropdown(
            id='dropdown_type',
            options=[{'label': 'END', 'value':'end'},
                     {'label': 'AND', 'value': 'and'},
                     {'label': 'OR', 'value': 'or'}],
            value='end'
        ), width=10),
    ],
    className="mb-3",
)

insert_button = dbc.Row(
    [
        dbc.Label("Alter the node now", width=2),
        dbc.Col(dbc.Button("Alter", id='submit-val', n_clicks=0, class_name="button"), width=5),
        dbc.Col(html.Div(id='container-alter-type', children='No node altered untill now'), width=5)
    ]
)

@callback(
    Output('container-alter-type', 'children'),
    Input('submit-val', 'n_clicks'), 
    State('dropdown_type', 'value'),
    State('dropdown_nr', 'value'),
    prevent_inital_call=True
)
def alter_output(n_clicks, n_type, node_nr):
    if n_clicks > 0:
        data_input.alter_type(node_nr, n_type)
        right = data_input.correct_node_types()
        return "Errors: {} if True alteration can not be conducted".format(right)
    else: 
        pass

fig = display_graph.show_plot()
figi= dbc.Row(dbc.Col(dcc.Graph(figure=fig, id="alter_type_graph"),width=12))

update_button_type= dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='update_type', n_clicks=0, class_name="button"), width=5),
    ]
)

@callback(Output('alter_type_graph', 'figure'), Input('update_type', 'n_clicks'))
def update_graph_alter(n):
    fig = display_graph.show_plot()
    return fig

form = dbc.Form([dropdown, dropdown_type, insert_button])
layout = dbc.Container([html.H1("Alter the node type", className='app-header'), form, update_button_type, figi], fluid=True)
