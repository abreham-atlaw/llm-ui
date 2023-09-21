from lib.gai_client import Llama2Client
from llmui.config import GAI_URL


class UtilsProviders:

	@staticmethod
	def provide_llama2_client() -> Llama2Client:
		return Llama2Client(GAI_URL)
