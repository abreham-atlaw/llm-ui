import typing

from lib.vectordb import VectorDB

import uuid

from chromadb import Client


class ChromaVectorDB(VectorDB):

	def __init__(self):
		super().__init__()
		self.__client = Client()
		self.__id = self.__generate_id()
		self.__collection = self.__client.create_collection(self.__id)

	@staticmethod
	def __generate_id() -> str:
		return uuid.uuid4().hex

	def _add(self, documents: typing.List[str]):
		self.__collection.add(
			documents=documents,
			ids=[self.__generate_id() for _ in documents]
		)

	def query(self, query: str, num_results=5) -> typing.List[str]:
		return self.__collection.query(
			query_texts=[query],
			n_results=num_results
		)["documents"][0]
