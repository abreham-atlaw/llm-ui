import unittest

from llmui.config import ENVIRON_PATH
from llmui.core.agent.directed.sections.debug.executors.cause_executor import CauseExecutor
from llmui.core.environment import LLMUIEnvironment
from llmui.di import LLMProviders


class CauseExecutorTest(unittest.TestCase):

	def test_functionality(self):
		environment = LLMUIEnvironment(
			environ_file=ENVIRON_PATH
		)

		executor = CauseExecutor(LLMProviders.provide_default_llm())
		cause = executor((
			"""
Error: AxiosError: Request failed with status code 404


Stacktrace:
settle node_modules/axios/lib/core/settle.js:19:12
XMLHttpRequest.onloadend node_modules/axios/lib/adapters/xhr.js:111:7
XMLHttpRequest.invokeTheCallbackFunction node_modules/jsdom/lib/jsdom/living/generated/EventHandlerNonNull.js:14:28
XMLHttpRequest.<anonymous> node_modules/jsdom/lib/jsdom/living/helpers/create-event-accessor.js:35:32
innerInvokeEventListeners node_modules/jsdom/lib/jsdom/living/events/EventTarget-impl.js:350:25
invokeEventListeners node_modules/jsdom/lib/jsdom/living/events/EventTarget-impl.js:286:3
XMLHttpRequestImpl._dispatch node_modules/jsdom/lib/jsdom/living/events/EventTarget-impl.js:233:9
fireAnEvent node_modules/jsdom/lib/jsdom/living/helpers/events.js:18:36
Request.<anonymous> node_modules/jsdom/lib/jsdom/living/xhr/XMLHttpRequest-impl.js:891:5
Request.emit node:events:549:35


Extra Information:
 Serialized Error:
Code: 'ERR_BAD_REQUEST'
Config:
baseURL: 'http://172.17.0.1:5000/'
url: 'blog/undefined'
method: 'get'
status: 404
statusText: 'NOT FOUND'
response: '<!doctype html>\n<html lang=en>\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>\n'
Request:
baseURL: 'http://172.17.0.1:5000/'
url: 'blog/undefined'
method: 'get'
status: 404
statusText: 'NOT FOUND'
response: '<!doctype html>\n<html lang=en>\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>\n'
""",
			"BlogPost Repository Test > Get BlogPost Test",
			"src/tests/unit/apps/core/data/BlogPostRepositoryTest.spec.ts",
			[
				"src/apps/core/data/repositories/BlogPostRepository.ts",
				"src/apps/core/data/models/BlogPost.ts"
			],
			environment.state.read_content
		))

		self.assertIsNotNone(cause)
