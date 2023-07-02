import typing
from abc import ABC, abstractmethod

from dataclasses import dataclass

from llmui.core.environment.action import LLMUIAction


@dataclass
class LLMUIState:

    action_stack: typing.List[LLMUIAction]
    output: str

