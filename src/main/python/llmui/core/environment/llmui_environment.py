import json
import os
import typing
from copy import deepcopy

from lib.rl.environment import Environment
from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import WriteExecutor, ReadExecutor, RunExecutor
from llmui.core.environment.action_executor.bash_executor import BashExecutor
from llmui.core.environment.action_executor.parent_executor import ParentActionExecutor
from llmui.core.environment.state import LLMUIState


class LLMUIEnvironment(Environment[LLMUIState, LLMUIAction]):

	def __init__(self, environ_file: str, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__state = self.__load_state(environ_file)
		self.__working_dir = self.state.root_path
		self.__executor = ParentActionExecutor([
			WriteExecutor(cwd=self.__working_dir),
			ReadExecutor(cwd=self.__working_dir),
			RunExecutor(cwd=self.__working_dir),
			BashExecutor(cwd=self.__working_dir)
		], cwd=self.__working_dir)

	def __load_state(self, path: str) -> LLMUIState:
		with open(path, 'r') as file:
			data = json.load(file)
		return LLMUIState(
			project_description=data.get('project_description', ''),
			action_stack=[],
			outputs=[],
			read_content=self.__read_file,
			root_path=data.get('cwd', ''),
			task=data.get("task", "")
		)

	def __read_file(self, path: str) -> str:
		return self.__executor(LLMUIAction(
			command="read",
			args=[path]
		))

	def perform_action(self, action: LLMUIAction):
		if action is None:
			return
		new_state = deepcopy(self.get_state())
		new_state.outputs.append(self.__executor(action))
		new_state.action_stack.append(action)
		self.__state = new_state

	def render(self):
		pass

	def update_ui(self):
		pass

	def check_is_running(self) -> bool:
		return True

	def is_action_valid(self, action: LLMUIAction, state: LLMUIState) -> bool:
		return self.__executor.is_valid_action(action)

	def get_state(self) -> LLMUIState:
		return self.__state

	def _is_episode_over(self, state: LLMUIState) -> bool:
		return False

	def _get_reward(self, state: LLMUIState) -> float:
		return 0

	def _initialize(self):
		super()._initialize()
		os.chdir(self.__working_dir)

