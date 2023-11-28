from typing import Optional

from llmui.core.agent.directed.lib.handler import Handler
from llmui.core.agent.directed.sections.debug.states.user_help_state import UserHelpState
from llmui.core.environment import LLMUIState, LLMUIAction


class UserHelpHandler(Handler[UserHelpState, None]):

	def _init_internal_state(self) -> UserHelpState:
		return UserHelpState()

	def __get_user_input(self, message: str) -> str:
		return input(message)

	def handle(self, state: LLMUIState, args: None) -> Optional[LLMUIAction]:
		self.get_internal_state().user_input = self.__get_user_input(f"""
I seem to be stuck on this error:		
{state.output}

Can you provide a bit of insight so I can solve it:
""")
		return None
