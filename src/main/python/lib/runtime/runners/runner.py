from abc import ABC, abstractmethod


class Runner(ABC):

	@abstractmethod
	def run(self, path: str) -> str:
		pass

