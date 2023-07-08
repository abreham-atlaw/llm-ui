import typing

import poe

from llmui.llm import LLM


class PoeLLM(LLM):

	def __init__(self, bot_name: str, token: str):
		self.__client = poe.Client(token)
		self.__bot_name = bot_name

	def chat(self, message: str) -> str:
		response: typing.Dict = None
		for response in self.__client.send_message(self.__bot_name, message):
			pass
		return response["text"]
