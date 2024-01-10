import typing

import unittest

from llmui.core.agent.directed_agent.handlers.implementation_handler import ImplementationHandler
from llmui.core.agent.directed_agent.stage import Stage
from llmui.core.agent.directed_agent.state import InternalState
from llmui.di import LLMProviders


class ImplementationHandlerTest(unittest.TestCase):

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
"""

	def test_functionality(self):
		handler = ImplementationHandler(LLMProviders.provide_default_llm())

		mock_state = LLMState
		mock_internal_state = InternalState(
			required_files=[
				'lib/apps/auth/application/blocs/AuthBloc.dart', 'lib/apps/auth/application/events/AuthEvent.dart',
				'lib/apps/auth/application/forms/AuthForm.dart', 'lib/apps/auth/application/states/AuthState.dart',
				'lib/apps/auth/data/models/User.dart', 'lib/apps/auth/data/repositories/AuthRepository.dart',
				'lib/apps/auth/data/requests/AuthRequest.dart', 'lib/apps/auth/presentation/screens/LoginScreen.dart',
				'lib/apps/auth/presentation/screens/RegistrationScreen.dart',
				'lib/apps/auth/presentation/widgets/AuthFormWidget.dart',
				'lib/apps/core/application/blocs/HomeBloc.dart',
				'lib/apps/core/application/events/HomeEvent.dart', 'lib/apps/core/application/forms/CartForm.dart',
				'lib/apps/core/application/states/HomeState.dart', 'lib/apps/core/data/models/Restaurant.dart',
				'lib/apps/core/data/repositories/RestaurantRepository.dart',
				'lib/apps/core/data/requests/OrderRequest.dart', 'lib/apps/core/presentation/screens/HomeScreen.dart',
				'lib/apps/core/presentation/screens/RestaurantScreen.dart',
				'lib/apps/core/presentation/screens/FoodScreen.dart',
				'lib/apps/core/presentation/screens/CartScreen.dart',
				'lib/apps/core/presentation/screens/ProfileScreen.dart',
				'lib/apps/core/presentation/screens/CommunityForumScreen.dart',
				'lib/apps/core/presentation/widgets/RestaurantCardWidget.dart',
				'lib/apps/core/presentation/widgets/FoodCardWidget.dart', 'lib/configs/content_configs.dart',
				'lib/configs/data_configs.dart',
				'lib/configs/ui_configs.dart',
				'lib/main.dart',
				'lib/router.dart'
			],
			dependencies={
				''
			}

		)

		handler._handle(Stage.DEPENDENCY_LISTED, )
