from CS312Graph import *

h_node_distances = {}
h_node_locations = {}
queue_tree = [] #number is index of other array
queue_vals = [] #first item is node, second item is float distance

def hDijkstra(network, sourceindex):
    for node in network.nodes:
        hInsert(node, float("inf"))
    hDecreaseKey(sourceindex, 0)
    while len(queue_tree) != 0: #order v, since v total items in queue
        node_dist = hDeleteMin()
        if node_dist == None:
            break
        current_node = node_dist[0]
        distance = node_dist[1]
        h_node_distances[current_node.node_id, distance]
        for edge in current_node.neighbors:
            if distance + edge.length < queue_vals[queue_tree[h_node_locations[edge.dest]][1]]:
                hDecreaseKey(h_node_locations[edge.dest])
    return h_node_distances
    


def hDeleteMin():
    firstRoot = queue_tree[0]
    if queue_vals[firstRoot][1] == float("inf"):
        return None
    lastLeaf = queue_tree[len(queue_tree) - 1]
    queue_tree[0] = lastLeaf
    queue_tree[len(queue_tree) - 1] = firstRoot
    node_distance = queue_vals.pop(queue_tree.pop(-1))
    return node_distance


def hInsert(node, distance): #O(logv) because of bubbleup
    queue_vals.append([node, distance])
    h_node_locations[[len(queue_vals)-1]] = node
    queue_tree.append([len(queue_vals)-1])
    bubbleUp(len(queue_tree))

def hDecreaseKey(index, distance): #O(logv) because of bubbleup
    queue_vals[queue_tree[index]][1] = distance
    bubbleUp(index)

def bubbleUp(index): #runs max log(v) times, all comparisons inside are constant time
    if index != 0:
        if index % 2 == 0: #right side of tree index / 2 - 1 gives index of root node 
            root = queue_tree[(index / 2) - 1]
            leaf = queue_tree[index]
            if queue_vals[root][1] > queue_vals[leaf][1]:
                queue_tree[(index / 2) - 1] = leaf
                queue_tree[index] = root
                h_node_locations[queue_vals[leaf][0]] = (index / 2) - 1
                h_node_locations[queue_vals[root][0]] = index
                bubbleUp((index / 2) - 1)
        else: #left side of tree, (index-1)/2 gives index of root node
            root = queue_tree[(index - 1) / 2]
            leaf = queue_tree[index]
            if queue_vals[root][1] > queue_vals[leaf][1]:
                queue_tree[(index - 1) / 2] = leaf
                queue_tree[index] = root
                h_node_locations[queue_vals[leaf][0]] = (index - 1) / 2
                h_node_locations[queue_vals[root][0]] = index
                bubbleUp((index - 1) / 2)

def siftDown(index):
    if len(queue_tree) > (index * 2) + 1: #check if left leaf exists
        root = queue_tree[index]
        left = queue_tree[(index*2)+1]
        if len(queue_tree) > (index + 1) * 2: #right leaf exists
            right = queue_tree[(index+1)*2]
            if queue_vals[left][1] < queue_vals[right][1]: #left side smaller
                if queue_vals[root] > queue_vals[left]: #leaf smaller than root
                    queue_tree[index] = left
                    queue_tree[(index*2)+1] = root
                    h_node_locations[queue_vals[left][0]] = index
                    h_node_locations[queue_vals[root][0]] = (index*2)+1
                    siftDown((index*2)+1)
            else: # right side smaller
                if queue_vals[root][1] > queue_vals[right][1]: #leaf smaller than root
                    queue_tree[index] = right
                    queue_tree[(index+1)*2] = root
                    h_node_locations[queue_vals[right][0]] = index
                    h_node_locations[queue_vals[root][0]] = (index+1)*2
                    siftDown((index+1)*2)
        else: #only left leaf exists
            if queue_vals[root][1] > queue_vals[left][1]: #leaf smaller than root
                    queue_tree[index] = left
                    queue_tree[(index*2)+1] = root
                    h_node_locations[queue_vals[left][0]] = index
                    h_node_locations[queue_vals[root][0]] = (index*2)+1
                    siftDown((index*2)+1)
