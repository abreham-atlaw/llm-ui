from llmui.llm import LLM


class ConsoleLLM(LLM):

	def reset(self):
		pass

	@staticmethod
	def __get_multiline_input():
		lines = []
		while True:
			line = input()
			if line == "^D":
				return "\n".join(lines)
			lines.append(line)

	def chat(self, message: str) -> str:
		print(f">>{message}")
		return self.__get_multiline_input()
