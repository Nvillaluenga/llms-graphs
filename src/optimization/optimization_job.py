from dataclasses import dataclass
from typing import List
from src.eval.Evaluator import Evaluator
from src.eval.TestCase import TestCase
from src.llm.LLMModel import LLMModel


@dataclass
class OptimizationJobInput:
    test_set: List[TestCase]
    base_prompt: str
    cycles: int


class OptimizationJob:
    job_input: OptimizationJobInput
    evaluator: Evaluator
    target_model: LLMModel
    optimizer_model: LLMModel
    prompts_tested: List

    def __init__(
        self,
        job_input: OptimizationJobInput,
        evaluator: Evaluator,
        target_model: LLMModel,
        optimizer_model: LLMModel,
    ) -> None:
        self.job_input = job_input
        self.evaluator = evaluator
        self.target_model = target_model
        self.optimizer_model = optimizer_model

    def evaluate_prompt(self, prompt: str) -> float:
        """Evaluate a prompt using the evaluator for this optimization job

        Args:
            prompt (str): prompt to evaluate

        Returns:
            float: score of the prompt
        """
        pass

    def generate_prompts(self, base_prompt: str) -> List[str]:
        """Generate a list of possible optimized prompts to test

        Args:
            base_prompt (str): some base prompt to base other generations

        Returns:
            List[str]: list of prompts
        """

    def optimize_prompt(self) -> str:
        best_prompt = self.job_input.base_prompt
        best_score = self.evaluate_prompt(best_prompt)
        self.prompts_tested = [
            {"cycle": 0, "prompt": best_prompt, "score": best_score}
        ]
        for cycle in self.job_input.cycles:
            new_prompts = self.generate_prompts(best_prompt)

            for new_prompt in new_prompts:
                score = self.evaluate_prompt(new_prompt)
                self.prompts_tested.append(
                    {"cycle": cycle, "prompt": new_prompt, "score": score}
                )

                if score > best_score:
                    best_score = score
                    best_prompt = new_prompt

        return best_prompt
