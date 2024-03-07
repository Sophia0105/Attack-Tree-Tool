import dash
import read_json
import data_input
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

# Register page to the dash app, set path to reach the side and the name which will be displayed
dash.register_page(__name__, path='/alter_parent', name='Alter Parent Node')

# Load and set data which has to be processed
data = read_json.load()
nr_vertices = len(read_json.create_nodes(data))
last_node = data[-1]
id = last_node["id"] + 1

# Creates list of options for the dropdown menu to select a node (for selecting a child node, therefore wihtout node 0)
options_dropdown = []
for i in range(nr_vertices):
    if i > 0:
        text = "Node " + str(i)
        options_dropdown.append({"label": text, "value": i})

# Drop-down menu for selecting a node number and the attached button for updating the selectable options
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

# Callback-function which is necceassary for updating the selectable options
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

# Creates dropdown-menu options for choosing a parent node -> new list neccesary with root node 0)
options_dropdown_p = []
for i in range(nr_vertices):
    text = "Node " + str(i)
    options_dropdown.append({"label": text, "value": i})

# Displays the dropdown-menu for selecting a new parent node including a button to update the options
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

# callback-function for updating the options of the second dropdown-menu
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

# creates the submit button
insert_button = dbc.Row(
    [
        dbc.Label("Alter the node now", width=2),
        dbc.Col(dbc.Button("Alter", id='submit-parent', n_clicks=0, class_name="button"), width=5),
        dbc.Col(html.Div(id='container-alter-parent', children='No node altered untill now'), width=5)
    ]
)

# callback function for submit button
@callback(
    # Output -> in this container the output gets displayed
    Output('container-alter-parent', 'children'),
    Input('submit-parent', 'n_clicks'), 
    # State: the function looks in what state these values are and can work with these
    State('dropdown_parent', 'value'),
    State('dropdown_nr', 'value'),
    # prevents calling this function when the page is loaded before the submit button was hit
    prevent_inital_call=True
)
def alter_output(n_clicks, n_parent, node_nr):  # takes the state of the two dropdown menus and alters the JSON-file with them via the alter_parent()-function
    if n_clicks > 0:
        alteration = data_input.alter_parent(node_nr, n_parent)
        data_input.correct_node_types()
        return alteration
    else: 
        pass

# creates a figure for displaying the current graph
fig = display_graph.show_plot()
figi= dbc.Row(dbc.Col(dcc.Graph(figure=fig, id="alter_parent_graph"),width=12))

# button to update the current graph if changes were made
update_button_type= dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='update-parent', n_clicks=0, class_name="button"), width=5),
    ]
)

# Function for updating the graph if the update-button was hit
@callback(Output('alter_parent_graph', 'figure'), Input('update-parent', 'n_clicks'))
def update_graph_alter(n):
    fig = display_graph.show_plot()
    return fig

# places the elements (dropdown, dropdown und insert-button) in a grid structure
form = dbc.Form([dropdown, dropdown_parent, insert_button])
# layout variable combines all dash-components to the displayed layout (heading, dropdowns, insert button, update button and graph)
layout = dbc.Container([html.H1("Alter the parent node", className='app-header'), form, update_button_type, figi], fluid=True)