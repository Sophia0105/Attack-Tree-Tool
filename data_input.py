import json
import read_json
import easygui

def append_node(filename, input_node):
    f_json = read_json.open_file(filename)
    
    text = input_node[0]
    node_type = input_node[1]
    id = input_node[2]
    parent_node = input_node[4]

    new_node = {"text_string": text, "node_type": node_type,"id": id, "parentnode": True, "parentnode_number": parent_node}
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