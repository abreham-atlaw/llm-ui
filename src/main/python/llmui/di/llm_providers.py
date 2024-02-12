from llmui import config
from llmui.config import LLM_TEMPERATURE
from llmui.llm import LLM, Bard, ConsoleLLM
from llmui.llm.chatgpt import ChatGPT
from llmui.llm.combined_llms import CombinedLLM
from llmui.llm.gemini import Gemini
from llmui.llm.llama2gai import GAILlama2
from llmui.llm.poe_llm import GooglePaLM


class LLMProviders:

	@staticmethod
	def provide_default_llm() -> LLM:
		return LLMProviders.provide_combined_llm()

	@staticmethod
	def provide_combined_llm() -> CombinedLLM:
		return CombinedLLM([
			LLMProviders.provide_gemini(),
			LLMProviders.provide_chatgpt()
		])

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

	@staticmethod
	def provide_gemini() -> Gemini:
		return Gemini(
			token=config.GEMINI_API_KEY,
			temperature=LLM_TEMPERATURE
		)
