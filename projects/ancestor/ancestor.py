from util import Queue

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
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
        if pair[0] not in graph.vertices:
            graph.add_vertex(pair[0])
        if pair[1] not in graph.vertices:
            graph.add_vertex(pair[1])
        graph.add_edge(v1=pair[1],v2=pair[0])
    if graph.get_parents(starting_node) == set():
        # print(starting_node)
        # print(graph.get_parents(starting_node))
        return -1
    
    max_depth = 0
    max_depth_id = starting_node
    q = Queue()
    visited = set()
    q.enqueue([starting_node])
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]

        if v not in visited:
            visited.add(v)
            if len(path) > max_depth:
                max_depth = len(path)
                max_depth_id = v
            elif len(path) == max_depth and v < max_depth_id:
                max_depth = len(path)
                max_depth_id = v
            for parent in graph.get_parents(v):
                parent_path = path.copy()
                parent_path.append(parent)
                q.enqueue(parent_path)
    return max_depth_id


