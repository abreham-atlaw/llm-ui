import json
import unittest

from llmui.config import EXTRAS_SAVE_PATH
from llmui.core.agent.directed.lib.vectordb.documentation import Documentation


class DocumentationTest(unittest.TestCase):

	def test_filter_for_task(self):
		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)
		documentation = Documentation(extras["docs"])

		result = documentation.search("""
**Task:**

**Objective:** Create a model for `Product` in the `core` app.

**App Structure:**

- The `core` app is located in the `apps` directory of the project.
- Within the `core` app, there are separate folders for models, serializers, views, and URLs.

**Model Requirements:**

- Create a model named `Product` in the `models` folder of the `core` app.
- The `Product` model should have the following fields:
  - `id`: A UUID field serving as the primary key.
  - `name`: A `CharField` to store the product name.
  - `image`: A `URLField` to store the product image URL.
  - `description`: A `TextField` to store the product description.
  - `price`: A `DecimalField` to store the product price.
  - `is_active`: A `BooleanField` to indicate whether the product is active or not (default value: `True`).

**Additional Information:**

- Follow the project's naming conventions and coding standards.
- Ensure that the `Product` model is imported in the `__init__.py` file of the `core` app's `models` folder.
- The `Product` model should be used in the `core` app's views and serializers as needed.

**Project Documentation:**

- Refer to the provided documentation for guidance on creating models, serializers, views, and URLs.
- The documentation emphasizes the importance of organizing components within the project structure.
- Models, views, and serializers should be stored in their respective folders and not consolidated into a single file.

**Deliverables:**

- A `Product` model created in the `core` app's `models` folder with the specified fields and relationships.
- The `Product` model imported in the `__init__.py` file of the `core` app's `models` folder.
- Unit tests to ensure the functionality of the `Product` model.
""")
		self.assertIsNotNone(result)
