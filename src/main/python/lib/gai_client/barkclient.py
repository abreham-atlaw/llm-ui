

from .file_based_client import FileBasedClient
from .query_client import QueryClient


class BarkClient(FileBasedClient, QueryClient):

	def __init__(self, *args, **kwargs):
		super().__init__(
			*args,
			model_id="bark",
			**kwargs
		)
