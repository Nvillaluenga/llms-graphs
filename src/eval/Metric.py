from abc import ABC, abstractmethod
from rouge_score import rouge_scorer
from typing import Dict
from sacrebleu import corpus_bleu

from src.llm.LLMModel import LLMModel


class Metric(ABC):
    name: str
    config: Dict

    def __init__(self, name=None, config=None):
        if name:
            self.name = name
        self.config = config if config else {}

    @abstractmethod
    def eval(
        predicted: str, target: str = None, instruction: str = None
    ) -> float:
        pass


class LLMMetric(Metric):
    _prompt: str  # All prompts have up to 3 variables in the prompt "instruction", "target" and "predicted"
    _llm: LLMModel

    def __init__(self, name, prompt: str, llm: LLMModel, config=None):
        if name:
            self.name = name
        self.config = config if config else {}
        self._prompt = prompt
        self._llm = llm

    def eval(
        self, predicted: str, target: str = None, instruction: str = None
    ) -> float:
        prompt = self._prompt.format(
            predicted=predicted, target=target, instruction=instruction
        )
        result = self._llm.invoke(prompt=prompt)
        return float(result) / 100


# TODO: Rouge metrics, probably, should change to one class and you choose the rouge type when you instantiate it
class Rouge1Metric(Metric):
    name: str = "Rouge 1"

    def eval(self, predicted: str, target: str, instruction: str = None):

        scorer = rouge_scorer.RougeScorer(["rouge1"], use_stemmer=True)
        score = scorer.score(prediction=predicted, target=target)
        return score["rouge1"].fmeasure


class Rouge2Metric(Metric):
    name: str = "Rouge 2"

    def eval(self, predicted: str, target: str, instruction: str = None):

        scorer = rouge_scorer.RougeScorer(["rouge2"], use_stemmer=True)
        score = scorer.score(prediction=predicted, target=target)
        return score["rouge2"].fmeasure


class RougeLMetric(Metric):
    name: str = "Rouge L"

    def eval(self, predicted: str, target: str, instruction: str = None):

        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        score = scorer.score(prediction=predicted, target=target)
        return score["rougeL"].fmeasure


class RougeLSumMetric(Metric):
    name: str = "Rouge L Sum"

    def eval(self, predicted: str, target: str, instruction: str = None):

        scorer = rouge_scorer.RougeScorer(["rougeLsum"], use_stemmer=True)
        score = scorer.score(prediction=predicted, target=target)
        return score["rougeLsum"].fmeasure


# Bleu
class BleuCorpusMetric(Metric):
    name: str = "Bleu Corpus"

    def eval(self, predicted: str, target: str, instruction: str = None):
        reference = [target]  # SacreBLEU expects a list of reference texts
        hypothesis = [predicted]
        bleu = corpus_bleu(hypothesis, [reference])
        return bleu.score / 100
