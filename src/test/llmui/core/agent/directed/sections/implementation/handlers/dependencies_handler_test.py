import unittest

from llmui.core.agent.directed.sections.implementation.handlers.dependencies_handler import DependenciesHandler, \
	DependenciesArgs
from llmui.core.environment import LLMUIState, LLMUIEnvironment
from llmui.di import LLMProviders


class DependenciesHandlerTest(unittest.TestCase):


	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file="/home/abreham/Projects/TeamProjects/LLM-UI/temp/projects/orbit/environ.json"
		)
		handler = DependenciesHandler(LLMProviders.provide_console_llm())
		handler._handle(
			environment.state,
			DependenciesArgs(
				descriptions={
					"orbit-website/index.html": "The index.html file is a basic HTML file that serves as the entry point for a web application. It sets the document type, specifies the language, includes the necessary meta tags for character encoding and viewport settings, sets the favicon, and defines the title of the web page. The main content of the file includes a div element with the id \"app\" and a script tag that loads a TypeScript file named \"main.ts\" as a module.",
					"orbit-website/src/App.vue": "The given file, `App.vue`, is a Vue.js component file written in TypeScript. It imports the `RouterView` component from the `vue-router` package and uses it within the template section. This component is responsible for rendering the views based on the current route. The file also includes a scoped style tag for component-specific styling. The purpose of this file is to serve as the main entry point for the application and to provide the routing configuration for rendering different views.",
					"orbit-website/src/components/Home.vue": "The Home.vue file is a Vue3 single-file component that represents the home page of a website. It includes HTML template markup with headings, paragraphs, a list, and buttons. It uses TypeScript and the vue-router library for routing functionality. The main purpose of this file is to display information about the company \"Orbit\" and its services, provide a button to contact them, and a link to navigate to the \"About\" page.",
					"orbit-website/src/components/About.vue": "The file \"About.vue\" is a Vue.js single-file component that represents the About page of a website or application. It contains a template with headings, paragraphs, and lists to display information about the mission, vision, values, history, and team members of a company or organization. The script setup section defines variables for storing data related to the organization's mission, vision, values, history, and team members. The styling section contains scoped CSS rules for customizing the appearance of the component.",
					"orbit-website/src/components": "The \"orbit-website/src/components\" folder contains Vue.js single-file components that are used in the Orbit website project. These components serve as building blocks for different sections and pages of the website. The folder aids in organizing and managing the components of the website, enabling efficient development and maintenance of the UI elements and functionality.",
					"orbit-website/src/router/index.ts": "The file `index.ts` is a TypeScript module that imports dependencies from `vue-router` library and defines routes for a Vue.js application. It creates a router instance using the `createRouter` function and sets up two routes: one for the home page and one for the about page. The router is then exported as the default export from the module. The purpose of this file is to configure the routes for the application's navigation.",
					"orbit-website/src/router": "The `orbit-website/src/router` is a directory that contains the files responsible for managing the routing functionality of the Orbit website. It is responsible for defining and configuring the routes that the website's pages will use for navigation.",
					"orbit-website/src/views": "The \"orbit-website/src/views\" directory is likely a part of a web development project. It is responsible for storing the views of the website, which are templates or pages that are rendered and displayed to the users. The views directory is generally where the front-end components, such as HTML, CSS, and JavaScript files, are organized and stored for different pages or sections of the website.",
					"orbit-website/src/main.ts": "The main.ts file imports the main.css file, the createApp function from the Vue library, and the App.vue component. It also imports and uses a router. The purpose of this file is to create and mount a Vue app to the '#app' element in the HTML document.",
					"orbit-website/src": "The \"orbit-website/src\" directory serves as the source code directory for the Orbit website project. It contains various folders and files that are essential for building and running the website. This directory serves as the central location for organizing and managing the project's source code, including Vue.js components, routing configuration, views, and other related files. It plays a crucial role in facilitating efficient development, maintenance, and deployment of the Orbit website.",
					"orbit-website": "The \"orbit-website\" folder serves as the root directory for the Orbit website project. It contains various files and subdirectories that are essential for developing and deploying the website. This folder acts as the central hub for organizing and managing the project's source code, configuration files, dependencies (stored in the \"node_modules\" directory), and other related assets. It provides a structured environment for building and running the website, enabling efficient development and deployment processes."
				},
				ignored_files=[
					"orbit-website/.vscode",
					"orbit-website/node_modules",
					"orbit-website/public",
					"orbit-website/src/assets",
					"orbit-website/package-lock.json",
					"orbit-website/package.json",
					"orbit-website/README.md",
					"orbit-website/.gitignore",
					"orbit-website/env.d.ts",
					"orbit-website/.eslintrc.cjs",
					"orbit-website/vite.config.ts",
					"orbit-website/tsconfig.node.json",
					"orbit-website/tsconfig.app.json",
					"orbit-website/tsconfig.json"
				],
				files_tasks={
					"orbit-website/src/App.vue": "Modify the template in the 'App.vue' file to include a <router-view> element for rendering the Services Page.",
					# "orbit-website/src/components/Services.vue": "Create a new file named 'Services.vue' in the 'components' folder. Implement the HTML structure for the Services Page in the template section of the component file. Apply styling to the services cards, giving them a pill-like shape with high border radius in the style section. Implement the carousel for case studies with curved edges in the template section.",
					# "orbit-website/src/router/index.ts": "Update the router configuration in the 'index.ts' file to include a new route for the Services Page. Define a route path (e.g., '/services') and map it to the 'Services' component created in step 1."
				}
			)
		)

		self.assertIsNotNone(handler.get_internal_state().dependencies)
