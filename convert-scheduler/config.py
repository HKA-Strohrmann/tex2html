from arxiv.config import Settings as BaseSettings

class Settings (BaseSettings):
    CONVERT_PATH: str = '/process-full-corpus:8080'
    LOG_PATH: str = 'out.log'

settings = Settings()