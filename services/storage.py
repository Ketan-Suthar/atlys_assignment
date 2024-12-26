from typing import List
from pathlib import Path
import json
from models.product import Product
from redis import Redis
from typing import Optional
from .istorage import StorageInterface


class LocalStorage(StorageInterface):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def save(self, products: List[Product]):
        self.file_path.write_text(json.dumps([product.dict() for product in products], indent=4))

    def load(self) -> List[Product]:
        if self.file_path.exists():
            if len(self.file_path.read_text()) > 0:
                return [Product(**item) for item in json.loads(self.file_path.read_text())]
        return []

class RedisCache:
    def __init__(self, redis_client: Redis):
        self.client = redis_client

    def get(self, key: str) -> Optional[str]:
        return self.client.get(key)

    def set(self, key: str, value: str, expiry: int):
        self.client.setex(key, expiry, value)
