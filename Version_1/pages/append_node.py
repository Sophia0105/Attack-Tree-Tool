import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/append')


data = read_json.load()
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
            value="Example Text"
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
            value=0,
        ), width=8),
        dbc.Col(dbc.Button("Update Options", id='update_dropdown_p_options', n_clicks=0, class_name="button"),width=2)
    ],
    className="mb-3",
)

@callback(
    Output('dropdown_2', 'options'),
    Input('update_dropdown_p_options', 'n_clicks')
)
def update_dropdown_p_options(n):
    data = read_json.load()
    new_options = []
    for i in range(len(data)):
        text = "Node " + str(i)
        new_options.append({"label": text, "value": i})
    return new_options

edge_weight = dbc.Row(
    [
        dbc.Label("Enter edge weight for evaluation", html_for="edge_weight", width=2),
        dbc.Col(dcc.Dropdown(
            id='edge_weight',
            options=[{'label': 'Impossible', 'value':'I'},
                     {'label': 'Possible', 'value': 'P'}],
            value='I'
        ), width=10),
    ],
    className="mb-3",
)


insert_button = dbc.Row(
    [
        dbc.Label("Insert node with these attributes now", width=2),
        dbc.Col(dbc.Button("Insert", id='submit-val', n_clicks=0, class_name="button"), width=5),
        dbc.Col(html.Div(id='container-button-basic', children='No node inserted untill now'), width=5)
    ]
)

@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'), 
    State('node_text', 'value'),
    State('dropdown_2', 'value'),
    State('edge_weight', 'value'),
    prevent_inital_call=True
)
def update_output(n_clicks, node_text, parent_n, edge_w):
    if n_clicks > 0:
        data = read_json.load()
        id = len(data)
        new_node = [node_text, "end", id, True, parent_n, edge_w, 1]
        outp = data_input.append_node(new_node)
        data_input.correct_node_types()
        return outp
    else: 
        pass

fig = display_graph.show_plot()
figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig, id="append_graph"),width=12))

update_button_append = dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='update_append', n_clicks=0, class_name="button"), width=5),
    ]
)

@callback(Output('append_graph', 'figure'), Input('update_append', 'n_clicks'))
def update_graph_append(n):
    fig = display_graph.show_plot()
    return fig

form = dbc.Form([node_text, dropdown_2, edge_weight,insert_button])
layout = dbc.Container([html.H1("Insert a new node", className='app-header'), form, update_button_append, figure], fluid=True)