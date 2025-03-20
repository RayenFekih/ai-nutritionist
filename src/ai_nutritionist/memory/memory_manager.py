import logging
import uuid
from datetime import datetime

from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from ai_nutritionist.memory.vector_store import get_vector_store
from ai_nutritionist.prompts import MEMORY_ANALYSIS_PROMPT
from ai_nutritionist.settings import settings


class MemoryAnalysis(BaseModel):
    """
    A Pydantic dataclass representing memory analysis with attributes to determine
    importance and store formatted memory.

    Attributes:
        is_important (bool): Indicates if the message is significant enough
            to be stored as a memory.
        formatted_memory (str | None): The formatted memory content to be stored.
    """

    is_important: bool = Field(
        ...,
        description="Whether the message is important enough to be stored as a memory",
    )
    formatted_memory: str | None = Field(
        ..., description="The formatted memory to be stored"
    )


class MemoryManager:
    """
    Manages memory operations including analysis, extraction, storage, and retrieval
    of important user messages. Utilizes LLMs to analyze messages for
    memory-worthy content and stores them in a vector store if deemed important.
    Provides functionality to retrieve relevant memories based on context and format
    them for prompts.

    Attributes:
        vector_store (VectorStore): The singleton instance for storing and retrieving memories.
        logger (Logger): Logger for logging memory operations.
        llm (ChatGroq): Language model for analyzing messages.

    Methods:
        _analyze_memory(message: str) -> MemoryAnalysis:
            Analyzes a message to determine its importance and format it for storage.

        extract_and_store_memories(message: BaseMessage) -> None:
            Extracts important memories from a human message and stores them if not similar to existing ones.

        get_relevant_memories(context: str) -> list[str]:
            Retrieves a list of relevant memories based on the provided context.

        format_memories_for_prompt(memories: list[str]) -> str:
            Formats a list of memories into a string suitable for prompts.
    """

    def __init__(self):
        self.vector_store = get_vector_store()
        self.logger = logging.getLogger(__name__)
        self.llm = ChatGroq(
            model=settings.SMALL_TEXT_MODEL_NAME,
            api_key=settings.GROQ_API_KEY,
            temperature=0.1,
            max_retries=2,
        ).with_structured_output(MemoryAnalysis)

    def _analyze_memory(self, message: str) -> MemoryAnalysis:
        prompt = MEMORY_ANALYSIS_PROMPT.format(message=message)
        return self.llm.invoke(prompt)

    def extract_and_store_memories(self, message: BaseMessage) -> None:
        """
        Extracts important memories from a given message and stores them if they do not already exist.

        Args:
            message (BaseMessage): The message to be analyzed and potentially stored as a memory.
        """

        if message.type != "human":
            return

        # Analyze the message for importance and formatting
        analysis = self._analyze_memory(message.content)
        if analysis.is_important and analysis.formatted_memory:
            self.logger.info(
                f"Important memory found: '{analysis.formatted_memory}'. Checking if a similar memory exists")
            # Check if similar memory exists
            similar = self.vector_store.find_similar_memory(
                analysis.formatted_memory)
            if similar:
                # Skip storage if we already have a similar memory
                self.logger.info(
                    f"Similar memory already exists: '{analysis.formatted_memory}' is similar to '{similar.text}'"
                )
                return

            # Store new memory
            self.logger.info(
                f"Storing new memory: '{analysis.formatted_memory}'")
            self.vector_store.store_memory(
                text=analysis.formatted_memory,
                metadata={
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                },
            )

    def get_relevant_memories(self, context: str) -> list[str]:
        """
        Retrieve relevant memories based on the provided context.

        Args:
            context (str): The context string to search for relevant memories.

        Returns:
            list[str]: A list of memory texts that are relevant to the context.
        """

        memories = self.vector_store.search_memories(
            context, k=settings.MEMORY_TOP_K)

        return [memory.text for memory in memories]

    def format_memories_for_prompt(self, memories: list[str]) -> str:
        """
        Formats a list of memory strings for display in a prompt.

        Args:
            memories (list[str]): A list of memory strings to be formatted.

        Returns:
            str: A single string with each memory prefixed by a dash and separated by newlines.
                Returns an empty string if the input list is empty.
        """

        if not memories:
            return ""
        return "\n".join(f"- {memory}" for memory in memories)


def get_memory_manager() -> MemoryManager:
    """Get a MemoryManager instance."""
    return MemoryManager()
