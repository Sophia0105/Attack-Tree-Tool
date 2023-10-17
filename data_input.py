import json
import read_json
import easygui

def append_node(filename):
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

def delete_node(filename, nr_vertices):
    f_json = read_json.open_file(filename)

    node_nr = int(input("Which node number do you want to delete? "))
    for i in range(nr_vertices+1):
        print(str(f_json[i]["id"]))
        if f_json[i]["id"] == node_nr:
            deleted_node = f_json.pop(i)
        else: 
            deleted_node = "None"


    print("deleted node: " + str(deleted_node))
    read_json.close_file(filename, f_json)



filename = easygui.fileopenbox()
# append_node(filename)
# delete_node(filename, 13)