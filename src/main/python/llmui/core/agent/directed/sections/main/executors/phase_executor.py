import typing

from llmui.core.agent.directed.lib.executor import LLMExecutor, I, O
from llmui.core.agent.directed.sections.common.executors.format_executor import FormatExecutor
from llmui.utils.format_utils import FormatUtils


class PhaseExecutor(LLMExecutor[typing.Tuple[str, str], typing.List[str]]):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__format_executor = FormatExecutor(
			llm=self._llm,
			output_format="""
{
	"0": first phase with it's description,
	"1": second phase with it's description,
	...
}
Note: only include phases. Don't include notes. 
"""
		)

	def _prepare_prompt(self, arg: typing.Tuple[str, str]) -> str:
		description, task = arg
		return f"""
I have the project description and task below. Can you break it down to multiple coding phases of development? Ignore the requirement gathering, setup, design and testing. Only include phases for coding development of the site.

Project Description:
{description}

Project Task:
{task}

It'll be great if you phrase the phases as tasks(commands)
"""

	def _prepare_output(self, output: str, arg: typing.Tuple[str, str]) -> typing.List[str]:
		output = self.__format_executor(output)
		phases = FormatUtils.extract_list_from_json_string(output)
		return phases
