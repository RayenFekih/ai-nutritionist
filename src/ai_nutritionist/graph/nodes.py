from langchain_core.messages import AIMessage

from src.ai_nutritionist.graph.state import AINutritionistState
from src.ai_nutritionist.graph.utils.chains import get_text_chat_chain


def conversation_node(state: AINutritionistState):

    chain = get_text_chat_chain()

    response = chain.invoke(
        {
            "messages": state["messages"],
        }
    )
    return {"messages": AIMessage(content=response)}
