from typing import List, Dict
from src.dag import DAG


class UseCase:
    dag: DAG
    test_set: List
    eval_metrics: Dict
