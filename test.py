from src.nodes import LLMFeature, LLMNode, CallableNode
from src.vertex import ConditionVertex, ExecuteVertex, FullVertex
from src.dag import DAG

def main() -> None:
    feature_1: LLMFeature = LLMFeature(
        name='something',
        prompt_template='What is {a} + {b}? 1'
    )
    feature_2: LLMFeature = LLMFeature(
        name='something',
        prompt_template='What is {a} + {b}? 0',
        priority=0
    )
    feature_3: LLMFeature = LLMFeature(
        name='something',
        prompt_template='What is {a} + {b}? 3',
        priority=3
    )
    llm_node: LLMNode = LLMNode(features=[feature_1, feature_2, feature_3], model = None)

    llm_node.execute({"a": 1, "b": 2})

    callable_node: CallableNode = CallableNode(lambda x: {"c": 3, "d": 4})

    print(callable_node.execute({"e": 5}))

    dag = DAG()

    dag.add_node("llm_node", llm_node)
    dag.add_node("callable_node", callable_node)
    dag.add_node("A", lambda x: f"node A with input {x}")
    dag.add_node("B", lambda x: f"node B with input {x}")
    dag.add_node("C", lambda x: f"node C with input {x}")
    dag.add_node("D", lambda x: f"node D with input {x}")
    dag.add_node("E", lambda x: f"node E with input {x}")

    dag.add_vertex(llm_node, callable_node)
    dag.add_vertex(callable_node, "A", lambda x: True)
    condition_vertex = ConditionVertex(lambda x: True)
    execute_vertex = ExecuteVertex(lambda x: x | {"vertex": True})
    full_vertex = FullVertex(condition_fuction= lambda x: True, execute_function= lambda x: x | {"full_vertex": True})
    dag.add_vertex('A', 'B', condition_vertex)
    dag.add_vertex('A', 'C', execute_vertex)
    dag.add_vertex('B', 'D', full_vertex)
    dag.add_vertex('C', 'D')
    dag.add_vertex('C', 'E', lambda x: False)
    # dag.add_vertex(lambda x: True, 'D', 'E')

    # Perform Topological Sort
    l, map = dag.execute({"a": 1, "b": 2})
    print(l)
    print(map)
    

main()