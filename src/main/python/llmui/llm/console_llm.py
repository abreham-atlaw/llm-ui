from llmui.llm import LLM


class ConsoleLLM(LLM):

	def reset(self):
		pass

	def chat(self, message: str) -> str:
		print(f">>{message}")
		contents = []
		while True:
			try:
				line = input()
			except EOFError:
				break
			contents.append(line)
		return "\n".join(contents)

