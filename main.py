import read_json
import display_graph
import easygui 
import dash_input
import data_input

if __name__=='__main__':
    filename=easygui.fileopenbox()
    data = read_json.load(filename)

    nr_vertices = len(read_json.create_nodes(data))
    nodes = read_json.create_nodes(data)
    node_types = read_json.get_nodeTypes(data)
    edges = read_json.create_edges(data)

    option = input("What do you want to do? \n1 look at existing attack tree \n2 insert new node\n")
    if int(option) == 1:
        # open attack tree
        new_stuff = display_graph.insert_node_types(nr_vertices, node_types, nodes, edges)
        nr_vertices = new_stuff[0]
        nodes = new_stuff[1]
        node_types = new_stuff [2]
        edges = new_stuff[3]

        display_graph.show_plot(nr_vertices, edges, nodes, node_types)


    elif int(option) == 2: 
        #insert new node
        full_info = []
        for i in range(nr_vertices):
            full_info.append(str(i) +  ": " +nodes[i])

        new_stuff = display_graph.insert_node_types(nr_vertices, node_types, full_info, edges)
        nr_vertices_old = nr_vertices
        nr_vertices = new_stuff[0]
        nodes = new_stuff[1]
        node_types = new_stuff [2]
        edges = new_stuff[3]

        dash_input.append_node(filename, nr_vertices, edges, nodes, node_types, nr_vertices_old)

    else: 
        print("Invalid Input")