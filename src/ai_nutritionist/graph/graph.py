from langgraph.graph import END, START, StateGraph

from src.ai_nutritionist.graph.nodes import conversation_node
from src.ai_nutritionist.graph.state import AINutritionistState


def create_graph():

    graph_builder = StateGraph(AINutritionistState)

    graph_builder.add_node("conversation_node", conversation_node)

    graph_builder.add_edge(START, "conversation_node")

    graph_builder.add_edge("conversation_node", END)

    return graph_builder


graph = create_graph().compile()
