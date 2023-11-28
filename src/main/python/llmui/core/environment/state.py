import os
import typing
from abc import ABC, abstractmethod

from dataclasses import dataclass

from llmui.core.environment.action import LLMUIAction


@dataclass
class LLMUIState:

    project_description: str
    task: str

    action_stack: typing.List[LLMUIAction]
    outputs: typing.List[str]

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

    @property
    def output(self) -> str:
        if len(self.outputs) == 0:
            return ""
        return self.outputs[-1]

    def __deepcopy__(self, memodict={}):
        return LLMUIState(
            project_description=self.project_description,
            task=self.task,
            action_stack=self.action_stack.copy(),
            outputs=self.outputs.copy(),
            read_content=self.read_content,
            root_path=self.root_path
        )
