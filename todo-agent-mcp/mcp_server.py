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