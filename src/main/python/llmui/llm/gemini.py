import google.generativeai as genai

from llmui.llm import LLM


class Gemini(LLM):

	def __init__(self, token: str, temperature: float = 0.7, patience=10):
		genai.configure(api_key=token)
		self.__model = genai.GenerativeModel('gemini-pro')
		self.__temperature = temperature
		self.__patience = patience

	def chat(self, message: str, temp: float = None, tries=None) -> str:
		if temp is None:
			temp = self.__temperature
		if tries is None:
			tries = self.__patience
		try:
			response = self.__model.generate_content(
				contents=[message],
				generation_config=genai.GenerationConfig(
					temperature=temp,
				),
				safety_settings={
					cat: genai.types.HarmBlockThreshold.BLOCK_NONE
					for cat in [7, 8, 9, 10]
				}
			)
			return response.text
		except ValueError as ex:
			print(f"[-]Gemini: Error {ex}. Retrying...")
			if tries == 0:
				raise ex
			return self.chat(message, temp=(temp+0.1)%1, tries=tries-1)

	def reset(self):
		pass
