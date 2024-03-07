import read_json

def evaluate_tree_backup():
    data = read_json.load()
    edge_labels = read_json.get_edge_labels()
    parent_nodes = read_json.get_parents()
    nr_vertices = len(read_json.create_nodes(data))

    graph = {}
    for i in range(nr_vertices): 
        children = []
        for j in range(len(parent_nodes)):
            if i == parent_nodes[j] and edge_labels[j] == 'P':
                children.append(j+1)
        
        graph[i] = children

    edges = []
    for key in graph:
        children = graph[key]
        valid_children = []
        for i in children: 
            if i in parent_nodes and len(graph[i]) > 0:
                valid_children.append(i)
                edges.append((key,i))
            elif i not in parent_nodes:
                valid_children.append(i)
                edges.append((key,i))
        graph[key] = valid_children


    return edges


def evaluate_tree():
    data = read_json.load()
    edge_labels = read_json.get_edge_labels()
    parent_nodes = read_json.get_parents()
    node_types = read_json.get_node_types(data)
    nr_vertices = len(read_json.create_nodes(data))

    graph = {}
    all_graph = {}
    for i in range(nr_vertices): 
        children = []
        all_children = []
        for j in range(len(parent_nodes)):
            if i == parent_nodes[j]:
                all_children.append(j+1)
            if i == parent_nodes[j] and edge_labels[j] == 'P':
                children.append(j+1)
        graph[i] = children
        all_graph[i] = all_children

    edges = []
    for key in graph:
        children = graph[key]
        all_children = all_graph[key]
        valid_children = []
        if node_types[key] == 'and':
            evals = []
            for i in all_children:
                evals.append(edge_labels[i-1])
            if 'I' in evals:
                if (parent_nodes[parent_nodes[i-1]], parent_nodes[i-1]) in edges:
                    edges.remove((parent_nodes[parent_nodes[i-1]], parent_nodes[i-1]))
                elif (parent_nodes[i-1],parent_nodes[parent_nodes[i-1]]) in edges:
                    edges.remove((parent_nodes[i-1],parent_nodes[parent_nodes[i-1]]))
                graph[parent_nodes[i-1]] = []
            else:
                for i in children: 
                    if i in parent_nodes and len(graph[i]) > 0:
                        valid_children.append(i)
                        edges.append((key,i))
                    elif i not in parent_nodes:
                        valid_children.append(i)
                        edges.append((key,i))
        else:        
            for i in children: 
                if i in parent_nodes and len(graph[i]) > 0:
                    valid_children.append(i)
                    edges.append((key,i))
                elif i not in parent_nodes:
                    valid_children.append(i)
                    edges.append((key,i))
        graph[key] = valid_children


    return edges

def get_branch_label():
    data = read_json.load()
    node_types = read_json.get_node_types(data)
    edge_labels = read_json.get_edge_labels()
    parent_nodes = read_json.get_parents()
    nr_vertices = len(read_json.create_nodes(data))

    n_dict = {}

    graph = {}
    for i in range(nr_vertices): 
        children = []
        for j in range(len(parent_nodes)):
            if i == parent_nodes[j]:
                children.append(j+1)
        graph[i] = children

    counter = nr_vertices   

    for key in graph:
        children = graph[key]
        evals = []
        for i in children:
            evals.append(edge_labels[i-1])
        if node_types[key] == 'and':
            k = (key, counter)
            counter += 1
            if 'I' in evals:
                n_dict[k] = 'I'
            else:
                n_dict[k] = 'P'
        if node_types[key] == 'or':
            k = (key, counter)
            counter += 1
            if 'P' in evals:
                n_dict[k] = 'P'
            else:
                n_dict[k] = 'I'

    return n_dict
