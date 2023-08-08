import read_json
import display_graph
import easygui 

if __name__=='__main__':
    filename = easygui.fileopenbox()
    data = read_json.load(filename)

    nr_vertices = len(read_json.create_nodes(data))
    nodes = read_json.create_nodes(data)
    node_types = read_json.get_nodeTypes(data)
    edges = read_json.create_edges(data)

    new_stuff = display_graph.insert_node_types(nr_vertices, node_types, nodes, edges)
    nr_vertices = new_stuff[0]
    nodes = new_stuff[1]
    node_types = new_stuff [2]
    edges = new_stuff[3]

    print(edges)

    display_graph.show_plot(nr_vertices, edges, nodes, node_types)