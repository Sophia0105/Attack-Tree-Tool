import dash
import os
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/')

filename_input = dbc.Row(
    [
        dbc.Label("Node Text", html_for="filename_input", width=2),
        dbc.Col(dbc.Input(
            id="filename_input", 
            placeholder="Enter the name for the new file",
            ), width=10),
    ],
)

update_button = dbc.Row(
    [
        dbc.Label("Start new tree", width=2),
        dbc.Col(dbc.Button("Init file", id='submit-name', n_clicks=0), width=5),
        dbc.Col(html.Div(id='filename', children='No file yet'), width=5)
    ]
)

@callback(
        Output('filename', 'children'), 
        Input('submit-name', 'n_clicks'),
        State('filename_input', 'value'),
        prevent_inital_call=True
    )
def update_graph_live(n, value):
    if n > 0:
        filename = str(os.getcwd())+ "\\" + value + ".json"
        text_file = open(filename, "w")
        text_file.write('["test"]')
        text_file.close()
        text_file = open("Storage.txt", "w")
        text_file.write(filename)
        text_file.close()
        return filename
    else:
        pass
    
form = dbc.Form([filename_input, update_button])
layout = dbc.Container([html.H1('Welcome', className='app-header'), form], fluid=True)