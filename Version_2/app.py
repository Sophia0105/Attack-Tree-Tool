import dash
from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import easygui

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Attack Tree Modeler")

# def serve_layout():
#     layout = html.Div
#     ([
#         html.H1('Attack Tree Modeler'),
#         html.Div('Actions: '),

#         html.Div(dbc.NavbarSimple(children=[dbc.DropdownMenu(children=[html.Div(dbc.DropdownMenuItem(f"{page['name']}", href=page["relative_path"])) for page in dash.page_registry.values()])])),

#         # html.Div([
#         #     html.Div(
#         #         dcc.Link(f"{page['name']}", href=page["relative_path"])
#         #     ) for page in dash.page_registry.values()
#         # ]),
#         dash.page_container
#     ])
#     return layout

# app.layout = serve_layout()

app.layout = html.Div([
        html.Div(
            dbc.NavbarSimple(
                children=[
                    dbc.DropdownMenu(children=[html.Div(dbc.DropdownMenuItem(f"{page['name']}", href=page["relative_path"])) for page in dash.page_registry.values()], 
                                     nav=True, 
                                     in_navbar=True, 
                                     label="Actions"),
                    ],
                    brand="Attack Tree Modeler",
                    brand_href="/",
                    color="DeepPink", 
                    dark=True,
                )
            ),
        html.Br(),

        # html.Div([
        #     html.Div(
        #         dcc.Link(f"{page['name']}", href=page["relative_path"])
        #     ) for page in dash.page_registry.values()
        # ]),
        dash.page_container
    ])

if __name__ == '__main__':
    filename = easygui.fileopenbox()
    text_file = open("Storage.txt", "w")
    text_file.write(filename)
    text_file.close()
    app.run(debug=False)