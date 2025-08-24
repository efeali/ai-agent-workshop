import ollama
from prompt_templates2 import TODO_AGENT_PROMPT

class MyOllama:
    def __init__(self, ollama_host: str, model: str):
        # Configure ollama client with custom host if needed

        self.ollama_client = ollama.Client(host=ollama_host)
        self.model = model
        self.ollama_host = ollama_host
        self.supports_tools = None  # Will be determined on first use

        print(f"Using Ollama server at: {self.ollama_host}")


    async def run(self, user_message: str):
        """Process a single user message with system prompt"""
        messages = [
            {"role": "user", "content": user_message},
            {"role": "system", "content": TODO_AGENT_PROMPT.template}
        ]

        # Use ollama.chat for conversation-style interaction
        response = self.ollama_client.chat(
            model=self.model,
            messages=messages,
            stream=False,
            think=True,
            options={
                "temperature": 0.7
            }
        )

        final_answer = response['message']['content']
        parts = final_answer.split("Final Answer:", 1)  # Split only on first occurrence
        if len(parts) > 1:
            final_answer =  parts[1]

        return final_answer


async def main(llm_url: str, model: str):
    print("Setting up clean LLM...")
    llm = MyOllama(ollama_host=llm_url, model=model)
    print("Ready!")
    return llm
