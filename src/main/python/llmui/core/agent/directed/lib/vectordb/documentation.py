import os
import typing

from lib.vectordb.vector_db import VectorDB
from llmui.di.utils_providers import UtilsProviders


class Documentation:

	def __init__(self, docs_path: str, docs_ext=""):
		self.__db: VectorDB = UtilsProviders.provide_vectordb()
		print(f"[+]Documentation: Loading docs({docs_path})...")
		self.__db.add_files([
			os.path.join(docs_path, file)
			for file in os.listdir(docs_path)
			if file.endswith(docs_ext)
		])

	def search(self, query: str, num_results: int = 5) -> typing.List[str]:
		return self.__db.query(query, num_results)
