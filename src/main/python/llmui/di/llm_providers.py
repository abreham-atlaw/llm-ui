from llmui import config
from llmui.llm import LLM
from llmui.llm.poe_llm import GooglePaLM


class LLMProviders:

	@staticmethod
	def provide_default_llm() -> LLM:
		return GooglePaLM(config.POE_TOKEN)
