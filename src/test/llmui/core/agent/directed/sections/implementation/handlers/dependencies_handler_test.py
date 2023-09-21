import unittest

from llmui.core.agent.directed.sections.implementation.handlers.dependencies_handler import DependenciesHandler, \
	DependenciesArgs
from llmui.core.environment import LLMUIState
from llmui.di import LLMProviders


class DependenciesHandlerTest(unittest.TestCase):


	def test_functionality(self):
		state = LLMUIState(
			action_stack=[],
			output="",
			read_content=None,
			root_path=".",
			project_description="""
App Name: Foodie Friends

Description: Foodie Friends is a social food delivery app that connects users with local restaurants and food vendors. Users can browse a wide range of culinary delights, read reviews from other users, and order food for delivery or pick-up. The app also features a community forum where users can share food recommendations, ask questions, and connect with other foodies.

Required Pages:

	Home page: This is the main page of the app where users can browse restaurants and food vendors. The page should 
	also display popular dishes, recent orders, and upcoming events. Restaurant page: This page provides detailed 
	information about a specific restaurant, such as its menu, hours of operation, and contact information. Users can 
	also read reviews from other users and place an order for delivery or pick-up. Food page: This page provides 
	detailed information about a specific dish, such as its ingredients, nutritional information, and reviews from 
	other users. Cart page: This page allows users to view the items they have added to their cart and checkout. 
	Profile page: This page allows users to create a profile, edit their account settings, and view their order 
	history. Community forum: This page allows users to connect with other foodies, share food recommendations, 
	and ask questions.

Additional Features:

	The app can be integrated with a payment processing system to allow users to pay for their orders securely.
	The app can be integrated with a geolocation service to allow users to find restaurants and food vendors near them.
	The app can be integrated with a messaging service to allow users to communicate with restaurants and food vendors.
	The app can be used to create and manage loyalty programs.

This is just a basic idea for a social food delivery app. There are many other features that could be added to make 
the app more comprehensive and user-friendly.

It'll use the flutter with the following folder structure.

lib
├── apps
│ ├── auth
│ │ ├── application
│ │ │ ├── blocs
│ │ │ ├── events
│ │ │ ├── forms
│ │ │ └── states
│ │ ├── data
│ │ │ ├── models
│ │ │ ├── repositories
│ │ │ └── requests
│ │ └── presentation
│ │ ├── screens
│ │ └── widgets
│ └── core
│ │ ├── application
│ │ │ ├── blocs
│ │ │ ├── events
│ │ │ ├── forms
│ │ │ └── states
│ │ ├── data
│ │ │ ├── models
│ │ │ ├── repositories
│ │ │ └── requests
│ │ └── presentation
│ │ │ ├── screens
│ │ │ └── widgets
├── configs
│ ├── content_configs.dart
│ ├── data_configs.dart
│ └── ui_configs.dart
├── main.dart
└── router.dart

"""
		)

		handler = DependenciesHandler(LLMProviders.provide_default_llm())
		handler.handle(
			state,
			DependenciesArgs(
				files=[
					"lib/apps/auth/application/blocs/AuthBloc.dart",
					"lib/apps/auth/application/events/AuthEvent.dart",
					"lib/apps/auth/application/forms/AuthForms.dart",
					"lib/apps/auth/application/states/AuthState.dart",
					"lib/apps/auth/data/models/AuthModels.dart",
					"lib/apps/auth/data/repositories/AuthRepository.dart"
				],
				descriptions={'lib/apps/auth/application/blocs/AuthBloc.dart': 'This file defines the AuthBloc class, which manages the authentication state of the app.', 'lib/apps/auth/application/events/AuthEvent.dart': 'This file defines the AuthEvent class, which represents the events that can be emitted by the AuthBloc.', 'lib/apps/auth/application/forms/AuthForms.dart': 'This file contains form classes related to authentication, such as login and registration forms.', 'lib/apps/auth/application/states/AuthState.dart': 'This file defines the AuthState class, which represents the different authentication states of the app.', 'lib/apps/auth/data/models/AuthModels.dart': 'This file contains data models related to authentication, such as user models.', 'lib/apps/auth/data/repositories/AuthRepository.dart': 'This file defines the AuthRepository class, which handles data operations related to authentication, such as login and registration.', 'lib/apps/auth/data/requests/AuthRequests.dart': 'This file contains request classes related to authentication, such as login and registration requests.', 'lib/apps/auth/presentation/screens/AuthScreens.dart': 'This file contains the authentication screens, such as the login and registration screens.', 'lib/apps/auth/presentation/widgets/AuthWidgets.dart': 'This file contains widgets related to authentication, such as login and registration form widgets.', 'lib/apps/core/application/blocs/CoreBloc.dart': 'This file defines the CoreBloc class, which manages the core state of the app, including navigation and global app state.', 'lib/apps/core/application/events/CoreEvent.dart': 'This file defines the CoreEvent class, which represents the events that can be emitted by the CoreBloc.', 'lib/apps/core/application/forms/CoreForms.dart': 'This file contains form classes related to core functionality, such as search forms.', 'lib/apps/core/application/states/CoreState.dart': 'This file defines the CoreState class, which represents the different core states of the app.', 'lib/apps/core/data/models/CoreModels.dart': 'This file contains data models related to core functionality, such as location models.', 'lib/apps/core/data/repositories/CoreRepository.dart': 'This file defines the CoreRepository class, which handles data operations related to core functionality, such as fetching nearby restaurants.', 'lib/apps/core/data/requests/CoreRequests.dart': 'This file contains request classes related to core functionality, such as location search requests.', 'lib/apps/core/presentation/screens/CoreScreens.dart': 'This file contains the core screens, such as the home screen and restaurant screen.', 'lib/apps/core/presentation/widgets/CoreWidgets.dart': 'This file contains widgets related to core functionality, such as restaurant list and menu widgets.', 'lib/configs/content_configs.dart': 'This file contains content configurations for the app, such as text styles and localization settings.', 'lib/configs/data_configs.dart': 'This file contains data configurations for the app, such as API endpoints and database settings.', 'lib/configs/ui_configs.dart': 'This file contains UI configurations for the app, such as theme settings and color schemes.', 'lib/main.dart': 'This is the entry point of the app and contains the main function.', 'lib/router.dart': "This file defines the app's routing configuration, including the mapping of routes to screens."}
			)
		)

		self.assertIsNotNone(handler.get_internal_state().dependencies)
