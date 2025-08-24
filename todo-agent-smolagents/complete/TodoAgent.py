from smolagents import LiteLLMModel, tool, CodeAgent
from TodoManager import TodoManager
from EmailManager import EmailManager
from smolagents.agents import ToolCallingAgent
from datetime import datetime


# Create tool functions that wrap your TodoManager methods
@tool
def add_todo_task(task: str, description: str, due_date: str, due_time: str) -> str:
    """
    Add a new todo item with task, description, due date and time
    Args:
        task: A short title for the todo task
        description: Additional details about the task
        due_date: Due date in YYYY-MM-DD format
        due_time: Due time in HH:MM format
    """
    todo_manager = TodoManager()
    email_manager = EmailManager()


    new_id = todo_manager.add_todo(task, description, due_date, due_time)
    if new_id != -1:
        email_manager.send_email("New Todo Added",
                                 f"A new todo has been added:\n\nTask: {task}\nDescription: {description}\nDue Date: {due_date}\nDue Time: {due_time}")

        return f"Todo '{task}' added successfully with ID {new_id}"
    return "Failed to add todo"

@tool
def list_all_todos(status: str = None) -> str:
    """
    List todos, optionally filtered by status (pending, completed)
    Args:
        status: Filter todos by status (optional)
        - If None, lists all todos

    """
    todo_manager = TodoManager()
    return todo_manager.list_todos(status)

@tool
def complete_todo_task(todo_id: int) -> str:
    """
    Mark a todo as completed by its ID
    Args:
        todo_id: The ID of the todo to mark as completed

    """
    todo_manager = TodoManager()
    return todo_manager.complete_todo(todo_id)

@tool
def delete_todo_task(todo_id: int) -> str:
    """
    Delete a todo by its ID
    Args:
        todo_id: The ID of the todo to delete

    """
    todo_manager = TodoManager()
    return todo_manager.delete_todo(todo_id)

@tool
def check_upcoming_todos_task(response: bool) -> str | None:
    """
    Check for todos due within the next 24 hours and send email reminders.
    If passed True to this there will be a response text returned. Otherwise no text will be returned.

    Args:
        response: If True, return a text
        - If False, don't return a text, just send email reminders
    """
    todo_manager = TodoManager()
    email_reminder = EmailManager()

    upcoming_todos = todo_manager.get_upcoming_todos()
    if upcoming_todos:
        email_reminder.send_reminder(upcoming_todos)
        if response:
            return f"You have {len(upcoming_todos)} todos upcoming within 24hours. Reminders sent via email."

    else:
        if response:
            return "No todos due within the next 24 hours."



@tool
def get_current_date() -> str:
    """
    Get the current date in YYYY-MM-DD format
    """
    return datetime.now().strftime("%Y-%m-%d")

class TodoAgent:
    def __init__(self):
        self.model = LiteLLMModel(
            model_id="ollama/llama3.1:8b",
            api_base="http://localhost:11434/api/generate"
        )

        instructions = ("You are a Todo management assistant."
                      "You can help users manage their todos, send reminders, and answer questions about their tasks. "
                      "Use the tools provided to perform actions like adding, listing, completing, and deleting todos."
                      "After each action, provide a clear response to the user. "
                      "After each action, also check for upcoming todos tasks without a response."
                    "If no date is provided and instead time references used for due date get the current date and calculate the due date based on that.")

        self.agent = ToolCallingAgent(
            tools=[
                add_todo_task,
                list_all_todos,
                complete_todo_task,
                delete_todo_task,
                check_upcoming_todos_task,
                get_current_date
            ],
            model=self.model,
            stream_outputs=True,
            instructions=instructions
        )

    def run(self, prompt: str) -> str:
        """
        Send a prompt to the Agent and return the response.

        Args:
            prompt: The message to send to the Agent.

        Returns:
            The response from the Agent.
        """
        return self.agent.run(prompt)