import os

class Settings:
    STATIC_TOKEN = "securetoken123"
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    CACHE_EXPIRY = 3600
    STORAGE_TYPE = os.getenv("STORAGE_TYPE", "local")  # Default to local
