import typing
from abc import ABC, abstractmethod

from .requests import CreateRequest, FetchResponseRequest
from lib.network.client import NetworkApiClient


class GAIClient(NetworkApiClient, ABC):

	def __init__(self, url: str, model_id: str):
		super().__init__(url=url)
		self.__model_id = model_id

	@abstractmethod
	def _generate_params(self, *args, **kwargs) -> typing.Dict:
		pass

	@abstractmethod
	def _deserialize_response(self, response: typing.Any) -> typing.Any:
		pass

	def __get_response(self, request_id: str):
		print("[+]Waiting for response...")
		response = None
		while response is None:
			response = self.execute(
				FetchResponseRequest(
					request_id=request_id
				)
			)
		return response

	def generate(self, *args, **kwargs):
		params = self._generate_params(*args, **kwargs)
		request_id = self.execute(
			CreateRequest(
				model_id=self.__model_id,
				params=params
			)
		)

		response = self.__get_response(request_id)
		return  self._deserialize_response(response)

	def __call__(self, *args, **kwargs):
		return self.generate(*args, **kwargs)