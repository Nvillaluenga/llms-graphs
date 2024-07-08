from src.nodes import LLMFeature, LLMNode, CallableNode
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

    dag.add_vertex(lambda x: "llm to callable", llm_node, callable_node)
    dag.add_vertex(lambda x: "callable to A", callable_node, "A")

    dag.add_vertex(lambda x: "A to B", 'A', 'B')
    dag.add_vertex(lambda x: "A to C", 'A', 'C')
    dag.add_vertex(lambda x: "B to D", 'B', 'D')
    dag.add_vertex(lambda x: "C to D", 'C', 'D')
    dag.add_vertex(lambda x: "C to E", 'C', 'E')
    # dag.add_vertex(lambda x: True, 'D', 'E')

    # Perform Topological Sort
    l, map = dag.execute({"a": 1, "b": 2})
    print(l)
    print(map)
    

main()