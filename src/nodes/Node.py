from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, List, Any, Dict, Union
from langchain_core.language_models.chat_models import BaseChatModel


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


Node = Union[Callable[[Dict], Dict], BaseNode]