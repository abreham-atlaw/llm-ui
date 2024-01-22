import typing
from abc import ABC, abstractmethod


class VectorDB(ABC):

	def add_files(self, files: typing.List[str]):
		documents = []
		for file in files:
			with open(file, "r") as fs:
				documents.append(fs.read())

		self.add(documents)

	def add(self, documents: typing.List[str]):
		self._add(documents)

	@abstractmethod
	def _add(self, documents: typing.List[str]):
		pass

	@abstractmethod
	def query(self, query: str, num_results=5) -> typing.List[str]:
		pass
