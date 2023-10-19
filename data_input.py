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

def delete_node(filename, nr_vertices, node_nr):
    f_json = read_json.open_file(filename)
    delete_node = "None"
    for i in range(nr_vertices):
        print(str(f_json[i]["id"]))
        if f_json[i]["id"] == node_nr:
            deleted_node = f_json.pop(i)
        else: 
            pass
    read_json.close_file(filename, f_json)
    return delete_node