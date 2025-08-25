# Web Search Keyword Agent
Smolagents ToolCallingAgent example with ability to run script

This one has Python web server and ReactJS front end.

It creates simple python code and executes using `run_script` tool.
If `run_script` tool wasn't defined then the agent would not be able to solve problems which needs custom coding.

**Examples prompts**
- Give me list of the files in current folder
- Give me the ip address of this computer
- Give me the public ip address of this computer



#### Setting up front end
1. `cd frontend`
2. `npm install`

#### Setting up agent and server 
1. `python -m venv .venv`
2. `.venv\Scripts\activate`
3. `pip install -r requirements.txt`

#### To use
Start front end Reactjs app
1. `npm start`

#### Run web server
1. `python main.py`

Then browse http://localhost:3000/ and start chatting

