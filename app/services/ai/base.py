from abc import ABC, abstractmethod
from typing import Optional


class BaseAIProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str,
        image_base64: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        raise NotImplementedError
