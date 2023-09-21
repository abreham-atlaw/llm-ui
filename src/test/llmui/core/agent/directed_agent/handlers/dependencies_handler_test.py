import unittest

from llmui.core.agent.directed_agent.handlers import DependenciesHandler
from llmui.core.agent.directed_agent.handlers.handler import HandlerContext
from llmui.core.agent.directed_agent.stage import Stage
from llmui.core.agent.directed_agent.state import InternalState
from llmui.core.environment import LLMUIState
from llmui.di import LLMProviders


class DependenciesHandlerTest(unittest.TestCase):

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

		handler = DependenciesHandler(LLMProviders.provide_default_llm())
		internal_state = InternalState(
			required_files=['todo_app/__init__.py', 'todo_app/settings.py', 'todo_app/urls.py', 'todo_app/wsgi.py', 'todo_app/manage.py', 'todo_app/apps/todo/__init__.py', 'todo_app/apps/todo/models.py', 'todo_app/apps/todo/admin.py', 'todo_app/apps/todo/views.py', 'todo_app/apps/todo/templates/todo/index.html'],
			descriptions={'todo_app/__init__.py': 'This file is typically an empty file and serves as a marker to Python that the directory should be considered a Python package.', 'todo_app/settings.py': 'This file contains the configuration settings for your Django project. It includes database settings, middleware, installed apps, and other project-specific settings.', 'todo_app/urls.py': 'This file defines the URL patterns for your Django project. You will map the endpoints to their corresponding views in this file.', 'todo_app/wsgi.py': 'This file is used to run your Django project as a WSGI application. It provides the entry point for your web server to interact with your Django app.', 'todo_app/manage.py': 'This is a command-line utility that allows you to interact with various Django commands. You can use it to run development servers, create database tables, and perform other administrative tasks.', 'todo_app/apps/todo/__init__.py': 'Similar to the previous __init__.py file, this file marks the todo directory as a Python package.', 'todo_app/apps/todo/models.py': 'This file defines the database models for your app. You will need to create a Todo model with fields like title, description, and completed to represent the todos.', 'todo_app/apps/todo/admin.py': 'This file is used to register your models with the Django admin interface. It allows you to manage the todos through the admin panel.', 'todo_app/apps/todo/views.py': 'This file contains the view functions that handle HTTP requests and return HTTP responses. You will implement the logic for each endpoint in this file.', 'todo_app/apps/todo/templates/todo/index.html': "This file is an HTML template that defines the structure and layout of the todo app's index page. You can customize it to display the list of todos."},
			implemented_files=None,
			dependencies=None
		)
		state = LLMUIState(
			action_stack=[],
			output="",
			read_content=lambda file: None
		)
		context = HandlerContext(
			project_description=self.APP_DESCRIPTION
		)
		handler.handle(
			Stage.LISTED,
			parent_state=internal_state,
			state=state,
			context=context
		)
		self.assertIsInstance(internal_state.dependencies, dict)


