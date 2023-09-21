import json
import typing
from lib.network.requests import Request


class CreateRequest(Request):

	def __init__(
			self,
			model_id: str,
			params: typing.Dict
	):
		super().__init__(
			url="/request/new",
			post_data=json.dumps({
				"params": params,
				"model": model_id
			}),
			method=Request.Method.POST
		)

	def deserialize_object(self, response) -> object:
		return response["request_id"]


class FetchResponseRequest(Request):

	def __init__(
			self,
			request_id: str
	):
		super().__init__(
			url=f"/request/fetch/{request_id}",
			method=Request.Method.GET
		)

	def _filter_response(self, response):
		return response["response"]
