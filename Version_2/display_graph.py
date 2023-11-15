import igraph as ig
import plotly.graph_objects as go
import read_json
import data_input

def insert_node_types(nr_vertices, node_types, nodes, edges):
    new_edges = edges
    number_of_nodes = nr_vertices
    counter = 0
    for i in node_types:
        if i=="and":
            counter_2 = 0
            for j in new_edges: 
                if j[0] == counter:
                    second = j[1]
                    new_edges[counter_2] = (number_of_nodes, second)
                counter_2 += 1
            nodes.append("and")
            node_types.append("helper")
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
            node_types.append("helper")
            new_edges.append((counter, number_of_nodes))
            number_of_nodes += 1
        else: 
            pass
        counter += 1
    return [number_of_nodes, nodes, node_types, new_edges]

def make_annotations(pos, text, labels, M, position, font_size=14, font_color='rgb(250,250,250)'):
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
                bgcolor = "#6175c1",
                showarrow=False)
        )
    return annotations
    
def show_plot(filename):
    data_input.correct_node_types(filename)
    data = read_json.load(filename)
    nr_vertices = len(read_json.create_nodes(data))
    nodes = read_json.create_nodes(data)
    node_types = read_json.get_node_types(data)
    edges = read_json.create_edges(data)

    full_info = []
    for i in range(nr_vertices):
        full_info.append(str(i) +  ": " +nodes[i])

    new_stuff = insert_node_types(nr_vertices, node_types, full_info, edges)
    nr_vertices_old = nr_vertices
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
    
    # Shows full nodes
    fig.add_trace(go.Scatter(x=Xnn,
                  y=Ynn,
                  mode='markers',
                  marker=dict(symbol="square",
                                size=10,
                                color='#6175c1',    #'#DB4551',
                                ),
                  text=labels,
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
                  text=labels,
                  hoverinfo='none'
                  ))

    
    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )

    fig.update_layout(annotations=make_annotations(position, nodes, nodes, M, position),
                      height= 1000,
                      font_size=14,
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      plot_bgcolor='rgb(248,248,248)'
                      )
    return fig


