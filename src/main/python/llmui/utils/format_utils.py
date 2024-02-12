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

	@staticmethod
	def filter_files(files, ignored_files):
		filtered_files = []
		for file in files:
			if not any(file.startswith(ignored_file) for ignored_file in ignored_files):
				filtered_files.append(file)
		return filtered_files

	@staticmethod
	def generate_files_list(files_list: typing.List[str], ignored_files: typing.List[str] = None, description: typing.Dict[str, str] = None) -> str:

		if ignored_files is not None:
			files_list = FormatUtils.filter_files(files_list, ignored_files=ignored_files)
		return "\n".join([
			f"{i+1}. {file}{f':{description.get(file)}' if description.get(file) is not None else ''}"
			for i, file in enumerate(files_list)
		])

	@staticmethod
	def extract_list_from_json_string(text) -> typing.List[str]:
		output = FormatUtils.extract_json_from_string(text)
		tasks = [output[key] for key in sorted(output, key=lambda k: int(k))]
		return tasks

	@staticmethod
	def format_docs(docs: typing.List[str]) -> str:
		return "<<DOCUMENTATION>>\n\n\n"+"\n\n".join(docs)+"\n\n\n<</DOCUMENTATION>>"

	@staticmethod
	def format_content(content: str) -> str:
		return f"""
```
{content.strip()}
```
"""
