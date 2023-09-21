import unittest

from llmui.core.agent.directed_agent.handlers import InitHandler
from llmui.core.agent.directed_agent.handlers.handler import HandlerContext
from llmui.core.agent.directed_agent.stage import Stage
from llmui.core.agent.directed_agent.state import InternalState
from llmui.core.environment import LLMUIState
from llmui.di import LLMProviders


class InitHandlerTest(unittest.TestCase):
	APP_DESCRIPTION = """
Endpoints:
	/todos/ - Get all todos.
	/todos/create/ - Create a new todo.
	/todos/<id>/ - Get a todo by ID.
	/todos/<id>/update/ - Update a todo by ID.
	/todos/<id>/delete/ - Delete a todo by ID.

Description: This app will allow users to create, read, update, and delete todos. The todos will be stored in a 
database. The endpoints will be used to interact with the database. The /todos/ endpoint will return a list of all 
todos. The /todos/create/ endpoint will create a new todo. The /todos/<id>/ endpoint will return a todo by ID. The 
/todos/<id>/update/ endpoint will update a todo by ID. The /todos/<id>/delete/ endpoint will delete a todo by ID. The 
<id> in the endpoints is the ID of the todo. The ID is a unique identifier for each todo.
The app will also need to have a way for users to authenticate and authorize themselves to access the endpoints. 
This can be done using Django's built-in authentication system.

It'll be using the following file structure:
todo_app/
	__init__.py
	settings.py
	urls.py
	wsgi.py
	manage.py
	apps/
		todo/
			__init__.py
			models.py
			admin.py
			views.py
			templates/
				todo/
					index.html
"""

	def test_functionality(self):

		handler = InitHandler(LLMProviders.provide_default_llm())
		internal_state = InternalState(None, None, None, None)
		state = LLMUIState(
			action_stack=[],
			output="",
			read_content=lambda file: None
		)
		context = HandlerContext(
			project_description=self.APP_DESCRIPTION
		)
		handler.handle(
			Stage.INIT,
			parent_state=internal_state,
			state=state,
			context=context
		)
		self.assertIsInstance(internal_state.files, list)
