# MCP To-do Agent

This is the same to-do app as smolagents todo v2, but it uses MCP instead of Smolagents. 
It has several tools defined for agent for adding task, deleting task, getting task list, marking a task as completed, checking for upcoming tasks (within next 24h), getting current date and sending email notifications.
Based on your conversation with chat bot, LLM + Agent will decide which tool to use, then call the best matching tool and execute the action. Tasks will be saved in CSV file in project's folder. 
Compared to Smolagents version, this app has more advanced prompt, and also can use ReActAgent which brings features like "reasoning and acting", creating complex decision making workflows (using llama_index's ReActAgent).

### Frontend
The application has frontend UI which is a ReactJS application and can be found under /frontend/ folder.

### Web server
`main.py` file has a code for simple web server. It receives requests coming from ReactJS web UI containing user message and passes it to the AI agent (via MCP client's run method). Then upon receiving agent's response, it returns that back to frontend application.

### MCP Server and Client + Agent
`mcp_server.py` file is MCP server where all tools defined and any tool execution would be performed.
`mcp_client.py` file is MCP client where communication with MCP server and communication with LLM will be performed

## To run
First, if you want this agent to send you emails about tasks you should enter your email server STMP details into `.env` file. If you don't want to use email feature then find lines related with `EmailManager` in `mcp_server.py` file and comment them out.

#### Setting up front end
1. `cd frontend`
2. `npm install`

#### Setting up agent and server 

1. `python -m venv .venv`
2. `.venv\Scripts\activate`
3. `pip install .`

**- Or -**
By using `uv` (modern Python package manager) 
1. `uv sync`

*To get uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`*

#### To start front end
1. `cd frontend/`
2. `npm start`

##### To start backend:
1. `python mcp_server.py`
2. `python main.py http://<ollama-url> <model-name>`

Then browse http://localhost:3000/ and start chatting

