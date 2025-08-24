# Smolagents To-Do Agent

This is a small To-do application leveraging AI Agent using Smolagents.

### Frontend
The application has frontend UI which is a ReactJS application and can be found under /frontend/ folder.

### Web server
`main.py` file has a code for simple web server. It handles requests from ReactJS web application and also passes user prompt to AI agent and returns agent's response back to frontend application.

### Agent
`TodoAgent.py` file has the main agent code. It leverages Smolagents and uses LiteLLMModel class so you can configure it to use your local or remote LLM.

# To run
First, if you want this agent to send you emails about tasks you should enter your email server STMP details into `.env` file. If you don't want to use email feature then find lines related with `EmailManager` in `TodoAgent.py` file and comment them out.

##### Setting up front end
1. `cd frontend`
2. `npm install`

##### Setting up agent and server 

1. `python -m venv .venv`
2. `.venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Add your email account settings into `.env` file.

##### To start frontend:
1. `cd frontend/`
2. `npm start`

##### To start backend:
1. `python main.py`


Then browse http://localhost:3000/ and start chatting