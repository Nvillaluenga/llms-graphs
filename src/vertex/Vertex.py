from typing import Callable, Any, Dict, Union

class BaseVertex():
    f: Callable
    def __init__(self, f: Callable[[Dict], Dict]):
        self.f = f

    def execute(self, context: Dict[str, Any]):
        print("in vertex execute")
        return self.f(context)
    
Vertex = Union[Callable[[Dict], Dict], BaseVertex]
