from typing import Callable, Any, Dict, Union
from abc import abstractmethod, ABC

class BaseVertex(ABC):
    required: bool = True

    @abstractmethod
    def condition(self, context: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict:
        pass


class PassVertex(BaseVertex): # Eliminiar estas clases
    def condition(self, context: Dict[str, Any]) -> bool:
        return True

    def execute(self, context: Dict[str, Any]) -> Dict:
        return context


class ConditionVertex(BaseVertex):
    condition_function: Callable[[Dict], bool]
    
    def __init__(self, condition_fuction: Callable[[Dict], bool]):
        self.condition_function = condition_fuction
    
    def condition(self, context: Dict[str, Any]) -> bool:
        return self.condition_function(context)

    def execute(self, context: Dict[str, Any]) -> Dict:
        return context
    
class ExecuteVertex(BaseVertex):
    execute_function: Callable[[Dict], Dict]
    
    def __init__(self, execute_function: Callable[[Dict], Dict]):
        self.execute_function = execute_function
    
    def condition(self, context: Dict[str, Any]) -> bool:
        return True

    def execute(self, context: Dict[str, Any]) -> Dict:
        return self.execute_function(context)

class FullVertex(BaseVertex):
    condition_function: Callable[[Dict], bool]
    execute_function: Callable[[Dict], Dict]
    
    def __init__(self, condition_fuction: Callable[[Dict], bool], execute_function: Callable[[Dict], Dict]):
        self.execute_function = execute_function
        self.condition_function = condition_fuction
    
    def condition(self, context: Dict[str, Any]) -> bool:
        return self.condition_function(context)

    def execute(self, context: Dict[str, Any]) -> Dict:
        return self.execute_function(context)
    
Vertex = Union[Callable[[Dict], Dict], BaseVertex, None]
