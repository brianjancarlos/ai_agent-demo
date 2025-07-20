import unittest
from unittest.mock import patch, MagicMock
from src.core.agent import Agent

class TestAgent(unittest.TestCase):

    @patch('src.core.agent.OllamaLLM')
    def test_agent_initialization(self, MockOllamaLLM):
        """Test that the agent is initialized correctly."""
        mock_llm_instance = MockOllamaLLM.return_value
        agent = Agent(name="Test Agent", model="test_model", system_prompt="Test prompt")

        self.assertEqual(agent.name, "Test Agent")
        self.assertEqual(agent.system_prompt, "Test prompt")
        MockOllamaLLM.assert_called_with(model="test_model")

    @patch('src.core.agent.OllamaLLM')
    def test_agent_invoke(self, MockOllamaLLM):
        """Test the invoke method of the agent."""
        mock_llm_instance = MockOllamaLLM.return_value
        mock_llm_instance.invoke.return_value = "Test response"

        agent = Agent(name="Test Agent", model="test_model", system_prompt="System prompt")
        response = agent.invoke("User prompt")

        expected_prompt = "System prompt\n\nUser prompt"
        mock_llm_instance.invoke.assert_called_with(expected_prompt)
        self.assertIn("Test response", response)

    @patch('src.core.agent.OllamaLLM')
    def test_agent_stream(self, MockOllamaLLM):
        """Test the stream method of the agent."""
        mock_llm_instance = MockOllamaLLM.return_value
        mock_llm_instance.stream.return_value = iter(["Test ", "response"])

        agent = Agent(name="Test Agent", model="test_model", system_prompt="System prompt")

        with patch('builtins.print') as mock_print:
            response = agent.stream("User prompt")

            expected_prompt = "System prompt\n\nUser prompt"
            mock_llm_instance.stream.assert_called_with(expected_prompt)

            # Check that print was called with the chunks
            mock_print.assert_any_call("Test ", end="", flush=True)
            mock_print.assert_any_call("response", end="", flush=True)

            self.assertIn("Test response", response)

if __name__ == '__main__':
    unittest.main()
