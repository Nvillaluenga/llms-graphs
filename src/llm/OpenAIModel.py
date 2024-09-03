from langchain_openai import ChatOpenAI
from src.llm import LLMModel


class OpenAIModel(LLMModel):

    def __init__(self, name, config):
        self._name = name
        self._model = ChatOpenAI(**config)

    def invoke(self, prompt: str) -> str:
        return self._model.invoke(prompt).content
