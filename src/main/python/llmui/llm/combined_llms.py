import typing

from llmui.llm import LLM


class CombinedLLM(LLM):

	def __init__(self, llms: typing.List[LLM]):
		self.__llms = llms

	def chat(self, message: str) -> str:
		for llm in self.__llms:
			try:
				return llm.chat(message)
			except Exception as ex:
				print(f"[+]{llm.__class__.__name__} failed with {ex}")
		raise Exception("All LLMs Failed")

	def reset(self):
		for llm in self.__llms:
			llm.reset()
