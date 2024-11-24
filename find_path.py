#!/usr/bin/python3

# algorithm to find a path through a set of linked nodes that uses each internodal segment exactly once in each direction

node_links = (
    (3,),
    (10,),
    (5,),
    (0,6,7),
    (10,6,8),
    (2,10,9),
    (3,4,11),
    (3,11,9),
    (4,11,9),
    (5,7,8),
    (1,4,5),
    (6,7,8)
)

def count_segs():
    seg_set = set()
    for n in range(len(node_links)):
        if node_links[n][0] > -1:
            for neighbor in node_links[n]:
                seg = (n,neighbor)
                if not seg in seg_set:
                    seg_set.add(seg)
    return seg_set

def find_path(current_node,last_node,root_node,leg_length,path_segs):
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
                    find_path(new_node, current_node, root_node, leg_length + 1, new_path)
                else:
                    new_node = root_node + 1
                    find_path(new_node, -1, new_node, 0, new_path)
        
        
seg_set = count_segs()
print(seg_set)
print(len(seg_set))
min_leg_length = 8
complete_paths = []
current_path = []
start_node = 0
last_node = -1
find_path(start_node,last_node, start_node, 0, current_path)
for i in range(len(complete_paths)):
    print('Path #' + str(i + 1) + ':\n' + str(complete_paths[i]))