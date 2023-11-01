import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/delete')

def layout():
    file = open("D:\TH\Bachelorarbeit\Attack Tree Modellierer\Version_2\Storage.txt", "r")
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
            dbc.Col(dbc.Button("Submit", id='submit', n_clicks=0, href="/"), width=5),
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
            deleted_node = data_input.delete_node(filename, nr_vertices, int(value))
            return "{}. nodes deleted -- last one: (id: {}), (text: {}), (type: {}), (parent: {})".format(n_clicks, str(deleted_node["id"]), deleted_node["text_string"], deleted_node["node_type"], str(deleted_node["parentnode_number"]))
        else:
            pass


    fig = display_graph.show_plot(filename)
    figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig),width=12))
    form = dbc.Form([dropdown, submit_button])
    layout = dbc.Container([html.H1("Delete a Node"), form, figure], fluid=True)
    return layout