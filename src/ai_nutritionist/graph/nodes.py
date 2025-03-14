from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig

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


def memory_injection_node(state: AINutritionistState):

    memory_manager = get_memory_manager()

    # Get relevant memories based on recent conversation
    recent_context = " ".join([m.content for m in state["messages"][-3:]])
    memories = memory_manager.get_relevant_memories(recent_context)

    # Format memories
    memory_context = memory_manager.format_memories_for_prompt(memories)

    return {"memory_context": memory_context}


def conversation_node(state: AINutritionistState, config: RunnableConfig):

    memory_context = state.get("memory_context", "")
    chain = get_text_chat_chain()

    response = chain.invoke(
        {
            "messages": state["messages"],
            "memory_context": memory_context,
        },
        config
    )
    return {"messages": AIMessage(content=response)}
