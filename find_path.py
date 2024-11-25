#!/usr/bin/python3

# algorithm to find a path through a set of linked nodes that uses each internodal segment exactly once in each direction

import sys
import argparse
import os

def parse_input(input_text):
    if input_text[0] == '/':
        data_path = input_text
    else:
        if input_text[:2] == './':
            input_text == input_text[2:]    
        data_path = os.path.join(os.getcwd(),input_text)
    return data_path

def set_data_path(filepath):
    while not os.path.isfile(filepath):
        if len(filepath) > 0:
            print('The filepath is not valid.')
        else:
            input_text = input(f'''
The current directory is: {os.getcwd()}
Enter the absolute or relative path of the file containing the array of node connections:
''')
        filepath = parse_input(input_text)
    return filepath

def make_array(path):
    arr = []
    with open(path) as file:
        for line in file:
            try :
                arr.append([int(i) for i in line.split(',')])
            except ValueError as e:
                return e
    return arr

def count_segs(node_links):
    seg_set = set()
    for n in range(len(node_links)):
        if node_links[n][0] > -1:
            for neighbor in node_links[n]:
                try:
                    if not n in node_links[neighbor]:
                        raise Exception('Inconsistent values in node array. Each child node must mutally reference its parent node.')
                except Exception as e:
                    return e
                seg = (n,neighbor)
                if not seg in seg_set:
                    seg_set.add(seg)
    return seg_set

def find_path(current_node,last_node,path_segs,leg_length):
    if len(path_segs) == len(seg_set) and leg_length >= min_leg:
        complete_paths.append(path_segs)
        return
    else:
        node_arr = node_links[current_node]
        for node in node_arr:
            if node == last_node:
                continue
            seg = (current_node,node)
            if not seg in path_segs:
                new_path = path_segs + [seg]
                if leg_length < min_leg or len(node_links[node]) > 1 or len(end_nodes) == 0:
                    find_path(current_node=node, last_node=current_node,
                              path_segs=new_path, leg_length=leg_length + 1)
                elif node in (end_nodes):
                    end_nodes.remove(node)
                    find_path(current_node=node, last_node=-1,
                              path_segs=new_path, leg_length=0)
                else:
                    find_path(current_node=end_nodes.pop(0),last_node=-1,
                              path_segs=new_path,leg_length=0)

# parser to capture command-line arguments
parser = argparse.ArgumentParser(description=(
                                    'Finds every path through a network of connected nodes that uses each segment exactly once in each direction.\n\n'

                                    'Takes a text file containing a comma-separated array as input. Each line of the file (counting from 0) represents '
                                    'the corresponding zero-indexed node number and lists each neigboring nodes to which it is connected. All node links '
                                    'are mutual, so any node listed as neighbor of another node must also list that node as its neighbor. Nodes containing '
                                    'only the value -1 are considered empty and excluded from the path calculation. (This is useful if noncontiguous node '
                                    'numbering is desired.)\n\n'

                                    'Nodes with only 1 neighbor are end nodes. Each path will start and end at an end node, and the path may not '
                                    'immediately reverse itself by returning to the preceding node except at an end node.'
                                    )
)
parser.add_argument('filepath', nargs='?', default='')
parser.add_argument('-c','--min_seg_count', default=2, type=int, help='Sets the minimum number of segments for each leg between ending nodes within a path.')
args = parser.parse_args()
arg_path = args.filepath
min_leg = args.min_seg_count

data_path = set_data_path(arg_path)
node_links = make_array(data_path)
if type(node_links) == "<class 'ValueError'>":
    print('There are invalid values in the node array file.')
    print(type(node_links))
    print(node_links)
    sys.exit()
end_nodes = []
for node in range(len(node_links)):
    if len(node_links[node]) == 1 and node_links[node][0] > -1:
        end_nodes.append(node)
if len(end_nodes) == 0:
    print('There is no end node in the array file. At least one node must have only one neighbor.')
    sys.exit()
seg_set = count_segs(node_links)
if isinstance(seg_set,Exception):
    print('There was a problem with the data in the node array file.')
    print(type(seg_set))
    print(seg_set)
    sys.exit()

complete_paths = []
find_path(current_node=end_nodes.pop(0), last_node=-1, path_segs=[], leg_length=0)
for i in range(len(complete_paths)):
    print('Path #' + str(i + 1) + ':\n' + str(complete_paths[i]))