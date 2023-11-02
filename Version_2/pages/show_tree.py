import dash
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/')


file = open('D:\TH\Bachelorarbeit\Attack Tree Modellierer\Version_2\Storage.txt', 'r')
filename= file.read()

fig = display_graph.show_plot(filename)
# figure= html.Div([dbc.Row(dbc.Col(dcc.Graph(id='live_graph', figure=fig),width=12))])

update_button = dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='submit-val', n_clicks=0), width=5),
        # dbc.Col(html.Div(id='container-button-basic', children='No node inserted untill now'), width=5)
        html.Div([dbc.Row(dbc.Col(dcc.Graph(id='live_graph', figure=fig),width=12))])
    ]
)

@callback(Output('live_graph', 'figure'), Input('submit-val', 'n_clicks'))
def update_graph_live(n):
    fig = display_graph.show_plot(filename)
    return fig

layout = dbc.Container([html.H1('Current Attack Tree', className='app-header')], fluid=True)
