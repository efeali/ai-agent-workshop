from smolagents import CodeAgent, WebSearchTool, LiteLLMModel, ToolCallingAgent, tool, PythonInterpreterTool
import io
import sys

@tool
def run_script(script: str) -> str:
    """
    Run a python script and return the output
    Args:
        script: the python code to be executed
    """
    print(f"Running script:\n{script}")

    try:
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()

        exec_globals = {}
        exec(script, exec_globals)

        # Restore stdout
        sys.stdout = old_stdout

        # Get captured output
        output = captured_output.getvalue()

        # Get result variable if it exists
        result = exec_globals.get('result', None)

        # Combine output and result
        if output and result is not None:
            return f"{output}\nResult: {result}"
        elif output:
            return output
        elif result is not None:
            return str(result)
        else:
            return "Script executed successfully, no output or result."

    except Exception as e:
        # Restore stdout in case of error
        sys.stdout = old_stdout
        return f"Error executing script: {str(e)}"


class AgentServer():
    def __init__(self):
        self.model = LiteLLMModel(
            model_id="ollama/gemma3:12b",
            api_base="http://localhost:11434/api/generate"
        )
        self.agent = ToolCallingAgent(
            tools=[WebSearchTool(), PythonInterpreterTool(), run_script],
            model=self.model
        )

    def prompt_to_smolagent(self, msg: str) -> str:
        """
        Send a prompt to the LLM and return the response.

        Args:
            msg: The message to send to the LLM.

        Returns:
            The response from the LLM.
        """
        return self.agent.run(msg)




# if __name__ == "__main__":
#     agent = AgentServer()
#     response = agent.prompt_to_smolagent(
#         "give me the list of files in current directory")
#     print(response)