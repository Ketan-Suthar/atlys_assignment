from .storage import StorageInterface
from .storage import LocalStorage

class StorageFactory:
    @staticmethod
    def create_storage() -> StorageInterface:
        from config import Settings
        storage_type = Settings.STORAGE_TYPE
        if storage_type == "local":
            return LocalStorage("scraped_data.json")
        raise ValueError(f"Unsupported storage type: {storage_type}")
