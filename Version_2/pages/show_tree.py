import dash
import read_json
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import easygui


dash.register_page(__name__, path='/')

def layout():
    file = open('D:\TH\Bachelorarbeit\Attack Tree Modellierer\Version_2\Storage.txt', 'r')
    filename= file.read()
    
    fig = display_graph.show_plot(filename)
    figure= html.Div([dbc.Row(dbc.Col(dcc.Graph(id='live_graph', figure=fig),width=12)),dcc.Interval(id='interval_component', interval = 1*1000, n_intervals=0)])

    @callback(Output('live_graph', 'figure'), Input('interval_component', 'n_intervals'))
    def update_graph_live(n):
        fig = display_graph.show_plot(filename)
        return fig

    layout = dbc.Container([html.H1('Current Attack Tree'), figure], fluid=True)
    return layout