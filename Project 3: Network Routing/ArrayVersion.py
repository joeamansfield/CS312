from CS312Graph import *

a_node_distances = {}
a_queue = []

def aDijkstra(network, sourceindex): #O(v^2), O(v) function nested in v time loop
    for node in network.nodes: #order n, just initializes a new array with distances for each point, still n space since creating 1 copy with less info
        a_node_distances[node.node_id] = [float("inf"), None]
        aInsert(node)
    source = network.nodes[sourceindex]
    a_node_distances[source.node_id] = [0, None]
    while len(a_queue) != 0: #v time, because there are v total elements in queue
        current_node = aDeleteMin() #O(v)
        if current_node == None:
            break #happens if there are points not connected - I don't know how to make the gui display this if the destination is one of those, maybe worth looking at later
        distance = a_node_distances[current_node.node_id][0]
        for edge in current_node.neighbors:
            if edge.dest in a_queue:
                if distance + edge.length < a_node_distances[edge.dest.node_id][0]:
                    a_node_distances[edge.dest.node_id][0] = distance + edge.length
                    a_node_distances[edge.dest.node_id][1] = current_node
                    aDecreaseKey() #O(1)
    return a_node_distances

def aDeleteMin(): #total time v, since none of the n time functions were nested
    min = float("inf")
    id = None
    min_node = None
    for node in a_queue: #v members, constant time comparisons, total time is v
        key = node.node_id
        if a_node_distances[key][0] < min:
            min = a_node_distances[key][0]
            id = key
    if id == None: #triggers if no remaining nodes are connected, resulting in id never modified
        return None
    for i in range(len(a_queue)): #v members, constant time comparison, total time is v
        if a_queue[i].node_id == id:
            min_node = i
    min_node = a_queue.pop(min_node)
    return min_node

def aInsert(node):#literally nothing to be done to maintain order in array implementation, constant time
    a_queue.append(node)

def aDecreaseKey():#literally nothing to be done to maintain order in array implementation, constant time
    pass