import typing

from .client import GAIClient
from .query_client import QueryClient


class Llama2Client(QueryClient):

	def __init__(self, url: str):
		super().__init__(url, model_id="llama2")

	def _deserialize_response(self, response: typing.Any) -> typing.Any:
		return response
