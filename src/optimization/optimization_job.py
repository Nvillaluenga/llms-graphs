import json
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
    prompt_generation_prompt: str = """You are a master prompt generator, you are given a base prompt: 
```
{base_prompt}
```

and you are going to return 5 new prompts based on that base prompt that performs better, the response must be a json array containing string
something like this:

output: ["some prompt 1", "another different prompt 2", "a prompt 3"]
output: 
"""

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
        score = 0
        for test_case in self.job_input.test_set:
            test_case_prompt = prompt.format(**test_case.input_vars)
            # TODO: Change this I do not like rewriting test_cases like this
            test_case.generated_output = self.target_model.invoke(
                test_case_prompt
            )

            score += self.evaluator.evaluate(
                test_case=test_case, instruction=test_case_prompt
            )

        return score / max(len(self.job_input.test_set), 1)

    def generate_prompts(self, base_prompt: str) -> List[str]:
        """Generate a list of possible optimized prompts to test

        Args:
            base_prompt (str): some base prompt to base other generations

        Returns:
            List[str]: list of prompts
        """

        generate_prompt = self.prompt_generation_prompt.format(
            base_prompt=base_prompt
        )
        new_prompts_string = self.optimizer_model.invoke(generate_prompt)
        new_prompts_string = (
            new_prompts_string.replace("```json", "").replace("```", "").strip()
        )  # TODO: we can do better

        new_prompts = json.loads(new_prompts_string)
        return new_prompts

    def optimize_prompt(self) -> str:
        best_prompt = self.job_input.base_prompt
        best_score = self.evaluate_prompt(best_prompt)
        self.prompts_tested = [
            {"cycle": 0, "prompt": best_prompt, "score": best_score}
        ]
        for cycle in range(1, self.job_input.cycles + 1):
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
