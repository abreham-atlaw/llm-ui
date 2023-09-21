import typing
from abc import ABC

import requests
from urllib.parse import urlparse
import os

from .client import GAIClient


class FileBasedClient(GAIClient, ABC):

	def __init__(self, *args, out_path="./", **kwargs):
		super().__init__(*args, **kwargs)
		self.__out_path = os.path.abspath(out_path)

	@staticmethod
	def __download_file(url, directory_path):
		print(f"[+]Downloading {url}...")
		parsed_url = urlparse(url)
		filename = os.path.basename(parsed_url.path)

		file_path = os.path.join(directory_path, filename)

		response = requests.get(url)
		response.raise_for_status()

		with open(file_path, 'wb') as file:
			file.write(response.content)

		return file_path

	def _deserialize_response(self, response: str) -> str:
		return self.__download_file(response, self.__out_path)

