from dataclasses import dataclass

import docker
from datetime import datetime

from docker.errors import BuildError, ContainerError

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
			return str(self.__client.containers.run(name))
		except BuildError as e:
			message = ""
			for line in e.build_log:
				if 'stream' in line:
					message += line['stream'].strip()
			return message
		except ContainerError as e:
			return e.stderr.decode("utf-8")
		except Exception as ex:
			return str(ex)
