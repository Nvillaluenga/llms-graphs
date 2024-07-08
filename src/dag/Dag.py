from src.nodes import Node, CallableNode, BaseNode
from src.vertex import BaseVertex, Vertex, FullVertex
from typing import Union, List, Any, Dict, Tuple


def find_key_by_object(d, target_object):
    for key, value in d.items():
        if value is target_object:
            return key
    return None


class DAG:
    graph: Dict[str, List[Tuple[str, BaseVertex]]]
    nodes: Dict[str, BaseNode]

    def __init__(self):
        self.nodes = {}
        self.graph = {}

    def add_node(self, name: str, node: Node) -> None:
        if callable(node):
            node = CallableNode(f=node)
        self.graph[name] = []
        self.nodes[name] = node

    def add_vertex(
        self,
        node_from: Union[str, BaseNode],
        node_to: Union[str, BaseNode],
        vertex: Vertex = None,
    ):
        if vertex == None:
            vertex = FullVertex()

        elif callable(vertex):
            vertex = FullVertex(condition_function=vertex)

        if isinstance(node_from, BaseNode):
            node_from = find_key_by_object(self.nodes, node_from)
        if isinstance(node_to, BaseNode):
            node_to = find_key_by_object(self.nodes, node_to)

        self.graph[node_from].append((node_to, vertex))

    def get_topological_sort(
        self,
    ) -> Tuple[List[str], Dict[str, List[Tuple[str, BaseVertex]]]]:
        visited = set()
        stack = []
        dependency_map = {}
        for node in self.graph:
            if node not in visited:
                self._topological_sort_util(
                    node, visited, stack, dependency_map
                )
        stack.reverse()
        return stack, dependency_map

    def execute(self, general_context: Dict[str, Any]):
        outputs = {}
        node_execution_list, dependency_map = self.get_topological_sort()
        for node_name in node_execution_list:
            node_context = self._get_context_for_node(
                node_name=node_name,
                general_context=general_context,
                dependency_map=dependency_map,
                outputs=outputs,
            )
            node = self.nodes[node_name]
            node_result = node.execute(node_context)
            outputs[node_name] = node_result

        return node_execution_list, outputs

    # Utils functions
    def _topological_sort_util(
        self, node: str, visited: set, stack: list, dependency_map: dict
    ):
        visited.add(node)
        for neighbor, vertex in self.graph[node]:
            if neighbor not in visited:
                self._topological_sort_util(
                    neighbor, visited, stack, dependency_map
                )
            dependency_map[neighbor] = dependency_map.get(neighbor, []) + [
                (node, vertex)
            ]
        stack.append(node)

    def _get_context_for_node(
        self,
        node_name: str,
        general_context: Dict[str, Any],
        dependency_map: Dict[str, List[Tuple[str, BaseVertex]]],
        outputs: Dict[str, Dict[str, Any]],
    ):
        dependencies = dependency_map.get(node_name, [])
        node_context = {} | general_context
        for dependency_node, dependency_vertex in dependencies:
            dependency_node_output = outputs[dependency_node]
            if dependency_vertex.condition(dependency_node_output):
                node_partial_input = dependency_vertex.execute(
                    dependency_node_output
                )
                node_context = node_context | node_partial_input

        return node_context
