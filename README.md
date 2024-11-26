Finds paths through a graph of connected nodes, using each edge (segment) exactly once in each direction.

Takes a text file containing a comma-separated array as input. Each line of the file (counting from 0) represents 
the corresponding zero-indexed node number and lists each neigboring nodes to which it is connected. All node 
links are mutual, so any node listed as neighbor of another node must also list that node as its neighbor. Nodes 
containing only the value -1 are considered empty and excluded from the path calculation. (This is useful if 
noncontiguous node numbering is desired.)

Nodes with only 1 neighbor are end nodes. Each path will start and end at an end node, and the path may not 
immediately reverse itself by returning to the preceding node except at an end node.

Prints results to terminal and provides option to save results to output file.
