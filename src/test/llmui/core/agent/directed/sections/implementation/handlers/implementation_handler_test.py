import unittest
import os

from llmui.core.agent.directed.sections.common.models import ProjectInfo
from llmui.core.agent.directed.sections.implementation.executors.list_files_executor import ListFilesExecutor
from llmui.core.agent.directed.sections.implementation.handlers.implementation_handler import ImplementationHandler, \
	ImplementationHandlerArgs
from llmui.core.agent.directed.sections.implementation.states.implementation_state import ImplementationStage
from llmui.core.environment import LLMUIState
from llmui.di import LLMProviders


class ImplementationHandlerTest(unittest.TestCase):

	ROOT_PATH = "/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit"

	def read_content(self, file) -> str:
		file = os.path.join(self.ROOT_PATH, file)
		if not os.path.exists(file):
			return ""
		with open(file, "r") as file:
			content = file.read()
			return content

	def __write(self, file_path: str, content: str):
		self.__create_dir(file_path)
		with open(file_path, "w") as file:
			print(content, file=file)

	@staticmethod
	def __create_dir(path: str):
		os.makedirs(os.path.dirname(path), exist_ok=True)

	def test_functionality(self):
		state = LLMUIState(
			action_stack=[],
			outputs=[],
			read_content=self.read_content,
			root_path=self.ROOT_PATH,
			project_description="""
Website Description:
The Orbit website will serve as a digital platform that showcases the company's expertise in software development. It will highlight the company's services, projects, and team members. The website will also provide a way for potential clients to get in touch with the company.

Pages Required:

1. Home Page:
	- A brief introduction to the company
   - Highlight of key services
   - A call-to-action (CTA) to contact the company or learn more about its services

2. About Us Page:
   - Detailed information about the company, its mission, vision, and values
   - History of the company
   - Team member profiles

3. Services Page:
   - Detailed descriptions of the services offered
   - Case studies or examples of past projects
   - CTAs to request a quote or get more information

4. Projects Page:
   - Showcase of completed projects
   - Testimonials from clients
   - Each project could have its own page with more details and a case study

5. Blog Page:
   - Regularly updated articles about industry trends, company news, etc.
   - Each blog post could have its own page

6. Contact Us Page:
   - Contact form for potential clients to get in touch
   - Company contact information (email, phone number, address)
   - Embedded map showing the company's location

7. Careers Page:
   - List of current job openings
   - Information about the company culture
   - Form to submit applications

"""
		)
		handler = ImplementationHandler.load_handler(
			"/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/web.json",
			LLMProviders.provide_default_llm()
		)
		# handlers = ImplementationHandler(LLMProviders.provide_default_llm())
		while not handler.get_internal_state().stage == ImplementationStage.done:
			action = handler._handle(
				state,
				ImplementationHandlerArgs(
					ListFilesHandler.Mode.implement,
					{},
					project_info=ProjectInfo(
						description=state.project_description,
						tech_stack=["Vue3", "OptionsAPI", "Typescript"]
					)
				)
			)
			if action is not None:
				self.__write(os.path.join(self.ROOT_PATH, action.args[0]), action.args[1])
			handler.save("/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/web.json")
		self.assertTrue(handler.get_internal_state().stage)

	def test_test_functionality(self):
		state = LLMUIState(
			action_stack=[],
			outputs=[],
			read_content=self.read_content,
			root_path=self.ROOT_PATH,
			project_description="""
The app is a flask rest-api backend for a simple todo list.
The app will have the following features:

	Users can add new todo items.
	Users can edit existing todo items.
	Users can delete todo items.
	Users can mark todo items as completed.
	Users can view a list of all their todo items.

The following are the required endpoints for the app:

	/: This is the home page of the app. It will display a list of all the todo items for the current user.
	/add: This endpoint allows users to add new todo items.
	/edit/<int:todo_id>: This endpoint allows users to edit existing todo items. The todo_id parameter is the ID of the todo item to be edited.
	/delete/<int:todo_id>: This endpoint allows users to delete existing todo items. The todo_id parameter is the ID of the todo item to be deleted.
	/complete/<int:todo_id>: This endpoint allows users to mark a todo item as completed. The todo_id parameter is the ID of the todo item to be marked as completed.
"""
		)
		handler = ImplementationHandler(LLMProviders.provide_default_llm())
		# handlers = ImplementationHandler.load_handler("/home/abreham/Projects/TeamProjects/LLM-UI/temp/config.json", LLMProviders.provide_default_llm())
		while not handler.get_internal_state().stage == ImplementationStage.done:

			action = handler._handle(
				state,
				ImplementationHandlerArgs(
					ListFilesHandler.Mode.test,
					{
						"app.py": "This file sets up the Flask application and handles the routing for the various endpoints.",
						"models.py": "This file contains the definition of the Todo model, which represents a todo item in the database.",
						"routes.py": "This file defines the routes for the various endpoints in the app, including adding, editing, deleting, completing, and viewing todo items.",
						"controllers.py": "This file contains the controller functions that handle the logic for each endpoint.",
						"database.py": "This file manages the database connection and provides functions for interacting with the Todo model.",
						"serializers.py": "This file defines the serializers for converting Todo objects to JSON format and vice versa.",
						"requirements.txt": "This file lists the dependencies required for the app to run, including Flask and any other necessary libraries.",
						"README.md": "This file provides documentation and instructions on how to set up and use the app."
					},
					project_info=ProjectInfo(
						description=state.project_description,
						tech_stack=["python, flask, unittest"]
					)
				)
			)
			if action is not None:
				self.__write(os.path.join(self.ROOT_PATH, action.args[0]), action.args[1])
			handler.save("/home/abreham/Projects/TeamProjects/LLM-UI/temp/config.json")
		self.assertTrue(handler.get_internal_state().stage)
