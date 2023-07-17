from llmui.llm import LLM


class ConsoleLLM(LLM):

	def reset(self):
		pass

	def chat(self, message: str) -> str:
		print(f">>{message}")
		return input("$ ")
