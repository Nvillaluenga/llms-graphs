## Primer archivo

from typing import Callable, Optional, Mapping, Any, List, TypeVar, Generic

Input = TypeVar('Input')
Output = Dict[str, Any]

class Node(Generic[Input, Output]):
    pass

class LLMFeature:
    priority: int
    prompt_template: str
    name: str

@expected_input(TIPO)
class LLMNode(Node[LLMFeature, Output]):
    action: Callable[[List[LLMFeature]], Output]

task1: LLMNode = LLMNode()

task2: LLMNode = LLMNode()

task1 >> task2

task1.run(inputs)


class MyLibrary:

    @classmethod
    def run_graph(cls, root: Node):
        pass

MyLibrary.run_graph(task1)

