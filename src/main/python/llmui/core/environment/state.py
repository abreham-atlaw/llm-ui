import os
import typing
from abc import ABC, abstractmethod

from dataclasses import dataclass

from llmui.core.environment.action import LLMUIAction


@dataclass
class LLMUIState:

    project_description: str

    action_stack: typing.List[LLMUIAction]
    output: str

    read_content: typing.Callable
    root_path: str

    @property
    def files(self) -> typing.List[str]:
        file_list = []
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.root_path)
                file_list.append(relative_path)
        return file_list
