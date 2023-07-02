import typing
from abc import ABC, abstractmethod

from lib.rl.environment import Environment

S = typing.TypeVar("S")
A = typing.TypeVar("A")


class Agent(ABC, typing.Generic[S, A]):

	def __init__(self):
		self.__environment = None

	def _get_environment(self) -> Environment[S, A]:
		if self.__environment is None:
			raise Exception("Environment Not Set.")
		return self.__environment

	def set_environment(self, environment: Environment[S, A]):
		self.__environment = environment

	def _is_episode_over(self, state: S) -> bool:
		return self._get_environment().is_episode_over(state)

	@abstractmethod
	def _policy(self, state: S) -> A:
		pass

	def perform_timestep(self):
		state = self._get_environment().get_state()
		action = self._policy(state)
		return self._get_environment().do(action)

	def perform_episode(self):
		while not self._get_environment().is_episode_over():
			self.perform_timestep()

	def loop(self):
		if self._get_environment().is_episodic():
			while True:
				self.perform_episode()
				self._get_environment().reset()
		else:
			while True:
				self.perform_timestep()
