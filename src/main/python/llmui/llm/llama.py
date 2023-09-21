from llmui.llm import LLM
import llama_cpp as llama


class Llama(LLM):

	__ANSWER_KEY = "Answer: "

	def __init__(self, path: str):
		self.model = llama.Llama(model_path=path)

	def chat(self, message: str) -> str:
		output = self.model(message)["choices"][0]["text"]
		return output[output.find(self.__ANSWER_KEY)+len(self.__ANSWER_KEY):]

	def reset(self):
		pass
