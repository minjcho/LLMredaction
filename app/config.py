from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ALLOW_REMOTE_LLM: bool = False
    FERNET_KEY: str = ""
    ADMIN_KEY: str = "changeme"
    DOC_TTL_SEC: int = 3600  # default: 1 hour
    GEMINI_API_KEY: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
