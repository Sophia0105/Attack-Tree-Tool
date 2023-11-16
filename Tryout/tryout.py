import igraph as ig
import plotly.graph_objects as go

def show_plot():
    nodes = ["test1", "test2", "test3", "test4", "test5"]
    edge_labels = ["0.5", "0.33", "0.45", "0.87"]
    edges = [(0,1), (2,0), (1,3), (4,1)]
    nr_vertices = len(nodes)

    
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

    print("Xe: " + str(Xe))
    print("Ye: " + str(Ye))

    Xel = []
    Yel = []
    p = 0
    for i in range(len(edges)):
        x = Xe[p] + Xe[p+1]
        x = x / 2 
        Xel.append(x)
        y = Ye[p] + Ye[p+1]
        y = y / 2
        Yel.append(y)
        p += 3 


    fig = go.Figure()

    # Shows all edges
    fig.add_trace(go.Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line=dict(color='rgb(210,210,210)', width=5)
                   ))
    
    for i in range(len(edges)):
        fig.add_annotation(x = Xel[i], y = Yel[i], text = edge_labels[i], showarrow= False)
    
    # Shows full nodes
    fig.add_trace(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers+text',
                  marker=dict(symbol="square",
                                size=10,
                                color='#6175c1',    #'#DB4551',
                                ),
                  text=nodes,
                  textposition= "top center",
                  hoverinfo='none'
                  ))


    
    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )
    
    fig.update_layout(height= 1000,
                      font_size=14,
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      plot_bgcolor='rgb(248,248,248)'
                      )
    
    return fig
