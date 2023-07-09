import typing

from abc import ABC, abstractmethod


class LLM(ABC):

    @abstractmethod
    def chat(self, message: str) -> str:
        pass

    @abstractmethod
    def reset(self):
        pass
