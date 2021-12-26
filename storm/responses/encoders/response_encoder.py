from abc import ABC, abstractmethod
from typing import Any


class BaseResponseEncoder(ABC):
    @abstractmethod
    def encode(self, data: Any) -> bytes:
        pass
