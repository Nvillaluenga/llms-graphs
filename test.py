from src.nodes import LLMFeature, LLMNode, CallableNode
from src.dag import DAG

def main() -> None:
    feature: LLMFeature = LLMFeature(
        name='something',
        prompt_template='What is {{a}} + {{b}}?'
    )
    llm_node: LLMNode = LLMNode(features=[feature], model = None)

    llm_node.execute({"a": 1, "b": 2})

    callable_node: CallableNode = CallableNode(lambda x: {"c": 3, "d": 4})

    print(callable_node.execute({"e": 5}))

    dag = DAG()

    dag.add_node("llm_node", llm_node)
    dag.add_node("callable_node", callable_node)
    dag.add_node("A", lambda x: True)
    dag.add_node("B", lambda x: True)
    dag.add_node("C", lambda x: True)
    dag.add_node("D", lambda x: True)
    dag.add_node("E", lambda x: True)

    dag.add_vertex(lambda x: True, llm_node, callable_node)
    dag.add_vertex(lambda x: True, callable_node, "A")

    dag.add_vertex(lambda x: True, 'A', 'B')
    dag.add_vertex(lambda x: True, 'A', 'C')
    dag.add_vertex(lambda x: True, 'B', 'D')
    dag.add_vertex(lambda x: True, 'C', 'D')
    dag.add_vertex(lambda x: True, 'C', 'E')
    # dag.add_vertex(lambda x: True, 'D', 'E')

    # Perform Topological Sort
    topological_order = dag.topological_sort()
    print("Topological Sort of the nodes:")
    print(topological_order)

main()