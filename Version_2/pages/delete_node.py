import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/delete')


file = open("D:\TH\Bachelorarbeit\Attack Tree Modellierer\Storage.txt", "r")
filename= file.read()
data = read_json.load(filename)
nr_vertices = len(read_json.create_nodes(data))

options_dropdown = []
for i in range(nr_vertices):
    text = "Node " + str(i)
    options_dropdown.append({"label": text, "value": i})

dropdown = dbc.Row(
    [
        dbc.Label("Delete the node with the following id: ", html_for="dropdown", width=2),
        dbc.Col(dcc.Dropdown(
            id="dropdown",
            options=options_dropdown,
        ), width=10),
    ],
    className="mb-3",
)

submit_button = dbc.Row(
    [
        dbc.Label("If you really want to delete the node, press the button", width=2),
        dbc.Col(dbc.Button("Submit", id='submit', n_clicks=0, href="/show_tree"), width=5),
        dbc.Col(html.Div(id='button-container', children='Nothing deleted yet'), width=5)
    ]
)

@callback(
    Output('button-container', 'children'),
    Input('submit', 'n_clicks'),
    State('dropdown', 'value'),
    prevent_inital_call=True
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        deleted_node = data_input.delete_node(filename, nr_vertices, value)
        return "{}. nodes deleted -- last one: (id: {}), (text: {}), (type: {}), (parent: {})".format(n_clicks, str(deleted_node["id"]), deleted_node["text_string"], deleted_node["node_type"], str(deleted_node["parentnode_number"]))
    else:
        pass


update_button_append = dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='update_delete', n_clicks=0), width=5),
    ]
)

@callback(Output('delete_graph', 'figure'), Input('update_delete', 'n_clicks'))
def update_graph_delete(n):
    fig = display_graph.show_plot(filename)
    return fig

# update_button_delete2 = dbc.Row(
#     [
#         dbc.Label("Update graph", width=2),
#         dbc.Col(dbc.Button("Update Graph", id='update_delete_options', n_clicks=0), width=5),
#     ]
# )

# @callback(Output('dropdown','options'), Input('update_delete_options', 'n_clicks'))
# def update_options_delete(n):
#     data = read_json.load(filename)
#     nr_vertices = len(read_json.create_nodes(data))

#     options_dropdown = []
#     for i in range(nr_vertices):
#         text = "Node " + str(i)
#         options_dropdown.append({"label": text, "value": i})
#     return options_dropdown


fig = display_graph.show_plot(filename)
figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig, id="delete_graph"),width=12))
form = dbc.Form([dropdown, submit_button])
layout = dbc.Container([html.H1("Delete a Node", className='app-header'), form, figure], fluid=True)