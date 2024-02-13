import read_json
import os

def append_node(input_node):
    f_json = read_json.load()
    
    text = input_node[0]
    node_type = input_node[1]
    id = input_node[2]
    parent_node = input_node[4]
    edge_label = input_node[5]
    probability = input_node[6]

    if edge_label == None:
        return "Error: Entered edge weight isn't a number"
    elif probability == None:
        return "Error: Entered probability isn't a number"
    else:
        new_node = {"text_string": text, "node_type": node_type,"id": id, "parentnode": True, "parentnode_number": parent_node, "edge": edge_label, "probability": probability}
        f_json.append(new_node)
        read_json.close_file(f_json)
        return "Inserted node: (id: {}), (text: {}), (type: {}), (parent: {})".format( id , text, "end", str(parent_node))

def alter_text(node_nr, text):
    storage = str(os.getcwd()) + "\Storage.txt"
    file = open(storage, "r")
    filename= file.read()
    file.close()
    f_json = read_json.open_file(filename)
    nr_vertices = len(f_json)
    for i in range(nr_vertices):
        if (f_json[i]["id"] == node_nr):
            f_json[i]["text_string"] = text
            read_json.close_file(f_json)
            return "Successful"
        else: 
            pass

def alter_type(node_nr, n_type):
    storage = str(os.getcwd()) + "\Storage.txt"
    file = open(storage, "r")
    filename= file.read()
    file.close()
    f_json = read_json.open_file(filename)
    nr_vertices = len(f_json)
    for i in range(nr_vertices):
        if (f_json[i]["id"] == node_nr):
            f_json[i]["node_type"] = n_type
            read_json.close_file(f_json)
            return "Successful"
        else: 
            pass

def alter_parent(node_nr, parent_new):
    storage = str(os.getcwd()) + "\Storage.txt"
    file = open(storage, "r")
    filename= file.read()
    file.close()
    if node_nr == 0:
        return "Error: Node 0 has no parent node"
    else:
        f_json = read_json.open_file(filename)
        nr_vertices = len(f_json)
        for i in range(nr_vertices):
            if (f_json[i]["id"] == node_nr):
                f_json[i]["parentnode_number"] = parent_new
                read_json.close_file(f_json)
                return "Successful"
            else: 
                pass

def delete_node(node_nr):
    if node_nr == 0:
        return "Error: Node 0 can not be deleted"
    else:
        f_json = read_json.load()
        nr_vertices = len(f_json)
        data = change_parentnodes(f_json,node_nr)
        for i in range(nr_vertices):
            if (data[i]["id"] == node_nr):
                delete_node = data.pop(i)
                data = read_json.correct_ids(data)
                read_json.close_file(data)
                correct_node_types()
                return "node deleted -- last one: (id: {}), (text: {}), (type: {}), (parent: {})".format(str(delete_node["id"]), delete_node["text_string"], delete_node["node_type"], str(delete_node["parentnode_number"]))
            else: 
                pass
        return {'text_string': 'None', 'node_type': 'None', 'id': 'None', 'parentnode': 'None', 'parentnode_number': 'None'}

def correct_node_types():
    error = False
    f_json = read_json.load()
    nr_vertices = len(f_json)
    parent_nodes = []

    for i in range(nr_vertices):
        if i > 0:
            parent_nodes.append(f_json[i]["parentnode_number"])

    for i in range(nr_vertices): 
        if (f_json[i]["node_type"] == "and") and parent_nodes.count(i) < 2:
            f_json[i]["node_type"] = "end"
            error = True
        if (f_json[i]["node_type"] == "or") and parent_nodes.count(i) < 2:
            f_json[i]["node_type"] = "end"
            error = True
        if f_json[i]["node_type"] == "end" and parent_nodes.count(i) >= 2:
            f_json[i]["node_type"] = "or"
            error = True
    read_json.close_file(f_json)
    return error

def add_br_to_text():
    max_length = 20
    f_json = read_json.load()
    nr_vertices = len(f_json)
    for i in range(nr_vertices):
            old = f_json[i]["text_string"]
            new = add_br(old, max_length)
            f_json[i]["text_string"] = new
    read_json.close_file(f_json)

def add_br(input_line, max_length):
    if "<br>" in input_line: 
        return input_line
    else:
        lines = []
        cur_line = ''
        long_line = ''
        splited = input_line.split()
        for word in splited:
            if len(cur_line) + len(word) > max_length:
                lines.append(cur_line)
                long_line += "<br>" + word
                cur_line = word
            else:
                cur_line += " " + word
                long_line += " " + word
        return long_line
    
def alter_edge(node_nr, edge_new):
    if edge_new == None:
        return "Error: Entered edge weight isn't a number"
    else:
        f_json = read_json.load()
        nr_vertices = len(f_json)
        for i in range(nr_vertices):
            if (f_json[i]["id"] == node_nr):
                f_json[i]["edge"] = edge_new
                read_json.close_file(f_json)
                return "Successful"
            else: 
                pass

def alter_probability(node_nr, p_new):
    if p_new == None:
        return "Error: Entered probability isn't a number"
    else:
        f_json = read_json.load()
        nr_vertices = len(f_json)
        for i in range(nr_vertices):
            if (f_json[i]["id"] == node_nr):
                f_json[i]["probability"] = p_new
                read_json.close_file(f_json)
                return "Successful"
            else: 
                pass

def change_parentnodes(data, delete_id):
    new_data = data
    for j in data:
        if j["id"] == delete_id:
            parentnode = j["parentnode_number"]
    counter = 0
    for i in data: 
        if i["parentnode"] == True:
            if i["parentnode_number"] == delete_id:
                new_data[counter]["parentnode_number"] = parentnode
        if i["id"] == parentnode:
            new_data[counter]["node_type"] = "end"
        counter += 1
    return new_data