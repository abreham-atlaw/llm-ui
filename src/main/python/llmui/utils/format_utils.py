import json
import os
import re
import typing


class FormatUtils:

	@staticmethod
	def tree(path, level=0, excluded_files=[]) -> str:
		tree_structure = ""
		if not os.path.isdir(path):
			return "Invalid directory path."

		indent = "|   " * level
		dir_name = os.path.basename(path)
		if dir_name in excluded_files:
			return ""

		if level == 0:
			dir_name = "."
		tree_structure += f"{indent}|--{dir_name}/\n"

		for item in os.listdir(path):
			item_path = os.path.join(path, item)
			if os.path.isdir(item_path) and item not in excluded_files:
				tree_structure += FormatUtils.tree(item_path, level + 1, excluded_files)
			elif os.path.isfile(item_path) and item not in excluded_files:
				sub_indent = "|   " * (level + 1)
				tree_structure += f"{sub_indent}|--{item}\n"

		return tree_structure

	@staticmethod
	def extract_first_code_block(text) -> str:
		pattern = r"```(.+?)\n(.+?)```"
		match = re.search(pattern, text, re.DOTALL)
		if match:
			language = match.group(1)
			code = match.group(2)
			return code
		return ""

	@staticmethod
	def extract_json_from_string(text) -> typing.Dict:
		# Find the JSON within the string using regular expressions
		pattern = r'(?s)\{.*\}'
		match = re.search(pattern, text, re.DOTALL)

		if match:
			# Extract the JSON substring
			json_str = match.group(0)

			# Parse the JSON into a dictionary
			try:
				json_dict = json.loads(json_str)
				return json_dict
			except json.JSONDecodeError:
				pass

		raise Exception(f"Json Parse Error: {text}")
