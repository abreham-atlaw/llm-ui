from llmui import config
from llmui.llm import LLM
from llmui.llm.poe_llm import PoeLLM


class LLMProviders:

	@staticmethod
	def provide_default_llm() -> LLM:
		return PoeLLM(config.DEFAULT_BOT, config.POE_TOKEN)
