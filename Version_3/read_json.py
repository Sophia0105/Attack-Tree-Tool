import json
import os

def open_file(filename):
    file = open(filename)
    data = json.load(file)
    file.close()
    return data
 
def close_file(data):
    storage = str(os.getcwd()) + "\Storage.txt"
    file = open(storage, "r")
    filename= file.read()
    file.close()
    f_json = open(filename, "w")
    json.dump(data, f_json, indent=4)
    f_json.close()

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

def load():
    storage = str(os.getcwd()) + "\Storage.txt"
    file = open(storage, "r")
    filename= file.read()
    file.close()
    data = open_file(filename)
    updated = correct_ids(data)
    updated = data
    close_file(updated)
    return updated

def insert_node_types(nr_vertices, node_types, nodes, edges, valid_edges):
    new_edges = edges
    new_valid_edges = []
    number_of_nodes = nr_vertices
    counter = 0
    for i in node_types:
        counter3 = False
        if i=="and":
            counter_2 = 0
            for j in new_edges: 
                if j[0] == counter:
                    second = j[1]
                    new_edges[counter_2] = (number_of_nodes, second)
                    if j in valid_edges:
                        new_valid_edges.append((number_of_nodes,second))
                        counter3 = True
                counter_2 += 1
            nodes.append("and")
            node_types.append("helper")
            new_edges.append((counter, number_of_nodes))
            if counter3 == True:
                new_valid_edges.append((counter, number_of_nodes))
                counter3 = False
            number_of_nodes += 1
        elif i=="or":
            counter_2 = 0
            for j in new_edges: 
                if j[0] == counter:
                    second = j[1]
                    new_edges[counter_2] = (number_of_nodes, second)
                    if j in valid_edges:
                        new_valid_edges.append((number_of_nodes,second))
                        counter3 = True
                counter_2 += 1
            nodes.append("or")
            node_types.append("helper")
            new_edges.append((counter, number_of_nodes))
            if counter3 == True:
                new_valid_edges.append((counter, number_of_nodes))
                counter3 = False
            number_of_nodes += 1
        else: 
            pass
        counter += 1
    return [number_of_nodes, nodes, node_types, new_edges, new_valid_edges]

def get_edge_labels():
    data = load()
    edge_labels = []
    for i in range(len(data)):
        if data[i]["parentnode"] == True:
            edge_labels.append(data[i]["edge"])
    return edge_labels

def get_probabilities():
    data = load()
    labels = []
    for i in range(len(data)):
        labels.append(data[i]["probability"])
    return labels

def get_parents():
    data = load()
    parents = []
    for i in range(len(data)):
        if data[i]["parentnode"] == True:
            parents.append(data[i]["parentnode_number"])
    return parents