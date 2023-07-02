
from .llm import LLM


class Bard(LLM):

    def chat(self, message: str) -> str:
        raise Exception("Unimplemented")