import json

def open_file(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data
 
def close_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def correct_ids(data):
    new_data = data
    counter = 0
    for i in data:
        if i["id"] != counter:
            false_id = i["id"]
            counter2 = 0
            for j in data: 
                if j["parentnode"] == True:
                    if j["parentnode_number"] == false_id:
                        new_data[counter2]["parentnode_number"] = counter
                counter2 += 1
            new_data[counter]["id"] = counter
        counter += 1
    return new_data


def create_nodes(data):
    text = []
    for i in data: 
        text.append(i["text_string"])
    return text

def create_edges(data):
    edges = []
    for i in data:
        if i["parentnode"]==True:
            edge= (i["parentnode_number"], i["id"])
            edges.append(edge)
    return edges

def get_node_types(data):
    node_types = []
    for i in data:
        node_types.append(i["node_type"])
    return node_types

def load(filename):
    data = open_file(filename)
    updated = correct_ids(data)
    close_file(filename, updated)
    return updated