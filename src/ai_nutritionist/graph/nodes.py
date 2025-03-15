from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableConfig

from src.ai_nutritionist.graph.state import AINutritionistState
from src.ai_nutritionist.graph.utils.chains import get_text_chat_chain
from src.ai_nutritionist.graph.utils.helpers import get_chat_model
from src.ai_nutritionist.memory.memory_manager import get_memory_manager
from src.ai_nutritionist.settings import settings


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
    chain = get_text_chat_chain(state.get("summary", ""))

    response = chain.invoke(
        {
            "messages": state["messages"],
            "memory_context": memory_context,
        },
        config
    )
    return {"messages": AIMessage(content=response)}


def summarize_conversation_node(state: AINutritionistState):
    model = get_chat_model()
    summary = state.get("summary", "")

    if summary:
        summary_message = (
            f"This is summary of the conversation to date between Nour and the user: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = (
            "Create a summary of the conversation above between Nour and the user. "
            "The summary must be a short description of the conversation so far, "
            "but that captures all the relevant information shared between Nour and the user:"
        )

    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    delete_messages = [
        RemoveMessage(id=m.id)
        for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
    ]
    return {"summary": response.content, "messages": delete_messages}
