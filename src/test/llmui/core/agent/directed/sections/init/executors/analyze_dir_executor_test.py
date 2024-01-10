import unittest

from llmui.core.agent.directed.sections.init.executors.analyze_dir_executor import AnalyzeDirExecutor
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders


class AnalyzeDirExecutorTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			cwd="/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/web",
			environ_file="/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/environ.json"
		)

		executor = AnalyzeDirExecutor(
			LLMProviders.provide_console_llm()
		)

		analysis = executor((
			environment.state.root_path,
			"orbit-website/src/views",
			{
				"orbit-website/src/views/AboutView.vue": """
The file "AboutView.vue" is a Vue.js single-file component that represents the view for the About page in a web application. It consists of a template section and a style section.

In the template section, there is a <div> element with a class of "about" that wraps around an <h1> heading element. This structure suggests that the content within the "about" class will be styled and positioned accordingly. The <h1> element displays the text "This is an about page" as the heading for the about page.

In the style section, there is a media query that targets devices with a minimum width of 1024 pixels. Within this media query, the ".about" class is defined with some specific styles. It sets the minimum height of the "about" section to 100 viewport height (vh) units, ensuring it takes up the full height of the screen. The "display" property is set to "flex", indicating that the child elements inside the "about" section can be positioned with flexbox. The "align-items" property is set to "center", which vertically aligns the contents of the "about" section.

Overall, this file serves as the representation of the About page view in a Vue.js application, defining the structure and styling for the content displayed on the page.
""",

				"orbit-website/src/views/HomeView.vue": """
The given file, "HomeView.vue", is a Vue single-file component written in TypeScript. It consists of a script section, a template section, and a main HTML structure.

In the script section, the "TheWelcome" component is imported from the "../components/TheWelcome.vue" file. This import allows the usage of the "TheWelcome" component within the template section of the file.

The template section contains the main HTML structure of the component. It consists of a single root element, <main>, which serves as the container for the component's content. Within this element, the <TheWelcome /> component is rendered. The usage of the self-closing syntax (<TheWelcome />) indicates that it is a child component within the template.

The purpose of this file is to define the structure and behavior of the "HomeView" component, which represents the home view or page of the application. It includes the rendering of the "TheWelcome" component, which is likely to display a welcome message or provide some introductory content to the user.

Overall, this file encapsulates the logic and presentation of the home view and integrates the "TheWelcome" component to provide a cohesive user interface for the application's home page.
"""
			}
		))

		self.assertIsNotNone(analysis)
