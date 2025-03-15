from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from src.ai_nutritionist.graph.edges import should_summarize_conversation
from src.ai_nutritionist.graph.nodes import (
    conversation_node,
    memory_extraction_node,
    memory_injection_node,
    summarize_conversation_node,
)
from src.ai_nutritionist.graph.state import AINutritionistState


def create_graph():

    graph_builder = StateGraph(AINutritionistState)

    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("memory_extraction_node", memory_extraction_node)
    graph_builder.add_node("memory_injection_node", memory_injection_node)
    graph_builder.add_node("summarize_conversation_node",
                           summarize_conversation_node)

    graph_builder.add_edge(START, "memory_extraction_node")
    graph_builder.add_edge("memory_extraction_node", "memory_injection_node")
    graph_builder.add_edge("memory_injection_node", "conversation_node")
    graph_builder.add_conditional_edges(
        "conversation_node", should_summarize_conversation)

    graph_builder.add_edge("summarize_conversation_node", END)

    return graph_builder


memory = MemorySaver()
graph = create_graph().compile(checkpointer=memory)
