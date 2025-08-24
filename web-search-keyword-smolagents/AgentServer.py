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


