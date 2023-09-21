from lib.gai_client import Llama2Client
from llmui.di.utils_providers import UtilsProviders
from llmui.llm import LLM


class GAILlama2(LLM):

	def __init__(self):
		self.__client = UtilsProviders.provide_llama2_client()

	def chat(self, message: str) -> str:
		return self.__client.generate(message)

	def reset(self):
		pass
