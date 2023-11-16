import dash
from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import os

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Attack Tree Creator")

app.layout = html.Div([
        html.Div(
            dbc.NavbarSimple(
                children=[
                    dbc.DropdownMenu(children=[html.Div(dbc.DropdownMenuItem(f"{page['name']}", href=page["relative_path"])) for page in dash.page_registry.values()], 
                                     nav=True, 
                                     in_navbar=True, 
                                     label="Actions"),
                    ],
                    brand="Attack Tree Creator",
                    brand_href="/",
                    color="LightBlue", 
                    dark=True,
                ),
                # className= "navbar",
            ),
        html.Br(),
        dash.page_container
    ])

if __name__ == '__main__':
    app.run(debug=False)