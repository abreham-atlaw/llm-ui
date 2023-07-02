from llmui.llm import LLM


class ConsoleLLM(LLM):

	def chat(self, message: str) -> str:
		print(f">>{message}")
		return input("$ ")
