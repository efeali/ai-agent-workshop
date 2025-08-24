from smolagents import CodeAgent, InferenceClientModel, WebSearchTool

# InferenceClientModel is used to connect to Hugging Face Inference API (old HfApiModel)

agent = CodeAgent(tools=[], model=InferenceClientModel(model_id="Qwen/Qwen2.5-7B-Instruct"),
                  add_base_tools=True,
                  verbosity_level=2)
agent.run("What is the capital of Turkey?")

# print(agent.system_prompt)