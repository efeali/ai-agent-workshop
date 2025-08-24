# pip install llama-index llama-index-llms-ollama llama-index-tools-mcp langchain-community
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
#from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.agent import ReActAgent # This one is lighter version (according to Claude)
from llama_index.llms.ollama import Ollama
from prompt_templates import TODO_AGENT_PROMPT
import os

# Configuration variables
MCP_URL = os.environ.get("MCP_URL", "http://127.0.0.1:3001/sse")
TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0.7"))


async def setup_agent(llm_url: str, model: str) -> ReActAgent:
    """Setup and return the todo assistant agent"""
    try:
        if not llm_url.startswith("http"):
            raise ValueError("URL must start with http or https.")


        # Connect to MCP server
        print(f"Connecting to MCP server at {MCP_URL}")
        mcp_client = BasicMCPClient(MCP_URL)

        # Get tools list
        print("Fetching available tools...")
        tools = await McpToolSpec(client=mcp_client).to_tool_list_async()
        print(f"Found {len(tools)} tools")

        # Initialize Ollama LLM
        print(f"Initializing Ollama with model {model}...")
        llm = Ollama(
            base_url=llm_url,
            model=model,
            temperature=TEMPERATURE,
            context_window=8192, # Reduce from default (usually 4K-32K)
            #num_ctx=4096,  # Ollama-specific context limit
            #num_predict=1024 # Limit response length
        )

        # Create agent with flight search prompt
        system_prompt = TODO_AGENT_PROMPT.template.replace("{tools}", "").replace("{tool_names}", "").replace(
            "{input}", "")
        agent = ReActAgent(
            name="TodoAgent",
            llm=llm,
            tools=tools,
            system_prompt=system_prompt,
            temperature=TEMPERATURE,
            max_iterations=5
        )

        return agent
    except Exception as e:
        print(f"Error setting up agent: {str(e)}")
        raise


async def main(llm_url: str, model: str) -> ReActAgent:
    """Main function to run the todo agent application"""



    print("\n Natural Language ToDo Assistant")
    print("-" * 50)
    print("Ask me anything about your todo list using natural language!")
    print("Examples:")
    print("  • Flight at August 15th, 2025 3pm from NYC to LA")
    print("  • What are my tasks for today?")
    print("  • Complete the task to buy groceries")
    print("\nType 'exit' or 'quit' to end the session.")
    print("-" * 50)

    print("Make sure the todo mcp server is running with:")
    print("server --connection_type http")

    try:
        # Set up the agent
        agent = await setup_agent(llm_url=llm_url, model=model)
        print("Ready to work!")

        return agent


    except Exception as e:
        print(f"Error: {e}")
        print(f"Make sure the ToDo server is running at {MCP_URL}")
        raise

    #return 0


# if __name__ == "__main__":
#     sys.exit(asyncio.run(main()))