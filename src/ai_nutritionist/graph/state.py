from collections.abc import Sequence
from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AINutritionistState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    memory_context: str
    summary: str
