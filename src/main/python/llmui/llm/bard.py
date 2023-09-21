import time

from .llm import LLM
from bardapi import BardCookies

class Bard(LLM):

    def __init__(self, token1: str, token2: str):
        self.__client = BardCookies({
            "__Secure-1PSID": token1,
            "__Secure-1PSIDTS": token2
        })

    def chat(self, message: str) -> str:
        time.sleep(10)
        return self.__client.get_answer(message)["content"]

    def reset(self):
        pass