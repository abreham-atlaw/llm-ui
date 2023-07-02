import typing
from dataclasses import dataclass


@dataclass
class LLMUIAction:
    command: str
