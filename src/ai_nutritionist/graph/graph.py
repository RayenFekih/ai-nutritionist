from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from ai_nutritionist.graph.edges import should_summarize_conversation
from ai_nutritionist.graph.nodes import (
    conversation_node,
    memory_extraction_node,
    memory_injection_node,
    summarize_conversation_node,
)
from ai_nutritionist.graph.state import AINutritionistState


def create_graph():
    """
    Creates and returns a state graph for the AI Nutritionist.

    The graph consists of the following nodes:
    - "conversation_node": Handles the conversation logic.
    - "memory_extraction_node": Extracts memory from the conversation.
    - "memory_injection_node": Injects memory into the conversation.
    - "summarize_conversation_node": Summarizes the conversation.

    The edges between the nodes are defined as follows:
    - START -> "memory_extraction_node"
    - "memory_extraction_node" -> "memory_injection_node"
    - "memory_injection_node" -> "conversation_node"
    - Conditional edges from "conversation_node" based on the function `should_summarize_conversation`.
    - "summarize_conversation_node" -> END

    Returns:
        StateGraph: The constructed state graph for the AI Nutritionist.
    """

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
