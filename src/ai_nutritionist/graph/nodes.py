from langchain_core.messages import AIMessage, HumanMessage

from src.ai_nutritionist.graph.state import AINutritionistState
from src.ai_nutritionist.graph.utils.chains import get_text_chat_chain
from src.ai_nutritionist.memory.memory_manager import get_memory_manager


def memory_extraction_node(state: AINutritionistState):
    """Extract and store important information from the last message."""
    if not state["messages"]:
        return {}

    memory_manager = get_memory_manager()
    memory_manager.extract_and_store_memories(state["messages"][-1])
    return {}


def conversation_node(state: AINutritionistState):

    chain = get_text_chat_chain()

    response = chain.invoke(
        {
            "messages": state["messages"],
        }
    )
    return {"messages": AIMessage(content=response)}
