from src.nodes import Node, CallableNode, BaseNode
from src.vertex import BaseVertex, Vertex
from typing import Union, List, Any, Dict, Tuple

def find_key_by_object(d, target_object):
    for key, value in d.items():
        if value is target_object:
            return key
    return None

class DAG:
    graph: Dict[str, List[Tuple[str, BaseVertex]]]

    def __init__(self):
        self.nodes = {}
        self.graph = {}

    def add_node(self, name:  str, node: Node) -> None:
        if callable(node):
            node = CallableNode(f=node)
        self.graph[name] = []
        self.nodes[name] = node

    def add_vertex(self, vertex: Vertex, node_from: Union[str, BaseNode], node_to: Union[str, BaseNode]):
        if callable(vertex):
            vertex = BaseVertex(f=vertex)
        
        if isinstance(node_from, BaseNode):
            node_from = find_key_by_object(self.nodes, node_from)
        if isinstance(node_to, BaseNode):
            node_to = find_key_by_object(self.nodes, node_to)


        self.graph[node_from].append((node_to, vertex))
    
    def topological_sort_util(self, node: str, vertex: BaseVertex, visited: set, stack: list):
        visited.add(node)
        for (neighbor, vertex) in self.graph[node]:
            if neighbor not in visited:
                self.topological_sort_util(neighbor, vertex, visited, stack)
        stack.append((node, vertex))

    def topological_sort(self):
        visited = set()
        stack = []
        for node in self.graph:
            if node not in visited:
                self.topological_sort_util(node, None, visited, stack)
        stack.reverse()  # Reverse the stack to get the topological order
        return stack