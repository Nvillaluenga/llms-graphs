from abc import ABC, abstractmethod
from rouge_score import rouge_scorer
from typing import Dict
from sacrebleu import corpus_bleu
import json


class Metric(ABC):
    @abstractmethod
    def eval(predicted: Dict, target: Dict):
        pass


# TODO: Rouge metrics, probably, should change to one class and you choose the rouge type when you instantiate it
class Rouge1Metric(Metric):
    def eval(prediction: Dict, target: Dict):
        prediction = json.dumps(prediction)
        target = json.dumps(target)
        scorer = rouge_scorer.RougeScorer(["rouge1"], use_stemmer=True)
        score = scorer.score(prediction=prediction, target=target)
        return score["rouge1"].fmeasure


class Rouge2Metric(Metric):
    def eval(prediction: Dict, target: Dict):
        prediction = json.dumps(prediction)
        target = json.dumps(target)
        scorer = rouge_scorer.RougeScorer(["rouge2"], use_stemmer=True)
        score = scorer.score(prediction=prediction, target=target)
        return score["rouge2"].fmeasure


class RougeLMetric(Metric):
    def eval(prediction: Dict, target: Dict):
        prediction = json.dumps(prediction)
        target = json.dumps(target)
        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        score = scorer.score(prediction=prediction, target=target)
        return score["rougeL"].fmeasure


class RougeLSumMetric(Metric):
    def eval(prediction: Dict, target: Dict):
        prediction = json.dumps(prediction)
        target = json.dumps(target)
        scorer = rouge_scorer.RougeScorer(["rougeLsum"], use_stemmer=True)
        score = scorer.score(prediction=prediction, target=target)
        return score["rougeLsum"].fmeasure


# Bleu
class BleuCorpusMetric(Metric):
    def eval(prediction: Dict, target: Dict):
        reference = [target]  # SacreBLEU expects a list of reference texts
        hypothesis = [prediction]
        bleu = corpus_bleu(hypothesis, [reference])
        return bleu.score / 100
