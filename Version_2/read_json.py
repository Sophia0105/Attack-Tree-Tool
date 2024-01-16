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
        if data[i]["parentnode"] == True:
            labels.append(data[i]["probability"])
    return labels