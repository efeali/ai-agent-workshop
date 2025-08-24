"""
Model Context Protocol (MCP) ToDo Agent Server implementation.

This module sets up an MCP-compliant server and registers todo agent tools
that follow Anthropic's Model Context Protocol specification. These tools can be
accessed by Claude and other MCP-compatible AI models.
"""
from mcp.server.fastmcp import FastMCP
import argparse
from TodoManager import *
from EmailManager import *

# Default server settings
DEFAULT_PORT = 3001
DEFAULT_CONNECTION_TYPE = "http"  # Alternative: "stdio"

import logging
from rich.logging import RichHandler


def setup_logging():
    """Configure and set up logging for the application."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="| %(levelname)-8s | %(name)s | %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]",
        handlers=[RichHandler(rich_tracebacks=True)],
        force=True  # This is the fix that overrides uvicorn & third-party loggers
    )

    logger = logging.getLogger("todo_agent")
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return logger


# Create the logger instance for import by other modules
logger = setup_logging()


def create_mcp_server(port=DEFAULT_PORT):
    """
    Create and configure the Model Context Protocol server.

    Args:
        port: Port number to run the server on

    Returns:
        Configured MCP server instance
    """
    mcp = FastMCP("todo-mcp-server", port=port)

    # Register MCP-compliant tools
    register_tools(mcp)

    return mcp


def register_tools(mcp):
    """
    Register all tools with the MCP server following the Model Context Protocol specification.

    Each tool is decorated with @mcp.tool() to make it available via the MCP interface.

    Args:
        mcp: The MCP server instance
    """

    # Create tool functions that wrap your TodoManager methods
    @mcp.tool()
    def add_todo_task(task: str, description: str, due_date: str, due_time: str) -> str:
        """
        Add a new todo item with task name, description, due date and time

        Args:
            task: A short title for the todo task
            description: Additional details about the task
            due_date: Due date in YYYY-MM-DD format
            due_time: Due time in HH:MM format

        Returns:
            Success message with new todo ID or failure message
        """
        todo_manager = TodoManager()
        email_manager = EmailManager()

        new_id = todo_manager.add_todo(task, description, due_date, due_time)
        if new_id != -1:
            email_manager.send_email("New Todo Added",
                                      f"A new todo has been added:\n\nTask: {task}\nDescription: {description}\nDue Date: {due_date}\nDue Time: {due_time}")

            return f"Todo '{task}' added successfully with ID {new_id}"
        return "Failed to add todo"

    @mcp.tool()
    def list_all_todos(status: str = None) -> str:
        """
        List all todos, optionally filtered by status (pending, completed). If no status is provided, all todos with any status are listed.

        Args:
            status: Filter todos by status (optional). If "None", lists all todos

        Returns:
            String representation of the todo list
        """
        todo_manager = TodoManager()
        return todo_manager.list_todos(status)

    @mcp.tool()
    def complete_todo_task(todo_id: int) -> str:
        """
        Mark a todo as completed by its ID

        Args:
            todo_id: The ID of the todo to mark as completed

        Returns:
            Success message with todo ID or failure message
        """
        todo_manager = TodoManager()
        return todo_manager.complete_todo(todo_id)

    @mcp.tool()
    def delete_todo_task(todo_id: int) -> str:
        """
        Delete a todo by its ID
        Args:
            todo_id: The ID of the todo to delete
        Returns:
            Success message with todo ID or failure message
        """
        todo_manager = TodoManager()
        return todo_manager.delete_todo(todo_id)

    @mcp.tool()
    def check_upcoming_todos_task(response: bool) -> str:
        """
        Check for todos due within the next 24 hours and send email reminders.
        If response argument passed with True to this function there will be a response text returned. Otherwise, no text will be returned.

        Args:
            response: If True return a text, if False return an empty text, just send email reminders

        Returns:
            Status message about upcoming todos or empty string
        """
        todo_manager = TodoManager()
        email_reminder = EmailManager()

        upcoming_todos = todo_manager.get_upcoming_todos()
        if upcoming_todos:
            email_reminder.send_reminder(upcoming_todos)
            if response:
                return f"You have {len(upcoming_todos)} todos upcoming within 24hours. Reminders sent via email."
            else:
                return ""
        else:
            if response:
                return "No todos due within the next 24 hours."
            else:
                return ""

    @mcp.tool()
    def get_current_date() -> str:
        """
        Get the current date in YYYY-MM-DD HH:MM format
        Returns:
            Current date and time as a formatted string
        """
        return datetime.now().strftime("%Y-%m-%d %HH:%M")

    @mcp.tool()
    def server_status():
        """
        Check if the Model Context Protocol server is running.

        This MCP tool provides a simple way to verify the server is operational.

        Returns:
            A status message indicating the server is online
        """
        return {"status": "online", "message": "MCP ToDo Agent server is running"}

    logger.debug("Model Context Protocol tools registered")


def main():
    """
    Main entry point for the Model Context Protocol ToDo Agent Server.
    """
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Model Context Protocol ToDo Agent Service")
    parser.add_argument("--connection_type", type=str, default=DEFAULT_CONNECTION_TYPE,
                        choices=["http", "stdio"], help="Connection type (http or stdio)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"Port to run the server on (default: {DEFAULT_PORT})")
    args = parser.parse_args()

    # Initialize MCP server
    mcp = create_mcp_server(port=args.port)

    # Determine server type
    server_type = "sse" if args.connection_type == "http" else "stdio"

    # Start the server
    logger.info(
        f"🚀 Starting Model Context Protocol ToDo Agent Service on port {args.port} with {args.connection_type} connection")
    mcp.run(server_type)


if __name__ == "__main__":
    main() 