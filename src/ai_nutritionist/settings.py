from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    GROQ_API_KEY: str

    TEXT_MODEL_NAME: str = "llama-3.3-70b-versatile"
    SMALL_TEXT_MODEL_NAME: str = "gemma2-9b-it"

    # QDRant vector store
    QDRANT_API_KEY: str | None
    QDRANT_URL: str
    QDRANT_PORT: str = "6333"
    QDRANT_HOST: str | None = None
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    COLLECTION_NAME: str = "long_term_memory"
    SIMILARITY_THRESHOLD: float = 0.9  # Threshold for considering memories as similar

    MEMORY_TOP_K: int = 3
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 3
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 20

    ERROR_LOGGING_PATH: str = "logs"


settings = Settings()
