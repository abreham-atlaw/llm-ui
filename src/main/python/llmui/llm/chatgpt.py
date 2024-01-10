import time

from .llm import LLM

import openai


class ChatGPT(LLM):

	def __init__(self, token: str, system: str, temperature: int = 0.7):
		openai.api_key = token
		self.__system = system
		self.__temperature = temperature

	def __chat(self, message: str) -> str:
		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			temperature=self.__temperature,
			messages=[
				{
					"role": "system",
					"content": self.__system
				},
				{
					"role": "user",
					"content": message
				}
			]
		)
		return response.choices[0].message.content

	def chat(self, message: str) -> str:
		try:
			return self.__chat(message)
		except openai.error.RateLimitError as ex:
			print("ChatGPT: Sleeping...")
			time.sleep(1.1 * 60)
			return self.chat(message)

	def reset(self):
		pass
