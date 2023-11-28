import subprocess
import os
from llmui.core.environment.action import LLMUIAction
from llmui.core.environment.action_executor import ActionExecutor


class BashExecutor(ActionExecutor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.chdir(self._cwd)

    def is_valid_action(self, action: LLMUIAction) -> bool:
        return action.command == "bash"

    def __execute_bash(self, command: str):
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            return f"Error executing bash command: {error.decode()}"
        return output.decode()

    def execute(self, action: LLMUIAction) -> str:
        if action.args[0] == "cd":
            os.chdir(' '.join(action.args[1:]))
            return f"Changed working directory to {os.getcwd()}"
        else:
            command = ' '.join(action.args)
            result = self.__execute_bash(command)
            return result.strip()