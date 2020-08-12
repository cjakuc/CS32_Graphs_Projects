from util import Queue, Stack

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Vertex does not exist")

    def get_parents(self, vertex_id):
        """
        Get all parents (edges) of a vertex.
        """
        return self.vertices[vertex_id]


def earliest_ancestor(ancestors, starting_node):
    graph = Graph()
    for pair in ancestors:
        graph.add_vertex(pair[0])
        graph.add_vertex(pair[1])
        graph.add_edge(v1=pair[1],v2=pair[0])
    
    max_depth = 1
    max_depth_id = -1
    q = Queue()
    q.enqueue([starting_node])
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]

        if (len(path) >= max_depth and v < max_depth_id) or (len(path) > max_depth):
            max_depth = len(path)
            max_depth_id = v
        for parent in graph.get_parents(v):
            parent_path = path.copy()
            parent_path.append(parent)
            q.enqueue(parent_path)
    return max_depth_id


