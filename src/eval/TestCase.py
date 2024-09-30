from dataclasses import dataclass
from typing import Dict


@dataclass
class TestCase:
    input_vars: Dict[str, str]
    expected_output: str
    generated_output: str = None
