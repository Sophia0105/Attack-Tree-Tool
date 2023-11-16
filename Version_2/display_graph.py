import igraph as ig
import plotly.graph_objects as go
import read_json
import data_input


def show_plot():
    data_input.add_br_to_text()
    data_input.correct_node_types()
    data = read_json.load()
    nr_vertices = len(read_json.create_nodes(data))
    nodes = read_json.create_nodes(data)
    node_types = read_json.get_node_types(data)
    edges = read_json.create_edges(data)

    full_info = []
    for i in range(nr_vertices):
        full_info.append(str(i) +  ": " +nodes[i])

    new_stuff = read_json.insert_node_types(nr_vertices, node_types, full_info, edges)
    nr_vertices = new_stuff[0]
    nodes = new_stuff[1]
    node_types = new_stuff [2]
    edges = new_stuff[3]

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

    edge_labels = read_json.get_edge_labels()
    # x- and y- position of the edges
    Xe = []
    Ye = []
    counter = 0
    for edge in E: 
        Xe+= [position[edge[0]][0], position[edge[1]][0], None]
        Ye+= [2*M-position[edge[0]][1], 2*M-position[edge[1]][1], None]
        counter += 1
    

    Xel = []
    Yel = []
    p = 0
    for i in range(len(edges)):
        if node_types[i] == "end":
            x = Xe[p] + Xe[p+1]
            x = x / 2 
            Xel.append(x)
            y = Ye[p] + Ye[p+1]
            y = y / 2
            Yel.append(y)
            p += 3 

    new_nodes = []
    Xnn = []
    Ynn = []
    helpers = []
    Xhn = []
    Yhn = []
    for i in range(nr_vertices):
        if node_types[i] == "helper":
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
                   line=dict(color='rgb(210,210,210)', width=5),
                   hoverinfo='none'
                   ))
    
    for i in range(len(Xel)):
        if node_types[i] != "helper":
            fig.add_annotation(x = Xel[i], y = Yel[i], text = edge_labels[i], showarrow= False)

    for i in range(len(nodes)):
        fig.add_annotation(x=Xn[i], y= Yn[i], text = nodes[i], showarrow=False, bgcolor="#6175c1", font=dict(color="#ffffff"))
    
    # Shows full nodes
    fig.add_trace(go.Scatter(x=Xnn,
                  y=Ynn,
                  mode='markers',
                  marker=dict(symbol="square",
                                size=10,
                                color='#6175c1',    #'#DB4551',
                                ),
                  # text=nodes,
                  hoverinfo='none'
                  ))
    
    # Show helper nodes
    fig.add_trace(go.Scatter(x=Xhn,
                  y=Yhn,
                  mode='markers',
                  marker=dict(symbol="circle",
                                size=50,
                                color="#6175c1",    #'#DB4551',
                                ),
                  # text=nodes,
                  hoverinfo='none'
                  ))

    
    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )

    fig.update_layout(# annotations= read_json.make_annotations(position, nodes, nodes, M, position),
                      height= 1000,
                      font_size=14,
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      plot_bgcolor='rgb(248,248,248)'
                      )
    return fig


