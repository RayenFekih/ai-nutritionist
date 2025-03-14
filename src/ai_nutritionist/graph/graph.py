from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from src.ai_nutritionist.graph.nodes import (
    conversation_node,
    memory_extraction_node,
    memory_injection_node,
)
from src.ai_nutritionist.graph.state import AINutritionistState


def create_graph():

    graph_builder = StateGraph(AINutritionistState)

    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("memory_extraction_node", memory_extraction_node)
    graph_builder.add_node("memory_injection_node", memory_injection_node)

    graph_builder.add_edge(START, "memory_extraction_node")
    graph_builder.add_edge("memory_extraction_node", "memory_injection_node")
    graph_builder.add_edge("memory_injection_node", "conversation_node")
    graph_builder.add_edge("conversation_node", END)

    return graph_builder


memory = MemorySaver()
graph = create_graph().compile(checkpointer=memory)
