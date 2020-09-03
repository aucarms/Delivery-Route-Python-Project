import csv

# Constructor
# Space-time complexity is O(1)
class Vertex:
    def __init__(self, label, full_address, loc_name):
        self.label = int(label) 
        self.full_address = full_address
        self.loc_name = loc_name

        
# Constructor
# Space-time complexity is O(1)
class Graph:
    def __init__(self):
        self.adjacent_edge_list = {}
        self.edge_distance = {}

    #function to add vertex to a list
    # Space-time complexity is O(N)
    def add_vertex(self, new_vertex):
        self.adjacent_edge_list[new_vertex] = []

    #function to add all distances to a list
    # Space-time complexity is O(N)
    def add_total_distance(self, from_vertex, to_vertex, distance = 1.0):
        self.edge_distance[(from_vertex, to_vertex)] = distance
        self.edge_distance[(to_vertex, from_vertex)] = distance
        self.adjacent_edge_list[from_vertex].append(to_vertex)


