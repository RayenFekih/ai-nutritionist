
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.ai_nutritionist.graph.utils.helpers import (
    AsteriskRemovalParser,
    get_chat_model,
)
from src.ai_nutritionist.prompts import CHARACTER_PROMPT


def get_text_chat_chain():
    model = get_chat_model()
    system_message = CHARACTER_PROMPT

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    return prompt | model | AsteriskRemovalParser()
