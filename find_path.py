#!/usr/bin/python3

# algorithm to find a path through a set of linked nodes that uses each internodal segment exactly once in each direction

import sys
import os


def parse_input(input_text):
    if input_text[0] == '/':
        data_path == input_text
    else:
        if input_text[:2] == './':
            input_text == input_text[2:]    
        data_path = os.path.join(os.getcwd(),input_text)
    return data_path

def set_data_path():
    data_path = ''
    while not os.path.isfile(data_path):
        if len(sys.argv) > 1:
            input_text = sys.argv[1]
        else:
            input_text = input(f'''
The current directory is: {os.getcwd()}
Enter the absolute or relative path of the file containing the array to analyze:
''')
        data_path = parse_input(input_text)
    return data_path

def make_array(path):
    arr = []
    with open(path) as file:
        for line in file:
            arr.append([int(i) for i in line.split(',')])
    return arr


#node_links = (
#    (3,),
#    (10,),
#    (5,),
#    (0,6,7),
#    (10,6,8),
#    (2,10,9),
#    (3,4,11),
#    (3,11,9),
#    (4,11,9),
#    (5,7,8),
#    (1,4,5),
#    (6,7,8)
#)

def count_segs(node_links):
    seg_set = set()
    for n in range(len(node_links)):
        if node_links[n][0] > -1:
            for neighbor in node_links[n]:
                seg = (n,neighbor)
                if not seg in seg_set:
                    seg_set.add(seg)
    return seg_set

def find_path(node_links,current_node,last_node,root_node,leg_length,path_segs):
    if len(path_segs) == len(seg_set) and leg_length >= min_leg_length - 1:
        complete_paths.append(path_segs)
        return
    else:
        node_arr = node_links[current_node]
        for n in node_arr:
            if n == last_node:
                continue
            seg = (current_node,n)
            if not seg in path_segs:
                new_node = seg[-1]
                new_path = path_segs + [seg]
                if new_node > 1 or leg_length < min_leg_length:
                    find_path(node_links,new_node, current_node, root_node, leg_length + 1, new_path)
                else:
                    new_node = root_node + 1
                    find_path(node_links,new_node, -1, new_node, 0, new_path)

data_path = ''
while not os.path.isfile(data_path):
    data_path = set_data_path()
node_links = make_array(data_path)
seg_set = count_segs(node_links)
print(len(seg_set))
min_leg_length = 8
complete_paths = []
current_path = []
start_node = 0
last_node = -1
find_path(node_links,start_node,last_node, start_node, 0, current_path)
for i in range(len(complete_paths)):
    print('Path #' + str(i + 1) + ':\n' + str(complete_paths[i]))