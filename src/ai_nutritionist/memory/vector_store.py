import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

from src.ai_nutritionist.settings import settings


class Memory(BaseModel):
    """"Memory dataclass"""
    text: str
    metadata: dict
    score: float | None = None

    @property
    def id(self) -> str | None:
        return self.metadata.get("id")

    @property
    def timestamp(self) -> datetime | None:
        ts = self.metadata.get("timestamp")
        return datetime.fromisoformat(ts) if ts else None


class VectorStore:
    """
    A singleton class for managing a vector store using Qdrant for memory storage and retrieval.

    Attributes:
        EMBEDDING_MODEL (str): The model used for generating embeddings.
        COLLECTION_NAME (str): The name of the collection in the vector store.
        SIMILARITY_THRESHOLD (float): The threshold for determining similarity between memories.

    Methods:
        search_memories(query, k=5): Searches for memories similar to the query.
        find_similar_memory(text): Finds a memory similar to the given text.
        store_memory(text, metadata): Stores a new memory or updates an existing one.
    """

    # Class parameters
    EMBEDDING_MODEL = settings.EMBEDDING_MODEL
    COLLECTION_NAME = settings.COLLECTION_NAME
    SIMILARITY_THRESHOLD = settings.SIMILARITY_THRESHOLD

    # Singleton pattern parameters
    _instance: Optional["VectorStore"] = None
    _initialized: bool = False

    def __new__(cls) -> "VectorStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self.logger = logging.getLogger(__name__)
            self.model = SentenceTransformer(self.EMBEDDING_MODEL)
            self.client = QdrantClient(
                url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY
            )
            self._initialized = True

    def _collection_exists(self) -> bool:
        """
        Check if the collection with the specified name exists in the client's collections.

        Returns:
            bool: True if the collection exists, False otherwise.
        """
        collections = self.client.get_collections().collections
        return any(col.name == self.COLLECTION_NAME for col in collections)

    def _create_collection(self) -> None:
        """
        Creates a new collection in the vector store.

        Raises:
            Any exceptions raised by the client.create_collection method.
        """
        sample_embedding = self.model.encode("sample text")
        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=len(sample_embedding),
                distance=Distance.COSINE,
            ),
        )

    def search_memories(self, query: str, k: int = 5) -> list[Memory]:
        """
        Search for memories in the vector store that are similar to the given query.

        Args:
            query (str): The search query to find similar memories.
            k (int, optional): The maximum number of similar memories to return. Defaults to 5.

        Returns:
            list[Memory]: A list of Memory objects that are similar to the query.
        """

        if not self._collection_exists():
            return []

        self.logger.debug("Vectorstore memory search starts.")
        query_embedding = self.model.encode(query)
        results = self.client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=query_embedding.tolist(),
            limit=k,
        )
        self.logger.debug(f"Vectorstore found {len(results)} memories.")

        return [
            Memory(
                text=hit.payload["text"],
                metadata={k: v for k, v in hit.payload.items() if k != "text"},
                score=hit.score,
            )
            for hit in results
        ]

    def find_similar_memory(self, text: str) -> Memory | None:
        """
        Find a memory in the vector store that is most similar to the given text.

        Args:
            text (str): The text to compare against stored memories.

        Returns:
            Memory | None: The most similar Memory object if its similarity score 
            meets or exceeds the defined threshold, otherwise None.
        """

        results = self.search_memories(text, k=1)
        if results:
            self.logger.debug(
                f"Found similar memory: '{results[0].text}' is similar to '{text}' with score {results[0].score}")
        if results and results[0].score >= self.SIMILARITY_THRESHOLD:
            return results[0]
        return None

    def store_memory(self, text: str, metadata: dict) -> None:
        """
        Store a memory in the vector store with the given text and metadata.

        If the memory collection does not exist, it creates a new one. It checks
        for similar existing memories and updates the metadata with the same ID
        if a similar memory is found. The text is encoded into an embedding and
        stored as a point in the vector store.

        Args:
            text (str): The text to be stored as a memory.
            metadata (dict): Additional metadata to associate with the memory.

        Raises:
            Any exceptions raised by the client.upsert method.
        """

        if not self._collection_exists():
            self.logger.info(
                "Memory collection not found. Creating a new collection.")
            self._create_collection()

        # Check if similar memory exists
        similar_memory = self.find_similar_memory(text)
        if similar_memory and similar_memory.id:
            metadata["id"] = similar_memory.id  # Keep same ID for update

        embedding = self.model.encode(text)
        point = PointStruct(
            id=metadata.get("id", hash(text)),
            vector=embedding.tolist(),
            payload={
                "text": text,
                **metadata,
            },
        )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point],
        )


def get_vector_store() -> VectorStore:
    """Get or create the VectorStore singleton instance."""
    return VectorStore()
