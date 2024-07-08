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


class FullVertex(BaseVertex):
    condition_function: Callable[[Dict], bool]
    execute_function: Callable[[Dict], Dict]

    def __init__(
        self,
        condition_function: Callable[[Dict], bool] = None,
        execute_function: Callable[[Dict], Dict] = None,
    ):
        if condition_function is None:
            self.condition_function = lambda x: True
        else:
            self.condition_function = condition_function

        if execute_function is None:
            self.execute_function = lambda x: x
        else:
            self.execute_function = execute_function

    def condition(self, context: Dict[str, Any]) -> bool:
        return self.condition_function(context)

    def execute(self, context: Dict[str, Any]) -> Dict:
        return self.execute_function(context)


Vertex = Union[Callable[[Dict], Dict], BaseVertex, None]
