from abc import ABC, abstractmethod


class LLMModel(ABC):
    name: str
    config: dict

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        pass
