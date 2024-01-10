from llmui import config
from llmui.config import LLM_TEMPERATURE
from llmui.llm import LLM, Bard, ConsoleLLM
from llmui.llm.chatgpt import ChatGPT
from llmui.llm.llama2gai import GAILlama2
from llmui.llm.poe_llm import GooglePaLM


class LLMProviders:

	@staticmethod
	def provide_default_llm() -> LLM:
		return LLMProviders.provide_chatgpt()

	@staticmethod
	def provide_console_llm() -> ConsoleLLM:
		return ConsoleLLM()

	@staticmethod
	def provide_chatgpt() -> ChatGPT:
		return ChatGPT(
			config.OPENAI_KEY,
			"You are a programmer with accurate responses",
			temperature=LLM_TEMPERATURE
		)
