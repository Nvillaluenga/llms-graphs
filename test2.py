from abc import abstractmethod
from dataclasses import dataclass
from typing import Union, Callable, List, Any, Dict, Tuple
from langchain_core.language_models.chat_models import BaseChatModel
from collections import deque


class BaseNode:
    @abstractmethod
    def execute(self, context: Dict[str, Any]):
        inputs: Dict[str, str] = context['input']
        pass

class CallableNode(BaseNode):
    f: Callable
    def __init__(self, f: Callable[[Dict], Dict]):
        self.f = f

    def execute(self, context: Dict[str, Any]):
        # This is a space for doing mapping, checking, or other things
        print("In node callable execute")
        return self.f(context)

@dataclass
class LLMFeature:
    name: str
    prompt_template: str
    priority: int = 1

class LLMNode(BaseNode):
    features: List[LLMFeature]
    model: BaseChatModel

    def __init__(self, features: List[LLMFeature], model: BaseChatModel):
        self.features = features
        self.model = model

    def execute(self, context: Dict[str, Any]):
        llm_input = '\n'.join([f.prompt_template for f in self.features])
        print(f"In llm execute {llm_input}")
        # result = self.model.invoke(llm_input)
        # return result


class BaseVertex():
    f: Callable
    def __init__(self, f: Callable[[Dict], Dict]):
        self.f = f

    def execute(self, context: Dict[str, Any]):
        print("in vertex execute")
        return self.f(context)
    
Node = Union[Callable[[Dict], Dict], BaseNode]
Vertex = Union[Callable[[Dict], Dict], BaseVertex]

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
    
def main() -> None:
    feature: LLMFeature = LLMFeature(
        name='something',
        prompt_template='What is {{a}} + {{b}}?'
    )
    llm_node: LLMNode = LLMNode(features=[feature], model = None)

    llm_node.execute({"a": 1, "b": 2})

    callable_node: CallableNode = CallableNode(lambda x: {"c": 3, "d": 4})

    print(callable_node.execute({"e": 5}))

    dag = DAG()

    dag.add_node("llm_node", llm_node)
    dag.add_node("callable_node", callable_node)
    dag.add_node("A", lambda x: True)
    dag.add_node("B", lambda x: True)
    dag.add_node("C", lambda x: True)
    dag.add_node("D", lambda x: True)
    dag.add_node("E", lambda x: True)

    dag.add_vertex(lambda x: True, llm_node, callable_node)
    dag.add_vertex(lambda x: True, callable_node, "A")

    dag.add_vertex(lambda x: True, 'A', 'B')
    dag.add_vertex(lambda x: True, 'A', 'C')
    dag.add_vertex(lambda x: True, 'B', 'D')
    dag.add_vertex(lambda x: True, 'C', 'D')
    dag.add_vertex(lambda x: True, 'C', 'E')
    # dag.add_vertex(lambda x: True, 'D', 'E')

    # Perform Topological Sort
    topological_order = dag.topological_sort()
    print("Topological Sort of the nodes:")
    print(topological_order)

main()