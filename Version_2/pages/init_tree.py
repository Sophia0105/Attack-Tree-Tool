import dash
import os
import read_json
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import easygui


dash.register_page(__name__, path='/')

filename_input = dbc.Row(
    [
        dbc.Label("Determine a name for the file where the tree ist stored", html_for="filename_input", width=2),
        dbc.Col(dbc.Input(
            id="filename_input", 
            placeholder="Enter the name for the new file",
            ), width=10),
    ],
)

nodetext_input = dbc.Row(
    [
        dbc.Label("Put in the text for the first node of the new tree", html_for="nodetext_input", width=2),
        dbc.Col(dbc.Input(
            id="nodetext_input", 
            placeholder='Node Text, e.g. "open safe"',
            ), width=10),
    ],
)

update_button = dbc.Row(
    [
        dbc.Label("Start new tree", width=2),
        dbc.Col(dbc.Button("Init file", id='submit-name', n_clicks=0, class_name="button"), width=5),
        dbc.Col(html.Div(id='filename', children='No file yet'), width=5)
    ]
)

@callback(
        Output('filename', 'children'), 
        Input('submit-name', 'n_clicks'),
        State('filename_input', 'value'),
        State('nodetext_input', 'value'),
        prevent_inital_call=True
    )
def update_graph_live(n, value1, value2):
    if n > 0:
        filename = str(os.getcwd())+ "\\trees\\" + value1 + ".json"
        first_node = [{'text_string': value2, 'node_type': 'end', 'id': 0, 'parentnode': False}]
        read_json.close_file(first_node)
        storage = str(os.getcwd()) + "\Storage.txt"
        text_file = open(storage, "w")
        text_file.write(filename)
        text_file.close()
        return filename
    else:
        pass
    
form1 = dbc.Form([filename_input, nodetext_input, update_button])

storage = str(os.getcwd()) + "\Storage.txt"
file = open(storage, "r")
filename= file.read()
file.close()
file_string = "Currrently opened file is: " + str(filename)

select_button = dbc.Row(
    [
        dbc.Label("Open existing file", width=2),
        dbc.Col(dbc.Button("Select", id='select-name', n_clicks=0, class_name="button"), width=5),
        dbc.Col(html.Div(id='fileselector', children=file_string), width=5)
    ]
)

@callback(
    Output('fileselector', 'children'),
    Input('select-name', 'n_clicks'),
    prevent_inital_call=True
)
def open_file_dialog(n):
    if n > 0:
        path = str(os.getcwd()) + "\\trees\\*.json"
        new_filename = easygui.fileopenbox(filetypes=["*.json"], default=path)
        storage = str(os.getcwd()) + "\Storage.txt"
        if new_filename != None:
            text_file = open(storage, "w")
            text_file.write(new_filename)
            text_file.close()
            return "Currrently opened file is: " + str(new_filename)
        else:
            return "Error: No file choosen"
    else:
        storage = str(os.getcwd()) + "\Storage.txt"
        file = open(storage, "r")
        filename= file.read()
        file.close()
        return "Currrently opened file is: " + str(filename)

form2 = dbc.Form([select_button])
# form2 = html.Div("Here should be the file selector")

layout = dbc.Container([html.H1('Welcome', className='app-header'), html.H2('Initialize new tree'),form1, html.Br(), html.Br(), html.H2('Open existing tree'), form2], fluid=True)