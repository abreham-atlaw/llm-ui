import typing
from abc import ABC

from .client import GAIClient


class QueryClient(GAIClient, ABC):

	def _generate_params(self, message: str) -> typing.Dict:
		return {
			"query": message
		}
