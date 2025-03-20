import logging
from typing import Literal

from langgraph.graph import END

from ai_nutritionist.graph.state import AINutritionistState
from ai_nutritionist.settings import settings

logging.getLogger(__name__)
logger = logging.getLogger(__name__)


def should_summarize_conversation(
    state: AINutritionistState,
) -> Literal["summarize_conversation_node", "__end__"]:
    """
    Determine if the conversation should be summarized based on the number of messages.

    Args:
        state (AINutritionistState): The current state containing conversation details.

    Returns:
        Literal["summarize_conversation_node", "__end__"]: Returns "summarize_conversation_node"
        if the number of messages exceeds the defined trigger threshold, otherwise returns "__end__".
    """

    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        logger.debug(
            f"Summarization node triggered. Messages count: {len(messages)} > {settings.TOTAL_MESSAGES_SUMMARY_TRIGGER}"
        )
        return "summarize_conversation_node"

    return END
