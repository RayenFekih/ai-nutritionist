from typing import Literal

from langgraph.graph import END

from src.ai_nutritionist.graph.state import AINutritionistState
from src.ai_nutritionist.settings import settings


def should_summarize_conversation(
    state: AINutritionistState,
) -> Literal["summarize_conversation_node", "__end__"]:
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"

    return END
