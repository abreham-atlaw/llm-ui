import typing
from copy import deepcopy

from lib.rl.environment import Environment
from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import WriteExecutor, ReadExecutor, RunExecutor
from llmui.core.environment.action_executor.parent_executor import ParentActionExecutor
from llmui.core.environment.state import LLMUIState


class LLMUIEnvironment(Environment[LLMUIState, LLMUIAction]):

	def __init__(self, working_dir: str, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__working_dir = working_dir
		self.__executor = ParentActionExecutor([
			WriteExecutor(),
			ReadExecutor(),
			RunExecutor()
		])

		self.__state = LLMUIState([], "No previous Commands")

	def perform_action(self, action: LLMUIAction):
		new_state = deepcopy(self.get_state())
		new_state.output = self.__executor(action)
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
