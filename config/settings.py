from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_name: str = "llama3.1:8b"
    ollama_host: str = "http://localhost:11434"
    temperature: float = 0.7
    max_tokens: int = 2048
    max_iterations: int = 10
    tot_branches: int = 3
    tot_depth: int = 3
    tot_beam_width: int = 2

    class Config:
        env_file = ".env"

settings = Settings()