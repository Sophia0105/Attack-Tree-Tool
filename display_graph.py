import igraph as ig
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, dcc, html

def insert_node_types(nr_vertices, nodeTypes, nodes, edges):
    new_edges = edges
    number_of_nodes = nr_vertices
    counter = 0
    for i in nodeTypes:
        if i=="and":
            counter_2 = 0
            for j in new_edges: 
                if j[0] == counter:
                    second = j[1]
                    new_edges[counter_2] = (number_of_nodes, second)
                counter_2 += 1
            nodes.append("and")
            nodeTypes.append("helper")
            new_edges.append((counter, number_of_nodes))
            number_of_nodes += 1
        elif i=="or":
            counter_2 = 0
            for j in new_edges: 
                if j[0] == counter:
                    second = j[1]
                    new_edges[counter_2] = (number_of_nodes, second)
                counter_2 += 1
            nodes.append("or")
            nodeTypes.append("helper")
            new_edges.append((counter, number_of_nodes))
            number_of_nodes += 1
        else: 
            pass
        counter += 1
    return [number_of_nodes, nodes, nodeTypes, new_edges]

def o_show_plot(nr_vertices, edges, nodes, nodeTypes):
    g = ig.Graph(nr_vertices, edges)

    g.vs["text_string"] = nodes
    g.vs["node_type"] = nodeTypes

    fig, ax = plt.subplots(figsize = (300, 300))
    ig.plot(
        g,
        target=ax,
        layout= g.layout("rt", root=[0]),
        vertex_size=[0.3 if node_type == "or_helper" or node_type == "and_helper" else 0.9 for node_type in g.vs["node_type"]],
        vertex_color=["pink" if node_type == "or" or node_type == "or_helper" else "hotpink" if node_type == "and" or node_type == "and_helper" else "mediumvioletred" for node_type in g.vs["node_type"]],
        vertex_label=g.vs["text_string"],
        vertex_label_size= 5,
        vertex_shape = ["circle" if node_type == "and_helper" or node_type == "or_helper" else "rectangle" for node_type in g.vs["node_type"]],
        bbox = (1024,1024)
    )

def make_annotations(pos, text, labels, M, position, font_size=10, font_color='rgb(250,250,250)'):
    L=len(pos)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                text=labels[k], # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2*M-position[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations
    
def show_plot(nr_vertices, edges, nodes, nodeTypes):
    G = ig.Graph(nr_vertices, edges)
    lay = G.layout('rt', root=[0])

    position = {k:lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = ig.EdgeSeq(G)
    E = [e.tuple for e in G.es]

    L = len(position)

    # x- and y- position of the nodes
    Xn = [position[k][0] for k in range(L)]
    Yn = [2*M-position[k][1] for k in range(L)]

    # x- and y- position of the edges
    Xe = []
    Ye = []
    for edge in E: 
        Xe+= [position[edge[0]][0], position[edge[1]][0], None]
        Ye+= [2*M-position[edge[0]][1], 2*M-position[edge[1]][1], None]

    labels = nodes

    new_nodes = []
    Xnn = []
    Ynn = []
    helpers = []
    Xhn = []
    Yhn = []
    for i in range(nr_vertices):
        if nodeTypes[i] == "helper":
            helpers.append(nodes[i])
            Xhn.append(Xn[i])
            Yhn.append(Yn[i])
        else:
            new_nodes.append(nodes[i])
            Xnn.append(Xn[i])
            Ynn.append(Yn[i])
    

    fig = go.Figure()

    # Shows all edges
    fig.add_trace(go.Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line=dict(color='rgb(210,210,210)', width=1),
                   hoverinfo='none'
                   ))
    
    # Shows full nodes
    fig.add_trace(go.Scatter(x=Xnn,
                  y=Ynn,
                  mode='markers',
                  marker=dict(symbol="square",
                                size=70,
                                color='#6175c1',    #'#DB4551',
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  text=labels,
                  hoverinfo='text',
                  # opacity=0.8
                  ))
    
    # Show helper nodes
    fig.add_trace(go.Scatter(x=Xhn,
                  y=Yhn,
                  mode='markers',
                  marker=dict(symbol="circle",
                                size=15,
                                color='#6175c1',    #'#DB4551',
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  text=labels,
                  # opacity=0.8
                  ))

    
    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )

    fig.update_layout(title= 'Example Attack Tree',
              annotations=make_annotations(position, nodes, nodes, M, position),
              font_size=12,
              showlegend=False,
              xaxis=axis,
              yaxis=axis,
              margin=dict(l=40, r=40, b=85, t=100),
              hovermode='closest',
              plot_bgcolor='rgb(248,248,248)'
              )
    fig.show()

    app = Dash()
    app.layout = html.Div([dcc.Graph(figure=fig)])
    app.run_server(debug=True, use_reloader=False)


