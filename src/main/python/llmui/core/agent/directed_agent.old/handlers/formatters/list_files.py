from llmui.core.agent.directed_agent.handlers.formatters.formatter import Formatter, LLMFormatter


class ListRequiredFilesGenerator(Formatter):

	def format(self, project_description: str) -> str:
		return f"""
I would like it if you could help me on an app I was working on.

{project_description}

Can you make a numbered list of all files with their description(like the one below) I must implement to build the app?
1. lib/apps/auth/application/blocs/AuthBloc.dart: This file defines the AuthBloc class, which manages the authentication state of the app.
2. lib/apps/auth/application/events/AuthEvent.dart: This file defines the AuthEvent class, which represents the events that can be emitted by the AuthBloc.
"""
