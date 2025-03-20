from langchain_core.messages import HumanMessage
from langgraph.graph import END

from ai_nutritionist.graph.edges import should_summarize_conversation
from ai_nutritionist.graph.state import AINutritionistState
from ai_nutritionist.settings import settings


class TestShouldSummarizeConversation:

    # Returns "summarize_conversation_node" when message count exceeds TOTAL_MESSAGES_SUMMARY_TRIGGER
    def test_returns_summarize_node_when_message_count_exceeds_threshold(self):

        # Create a state with more messages than the threshold
        messages = [HumanMessage(content=f"Message {i}") for i in range(
            settings.TOTAL_MESSAGES_SUMMARY_TRIGGER+1)]
        state: AINutritionistState = {
            "messages": messages,
            "memory_context": "",
            "summary": ""
        }

        # Act
        result = should_summarize_conversation(state)

        # Assert
        assert result == "summarize_conversation_node"

    # Handles empty messages list
    def test_returns_end_when_messages_list_is_empty(self):

        # Create a state with empty messages list
        state: AINutritionistState = {
            "messages": [],
            "memory_context": "",
            "summary": ""
        }

        # Act
        result = should_summarize_conversation(state)

        # Assert
        assert result == END

    # Returns END when message count is less than or equal to TOTAL_MESSAGES_SUMMARY_TRIGGER
    def test_returns_end_when_message_count_is_below_or_equal_to_threshold(self):

        # Create a state with messages equal to the threshold
        messages = [HumanMessage(content=f"Message {i}") for i in range(
            settings.TOTAL_MESSAGES_SUMMARY_TRIGGER)]
        state: AINutritionistState = {
            "messages": messages,
            "memory_context": "",
            "summary": ""
        }

        # Act
        result = should_summarize_conversation(state)

        # Assert
        assert result == END
