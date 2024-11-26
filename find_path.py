#!/usr/bin/python3

# algorithm to find a path through a set of linked nodes that uses each internodal segment exactly once in each direction

import sys
import argparse
import os

def set_data_path(filepath):
    while not os.path.isfile(filepath):
        if filepath.startswith('./'):
            filepath == filepath[2:]
        elif len(filepath) > 0:
            print('The filepath is not valid.')
            filepath == ''
        else:
            filepath = input(f'''
The current directory is: {os.getcwd()}
Enter the absolute or relative path of the file containing the array of node connections:
''')
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

def find_path(current_node,last_node,path_segs,leg_length,start_nodes):
    if leg_length == 0:
        start_nodes.remove(current_node)
    for neighbor in node_links[current_node]:
        if neighbor == last_node:   # prevents immediate reversal of the previous segment
            continue
        seg = (current_node,neighbor)
        if not seg in path_segs:    # prevents duplicate segments
            new_node = neighbor
            new_last_node = current_node
            new_path = path_segs + [seg]
            new_leg_length = leg_length + 1     # number of segments from last end node
            if new_node in end_nodes:
                if new_leg_length < min_leg:       # prevents path to end node with leg length less than minimum
                    continue
                elif set(new_path) == seg_set:
                    complete_paths.append(new_path)
                    return
                else:                           # path has reached an end node        
                    new_leg_length = 0
                    if new_node in start_nodes:
                        new_last_node = -1      # allows path reversal by nullifying last node
                    elif len(start_nodes) > 0:
                        new_node = start_nodes[0] # use next available start node to begin next leg
                    else:
                        continue
            find_path(
                current_node=new_node,
                last_node=new_last_node,
                path_segs=new_path,
                leg_length=new_leg_length,
                start_nodes=start_nodes.copy()
            )

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
end_nodes = [n for n in range(len(node_links)) if len(node_links[n]) == 1 and node_links[n][0] > -1]
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
find_path(current_node=end_nodes[0], last_node=-1, path_segs=[], leg_length=0,start_nodes=end_nodes.copy())
for i in range(len(complete_paths)):
    print('Path #' + str(i + 1) + ':\n' + str(complete_paths[i]))
output_decision = input('Do you want to save the results to a file? (y/n): ')
if output_decision == 'y':
    prompt = 'Enter a filename. By default, file will save to current directory: ' + str(os.getcwd()) + '\n'
    output_path = os.path.split(input(prompt))
    while len(output_path[0]) > 0 and not os.path.isdir(output_path[0]):
        prompt = 'That is not a valid filepath. Try again: \n'
        output_path = os.path.split(input(prompt))
    final_path = os.path.join(output_path[0],output_path[1])
    output_text = ''
    with open(final_path,'w') as file:
        for result in complete_paths:
            file.write(str(result) + '\n\n')