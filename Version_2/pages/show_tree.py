import dash
import display_graph
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/show_tree')

fig = display_graph.show_plot()
# figure= html.Div([dbc.Row(dbc.Col(dcc.Graph(id='live_graph', figure=fig),width=12))])

update_button = dbc.Row(
    [
        dbc.Label("Update graph", width=2),
        dbc.Col(dbc.Button("Update Graph", id='submit-val', n_clicks=0, class_name="button"), width=5),
        # dbc.Col(html.Div(id='container-button-basic', children='No node inserted untill now'), width=5)
    ]
)

@callback(Output('live_graph', 'figure'), Input('submit-val', 'n_clicks'))
def update_graph_live(n):
    fig = display_graph.show_plot()
    return fig

figi = html.Div([dbc.Row(dbc.Col(dcc.Graph(id='live_graph', figure=fig),width=12))])

layout = dbc.Container([html.H1('Current Attack Tree', className='app-header'), update_button, figi], fluid=True)
