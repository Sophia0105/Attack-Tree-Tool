import read_json

def append_node(filename, input_node):
    f_json = read_json.open_file(filename)
    
    text = input_node[0]
    node_type = input_node[1]
    id = input_node[2]
    parent_node = input_node[4]

    new_node = {"text_string": text, "node_type": node_type,"id": id, "parentnode": True, "parentnode_number": parent_node}
    f_json.append(new_node)
    read_json.close_file(filename, f_json)
    correct_node_types(filename)

def alter_text(filename, node_nr, text, nr_vertices):
    f_json = read_json.open_file(filename)
    for i in range(nr_vertices):
        if (f_json[i]["id"] == node_nr):
            f_json[i]["text_string"] = text
            read_json.close_file(filename, f_json)
            return delete_node
        else: 
            pass

def alter_type(filename, node_nr, n_type, nr_vertices):
    f_json = read_json.open_file(filename)
    for i in range(nr_vertices):
        if (f_json[i]["id"] == node_nr):
            f_json[i]["node_type"] = n_type
            read_json.close_file(filename, f_json)
            return delete_node
        else: 
            pass

def alter_parent(filename, node_nr, parent_new, nr_vertices):
    if node_nr == 0:
        return "Error: Node 0 has no parent node"
    else:
        f_json = read_json.open_file(filename)
        for i in range(nr_vertices):
            if (f_json[i]["id"] == node_nr):
                f_json[i]["parentnode_number"] = parent_new
                read_json.close_file(filename, f_json)
                return delete_node
            else: 
                pass

def delete_node(filename, nr_vertices, node_nr):
    if node_nr == 0:
        return "Error: Node 0 can not be deleted"
    else:
        f_json = read_json.open_file(filename)
        delete_node = "None"
        for i in range(nr_vertices):
            if (f_json[i]["id"] == node_nr):
                delete_node = f_json.pop(i)
                read_json.close_file(filename, f_json)
                correct_node_types(filename)
                return delete_node
            else: 
                pass
        return {'text_string': 'None', 'node_type': 'None', 'id': 'None', 'parentnode': 'None', 'parentnode_number': 'None'}

def correct_node_types(filename):
    error = False
    f_json = read_json.open_file(filename)
    nr_vertices = f_json[-1]["id"]
    parent_nodes = []
    for i in range(nr_vertices):
        parent_nodes.append(f_json[i]["parentnode_number"])
    for i in range(nr_vertices): 
        if (f_json[i]["node_type"] == "and") and i not in parent_nodes:
            f_json[i]["node_type"] = "end"
            error = True
        if (f_json[i]["node_type"] == "or") and i not in parent_nodes:
            f_json[i]["node_type"] = "end"
            error = True
        if f_json[i]["node_type"] == "end" and parent_nodes.count(i) >= 2:
            f_json[i]["node_type"] = "or"
            error = True
    read_json.close_file(filename, f_json)
    return error
        