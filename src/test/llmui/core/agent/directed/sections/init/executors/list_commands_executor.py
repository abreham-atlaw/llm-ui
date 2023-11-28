import unittest

from llmui.core.agent.directed.sections.init.executors.list_commands_executor import ListCommandsExecutor
from llmui.di import LLMProviders


class ListCommandsExecutorTest(unittest.TestCase):

	def test_functionality(self):

		executor = ListCommandsExecutor(LLMProviders.provide_console_llm())
		output = executor((
			f"""
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

""",
			["Vue3", "OptionsAPI", "Typescript", "Ubuntu"]
		))

		self.assertIsNotNone(output)

