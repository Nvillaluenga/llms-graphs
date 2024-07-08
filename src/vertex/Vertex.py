from typing import Callable, Any, Dict, Union

class BaseVertex():
    f: Callable
    def __init__(self, f: Callable[[Dict], Dict]):
        self.f = f

    def execute(self, context: Dict[str, Any]):
        result = self.f(context)
        return result if isinstance(result, dict) else { "text": result }
    
Vertex = Union[Callable[[Dict], Dict], BaseVertex]
