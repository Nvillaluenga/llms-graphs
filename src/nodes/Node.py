from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Callable, List, Any, Dict, Union
from langchain_core.language_models.chat_models import BaseChatModel


class BaseNode(ABC):
    @abstractmethod
    def execute(self, context: Dict[str, Any]):
        pass


class CallableNode(BaseNode):
    f: Callable

    def __init__(self, f: Callable[[Dict], Dict]):
        self.f = f

    def execute(self, context: Dict[str, Any]):
        # This is a space for doing mapping, checking, or other things
        result = self.f(context)
        return result if isinstance(result, dict) else {"text": result}


@dataclass
class LLMFeature:
    name: str
    prompt_template: str
    priority: int = 1


class LLMNode(BaseNode):
    features: List[LLMFeature]
    model: BaseChatModel
    feature_separator: str = "\n\n"

    def __init__(self, features: List[LLMFeature], model: BaseChatModel):
        self.features = features
        self.features.sort(key=lambda x: x.priority)

        self.model = model

    def execute(self, context: Dict[str, Any]):
        llm_input = ""
        for feature in self.features:
            try:
                llm_input += (
                    self.feature_separator
                    + feature.prompt_template.format(**context)
                )
            except KeyError as e:
                print(
                    f'Couldn\'t load feature "{feature.name}" with template "{feature.prompt_template}" because of missing key "{e}"'
                )

        result = self.model.invoke(llm_input)
        return result.dict()


Node = Union[Callable[[Dict], Dict], BaseNode]
