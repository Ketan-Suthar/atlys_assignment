from abc import ABC, abstractmethod
from typing import List
from models import Product


class StorageInterface(ABC):
    @abstractmethod
    def save(self, products: List[Product]):
        pass

    @abstractmethod
    def load(self) -> List[Product]:
        pass
