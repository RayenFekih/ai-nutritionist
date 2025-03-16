import logging
from typing import Literal

from langgraph.graph import END

from src.ai_nutritionist.graph.state import AINutritionistState
from src.ai_nutritionist.settings import settings

logging.getLogger(__name__)
logger = logging.getLogger(__name__)


def should_summarize_conversation(
    state: AINutritionistState,
) -> Literal["summarize_conversation_node", "__end__"]:
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        logger.debug(
            f"Summarization node triggered. Messages count: {len(messages)} > {settings.TOTAL_MESSAGES_SUMMARY_TRIGGER}"
        )
        return "summarize_conversation_node"

    return END
