import unittest

from llmui.core.agent.directed.sections.implementation.executors.order_tasks_executor import OrderTasksExecutor
from llmui.di import LLMProviders


class OrderTasksExecutorTest(unittest.TestCase):

	def test_functionality(self):

		executor = OrderTasksExecutor(LLMProviders.provide_console_llm())
		order = executor(
			{
				"orbit-website/src/components/Services.vue": "Create a new file named 'Services.vue' in the 'components' folder. Implement the HTML structure for the Services Page in the template section of the component file. Apply styling to the services cards, giving them a pill-like shape with high border radius in the style section. Implement the carousel for case studies with curved edges in the template section.",
				"orbit-website/src/App.vue": "Modify the template in the 'App.vue' file to include a <router-view> element for rendering the Services Page.",
				"orbit-website/src/router/index.ts": "Update the router configuration in the 'index.ts' file to include a new route for the Services Page. Define a route path (e.g., '/services') and map it to the 'Services' component created in step 1."
			}
		)

		self.assertIsNotNone(order)

