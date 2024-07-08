from langchain_openai import ChatOpenAI
from src.nodes import LLMFeature, LLMNode, CallableNode
from src.dag import DAG


def main() -> None:
    feature_1: LLMFeature = LLMFeature(
        name="something", prompt_template="What is {a} + {b}?"
    )

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    llm_node: LLMNode = LLMNode(features=[feature_1], model=llm)

    callable_node: CallableNode = CallableNode(
        lambda x: print(f"Executing callable node {x['content']}")
    )

    dag = DAG()

    dag.add_node("llm_node", llm_node)
    dag.add_node("callable_node", callable_node)
    dag.add_vertex(llm_node, callable_node)

    l, map = dag.execute({"a": 1, "b": 2})

    print(l)
    print(map)


main()
