#!/usr/bin/python3


from CS312Graph import *
from ArrayVersion import *
from HeapVersion import *
import time


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: make switch for heap version
        path_edges = []
        node2 = self.network.nodes[destIndex]
        total_length = self.Solution[node2.node_id][0]
        while self.Solution[node2.node_id][1] != None:
            node1 = self.Solution[node2.node_id][1]
            len = self.Solution[node2.node_id][0] - self.Solution[node1.node_id][0]
            path_edges.append( (node1.loc, node2.loc, '{:.0f}'.format(len)) )
            node2 = node1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        if use_heap:
            self.Solution = hDijkstra(self.network, self.source)
        else:
            self.Solution = aDijkstra(self.network, self.source)

        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        t2 = time.time()
        return (t2-t1)

