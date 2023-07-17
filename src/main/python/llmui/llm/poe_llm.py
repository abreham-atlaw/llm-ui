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

	def reset(self):
		self.__client.send_chat_break(self.__bot_name)


class GooglePaLM(PoeLLM):

	def __init__(self, token: str):
		super().__init__("acouchy", token)

	def chat(self, message: str) -> str:
		response = super().chat(message)
		if "[user]" in response:
			response = response[:response.find("[user]")]
		return response
