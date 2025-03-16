import logging
import uuid
from datetime import datetime

from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from src.ai_nutritionist.memory.vector_store import get_vector_store
from src.ai_nutritionist.prompts import MEMORY_ANALYSIS_PROMPT
from src.ai_nutritionist.settings import settings


class MemoryAnalysis(BaseModel):
    """Result of analyzing a message for memory-worthy content."""

    is_important: bool = Field(
        ...,
        description="Whether the message is important enough to be stored as a memory",
    )
    formatted_memory: str | None = Field(
        ..., description="The formatted memory to be stored"
    )


class MemoryManager:

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
        memories = self.vector_store.search_memories(
            context, k=settings.MEMORY_TOP_K)

        return [memory.text for memory in memories]

    def format_memories_for_prompt(self, memories: list[str]) -> str:
        if not memories:
            return ""
        return "\n".join(f"- {memory}" for memory in memories)


def get_memory_manager() -> MemoryManager:
    """Get a MemoryManager instance."""
    return MemoryManager()
