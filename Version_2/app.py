import dash
from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import easygui

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

def serve_layout():
    layout = html.Div([
        html.H1('Attack Tree Modeler'),
        html.Div('Actions: '),
        html.Div([
            html.Div(
                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
            ) for page in dash.page_registry.values()
        ]),
        dash.page_container
    ])
    return layout

app.layout = serve_layout

if __name__ == '__main__':
    filename = easygui.fileopenbox()
    text_file = open("Storage.txt", "w")
    text_file.write(filename)
    text_file.close()
    app.run(debug=True)