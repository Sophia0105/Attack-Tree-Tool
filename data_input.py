import json
import read_json
import easygui

def open_promt():
    filename = easygui.fileopenbox()
    f_json = read_json.open_file(filename)
    # print(f_json)

    # if len(f_json) > 0 and f_json[-1].get("id") is not None:
    last_node =f_json[-1]
    # else:
    id = last_node["id"] + 1
    
    text = input("Node text: ")
    node_type = input("Node type (and/or/end): ")
    parent_node = int(input("Number of the parent node: "))

    new_node = {"text_string": text, "node_type": node_type,"id": id, "parentnode": True, "parentnode_number": parent_node}
    print(new_node)
    f_json.append(new_node)
    read_json.close_file(filename, f_json)

open_promt()