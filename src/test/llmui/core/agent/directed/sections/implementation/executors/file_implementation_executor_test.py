import json
import unittest

from llmui.config import ENVIRON_PATH, EXTRAS_SAVE_PATH
from llmui.core.agent.directed.sections.implementation.executors.file_implementation_executor import \
	FileImplementationExecutor
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders


class FileImplementationExecutorTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		with open(EXTRAS_SAVE_PATH, "r") as file:
			extras = json.load(file)

		CONTEXT = """
Task: Create a file named Product.ts in the src/apps/core/data/models directory. Implement the Product model class with properties like id, name, and description.

To complete this task, you need to create a file named "Product.ts" in the "src/apps/core/data/models" directory. In this file, you will implement the Product model class with properties like id, name, and description. The Product model class should have the following structure:

```typescript
// src/apps/core/data/models/Product.ts
export default class Product {
    id: string;
    name: string;
    description: string;

    constructor({
        id, name, description
    }: {
        id: string,
        name: string,
        description: string
    }) {
        this.id = id;
        this.name = name;
        this.description = description;
    }
}
```

In this implementation, the Product model class has properties such as id, name, and description. The constructor ensures the initialization of these properties during object creation.

Please note that this implementation assumes that you have already set up the necessary project structure and have the required dependencies installed.
"""
		FILE = "src/apps/core/data/models/Product.ts"
		TASK = "Create a file named Product.ts in the src/apps/core/data/models directory. Implement the Product model class with properties like id, name, and description."
		DEPENDENCIES = []

		executor = FileImplementationExecutor(LLMProviders.provide_default_llm())

		content = executor((
			CONTEXT, extras["tech_stack"], environment.state.root_path,
			FILE, TASK, DEPENDENCIES, environment.state.read_content
		))

		self.assertIsNotNone(content)
