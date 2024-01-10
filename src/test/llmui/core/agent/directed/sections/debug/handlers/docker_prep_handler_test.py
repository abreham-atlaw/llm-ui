import unittest

from llmui.core.agent.directed.sections.debug.handlers.docker_prep_handler import DockerPrepHandler
from llmui.core.environment import LLMUIState
from llmui.di import LLMProviders


class DockerPrepHandlerTest(unittest.TestCase):

	def test_functionality(self):
		state = LLMUIState(
			action_stack=[],
			output="",
			read_content=None,
			root_path="/home/abreham/Projects/TeamProjects/LLM-UI/temp/run",
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

		handler = DockerPrepHandler(LLMProviders.provide_console_llm())
		action = handler._handle(
			state,
			None
		)

		self.assertTrue(handler.get_internal_state().complete)
