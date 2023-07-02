import typing
from typing import *
from abc import ABC, abstractmethod

from lib.utils.logger import Logger

S = TypeVar("S")
A = TypeVar("A")



class Environment(ABC, Generic[S, A]):

	def __init__(self, episodic=True):
		self.episodic = episodic

	@abstractmethod
	def _get_reward(self, state: S) -> float:
		pass

	def get_reward(self, state: S = None) -> float:
		if state is None:
			state = self.get_state()
		return self._get_reward(state)

	@abstractmethod
	def perform_action(self, action: A):
		pass

	@abstractmethod
	def render(self):
		pass

	@abstractmethod
	def update_ui(self):
		pass

	@abstractmethod
	def check_is_running(self) -> bool:
		pass

	@abstractmethod
	def is_action_valid(self, action: A, state: S) -> bool:
		pass

	@abstractmethod
	def get_state(self) -> S:
		pass

	@abstractmethod
	def _is_episode_over(self, state: S) -> bool:
		pass

	def is_episode_over(self, state: S = None) -> bool:
		if state is None:
			state = self.get_state()
		return self._is_episode_over(state)

	@Logger.logged_method
	def do(self, action: A) -> float:
		if not self.is_action_valid(action, self.get_state()):
			raise ActionNotValidException()
		self.perform_action(action)
		self.update_ui()
		return self.get_reward()

	def is_episodic(self) -> bool:
		return self.episodic

	def reset(self):
		self.start()

	def _initialize(self):
		self.render()

	def start(self):
		self._initialize()


class ActionNotValidException(Exception):
	pass
