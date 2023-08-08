import igraph as ig
import matplotlib.pyplot as plt

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
            nodeTypes.append("and_helper")
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
            nodeTypes.append("or_helper")
            new_edges.append((counter, number_of_nodes))
            number_of_nodes += 1
        else: 
            pass
        counter += 1
    return [number_of_nodes, nodes, nodeTypes, new_edges]

def show_plot(nr_vertices, edges, nodes, nodeTypes):
    g = ig.Graph(nr_vertices, edges)

    g.vs["text_string"] = nodes
    g.vs["node_type"] = nodeTypes

    fig, ax = plt.subplots(figsize = (100, 300))
    ig.plot(
        g,
        target=ax,
        layout= g.layout_reingold_tilford(root=[0]),
        vertex_size=[0.3 if node_type == "or_helper" or node_type == "and_helper" else 0.9 for node_type in g.vs["node_type"]],
        vertex_color=["pink" if node_type == "or" or node_type == "or_helper" else "hotpink" if node_type == "and" or node_type == "and_helper" else "mediumvioletred" for node_type in g.vs["node_type"]],
        vertex_label=g.vs["text_string"],
        vertex_label_size= 5,
        vertex_shape = ["circle" if node_type == "and_helper" or node_type == "or_helper" else "rectangle" for node_type in g.vs["node_type"]],
        bbox = (1024,1024)
    )
    plt.show()