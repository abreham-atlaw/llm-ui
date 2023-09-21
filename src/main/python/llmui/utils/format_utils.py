import os
import re

class FormatUtils:

	@staticmethod
	def tree(path) -> str:
		tree_structure = ""
		if not os.path.isdir(path):
			return "Invalid directory path."

		for root, dirs, files in os.walk(path):
			level = root.replace(path, "").count(os.sep)
			indent = "|   " * level

			dir_name = os.path.basename(root)
			if dir_name == os.path.basename(path):
				dir_name = "."
			tree_structure += f"{indent}|--{dir_name}/\n"

			for file in files:
				sub_indent = "|   " * (level + 1)
				tree_structure += f"{sub_indent}|--{file}\n"

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
