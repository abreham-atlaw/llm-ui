from typing import *

import cattr
import json



class Serializer:

	def __init__(self, output_class):
		self.__output_class = output_class

	def serialize(self, data: object) -> Dict:
		return cattr.unstructure(data)

	def serialize_json(self, data: object):
		return json.dumps(self.serialize(data))

	def deserialize(self, json_: Dict) -> object:
		return cattr.structure(json_, self.__output_class)

	def deserialize_json(self, json_: str):
		return self.deserialize(json.loads(json_))
