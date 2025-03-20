
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from ai_nutritionist.graph.utils.helpers import (
    AsteriskRemovalParser,
    get_chat_model,
)
from ai_nutritionist.prompts import CHARACTER_PROMPT


def get_text_chat_chain(summary: str = ""):
    model = get_chat_model()
    system_message = CHARACTER_PROMPT

    if summary:
        system_message += (
            f"\n\nSummary of conversation earlier between Nour and the user: {summary}"
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    return prompt | model | AsteriskRemovalParser()
