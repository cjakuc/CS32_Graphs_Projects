
class Node():
    def __init__(self, ID,parent = None, child = None):
        self.ID = ID
        if parent != None:
            self.parents = [parent]
        else:
            self.parent = []
        if child != None:
            self.children = [child]
        else:
            self.children = []

    def addParent(self, parent):
        self.parents.append(parent)

    def addChild(self, child):
        self.children.append(child)
    
    def getParents(self):
        return self.parents


def earliest_ancestor(ancestors, starting_node):
    nodes = {}
    for pair in ancestors:
        if pair[0] in nodes:
            nodes[pair[0]].addChild(pair[1])
        else:
            nodes[pair[0]] = Node(ID=pair[0],child=pair[1])
        if pair[1] in nodes:
            nodes[pair[1]].addParent(pair[0])
        else:
            nodes[pair[1]] = Node(ID=pair[1],parent=pair[0])

    current_node = nodes[starting_node]
    while nodes[current_node]


def _earliest_helper(node:Node, nodes:dict, depth = 0):
    max_depth = depth
    ID = node.ID
    if node.parents == []:
        return ID, depth
    parents = node.getParents()
    for p in parents:
        current_node = nodes[p]
        current_ID, current_depth = _earliest_helper(current_node, nodes, depth=depth+1)
        if current_depth > max_depth:
            max_depth = current_depth
            ID = current_ID
        elif current_depth == max_depth:
            if current_ID < ID:
                ID = current_ID