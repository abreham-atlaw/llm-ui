from dataclasses import dataclass

import docker
from datetime import datetime

from .runner import Runner


class DockerRunner(Runner):

	def __init__(self):
		self.__client = docker.from_env()

	@staticmethod
	def _generate_name() -> str:
		return f"{datetime.now().timestamp()}"

	def __build_image(self, path: str) -> str:
		build_name = self._generate_name()
		self.__client.images.build(
			path=path,
			tag=build_name
		)
		return build_name

	def run(self, path: str) -> str:
		try:
			name = self.__build_image(path)
			return self.__client.containers.run(name)
		except Exception as ex:
			return str(ex)
