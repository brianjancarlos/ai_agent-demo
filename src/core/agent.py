from langchain_ollama import OllamaLLM
from colorama import Fore, Style

class Agent:
    def __init__(self, name: str, model: str, system_prompt: str = None):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = OllamaLLM(model=model)
        self.icon = "🤖"

    def _format_message(self, message: str) -> str:
        """Format message with agent name and icon."""
        return f"\n{Fore.CYAN}[{self.icon} {self.name} Agent]{Style.RESET_ALL}\n{message}"

    def invoke(self, prompt: str) -> str:
        """Invoke the agent with a given prompt."""
        if self.system_prompt:
            prompt = f"{self.system_prompt}\n\n{prompt}"

        response = self.llm.invoke(prompt)
        return self._format_message(response.strip())

    def stream(self, prompt: str):
        """Stream the agent's response."""
        if self.system_prompt:
            prompt = f"{self.system_prompt}\n\n{prompt}"

        buffer = ""
        for chunk in self.llm.stream(prompt):
            chunk_text = chunk
            # Simple coloring for demonstration
            if "Thinking:" in chunk_text or "Planning:" in chunk_text:
                chunk_text = f"{Fore.MAGENTA}{chunk_text}{Style.RESET_ALL}"

            print(chunk_text, end="", flush=True)
            buffer += chunk_text

        return self._format_message(buffer.strip())
