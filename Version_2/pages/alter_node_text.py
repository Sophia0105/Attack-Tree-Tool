import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc


# Register page to the dash app, set path to reach the side and the name which will be displayed
dash.register_page(__name__, path='/alter_text', name='Alter Node Text')

# Load and set data which has to be processed
data = read_json.load()
nr_vertices = len(read_json.create_nodes(data))
last_node = data[-1]
id = last_node["id"] + 1

# Creates list of options for the dropdown menu to select a node
options_dropdown = []
for i in range(nr_vertices):
    text = "Node " + str(i)
    options_dropdown.append({"label": text, "value": i})

# Drop-down menu for selecting a node number and the attached button for updating the selectable options
dropdown = dbc.Row(
    [
        dbc.Label("Node Number", html_for="dropdown_alter", width=2),
        dbc.Col(dcc.Dropdown(
            id='dropdown_alter',
            options=options_dropdown,
        ), width=8),
        dbc.Col(dbc.Button("Update Options", id='update_dropdown_options', n_clicks=0, class_name="button"),width=2)
    ],
    className="mb-3",
)

# Callback-function which is necceassary for updating the selectable options
@callback(
    Output('dropdown_alter', 'options'),
    Input('update_dropdown_options', 'n_clicks')
)
def update_dropdown_options(n):
    data = read_json.load()
    new_options = []
    for i in range(len(data)):
        text = "Node " + str(i)
        new_options.append({"label": text, "value": i})
    return new_options

# creates text field to input a new node text
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

# creates the submit button
insert_button = dbc.Row(
    [
        dbc.Label("Alter the node now", width=2),
        dbc.Col(dbc.Button("Alter", id='submit-val', n_clicks=0, class_name="button"), width=5),
        dbc.Col(html.Div(id='container-alter', children='No node altered untill now'), width=5)
    ]
)

# callback function for submit button
@callback(
    # Output -> in this container the output gets displayed
    Output('container-alter', 'children'),
    Input('submit-val', 'n_clicks'), 
    # State: the function looks in what state these values are and can work with these
    State('node_text', 'value'),
    State('dropdown_alter', 'value'),
    # prevents calling this function when the page is loaded before the submit button was hit
    prevent_inital_call=True
)
def alter_output(n_clicks, n_text, node_nr): # takes the state of the two dropdown menus and alters the JSON-file with them via the alter_text()-function
    if n_clicks > 0:
        data_input.alter_text(node_nr, n_text)
        return "Altered"
    else: 
        pass

# creates a figure for displaying the current graph
fig = display_graph.show_plot()
figure= dbc.Row(dbc.Col(dcc.Graph(figure=fig, id="alter_graph"),width=12))

# button to update the current graph if changes were made
update_button_alter= dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='update_alter', n_clicks=0, class_name="button"), width=5),
    ]
)

# Function for updating the graph if the update-button was hit
@callback(Output('alter_graph', 'figure'), Input('update_alter', 'n_clicks'))
def update_graph_alter(n):
    fig = display_graph.show_plot()
    return fig

# places the elements (dropdown, dropdown und insert-button) in a grid structure
form = dbc.Form([dropdown, node_text, insert_button])
# layout variable combines all dash-components to the displayed layout (heading, dropdowns, insert button, update button and graph)
layout = dbc.Container([html.H1("Alter the node text", className='app-header'), form, update_button_alter, figure], fluid=True)