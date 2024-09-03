from abc import ABC, abstractmethod
from src.test.Metric import Metric
from src.test.TestCase import TestCase
from typing import Dict, List
import numpy as np


class Evaluator(ABC):
    def __init__(self, metrics: List[Metric] = None):
        self.metrics = metrics if metrics else []

    @abstractmethod
    def evaluate(self, test_case: TestCase) -> float:
        pass

    @abstractmethod
    def batch_evaluate(self, test_case: List[TestCase]) -> List[float]:
        pass


class WeightedSumEvaluator(Evaluator):
    def __init__(
        self,
        metrics: List[Metric] = None,
        weights: Dict[str | Metric, int] = None,
    ):
        self.metrics = metrics if metrics else []

        self.weights = {}
        for key, value in weights.items():
            if isinstance(key, Metric):
                key = key.name
            self.weights[key] = value

    def aggregate_metrics(self, results: Dict[str, float]) -> float:
        weights = []
        scores = []
        for metric_name, score in results.items():
            weights.append(
                self.weights.get(metric_name, 1)
            )  # 1 is the default weight
            scores.append(score)

        weighted_sum = np.dot(scores, weights) / sum(weights)

        return weighted_sum

    def evaluate(
        self, test_case: TestCase, instruction: str
    ) -> (
        float
    ):  # Todo: should instruction be part of the test case? or the metric?
        results = {}
        for metric in self.metrics:
            result = metric.eval(
                predicted=test_case.generated_output,
                target=test_case.expected_output,
                instruction=instruction,
            )
            results[metric.name] = result

        return self.aggregate_metrics(results)

    def batch_evaluate(self, test_case: List[TestCase]) -> List[float]:
        pass


class BasicEvaluator(
    WeightedSumEvaluator
):  # Basically the same but all weights are the same (default to 1)
    def __init__(self, metrics: List[Metric] = None):
        self.metrics = metrics if metrics else []
        self.weights = {}
