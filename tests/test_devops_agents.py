import unittest
from unittest.mock import patch
from src.agents.devops import IncidentAnalyst, RunbookWriter

class TestDevopsAgents(unittest.TestCase):

    @patch('src.agents.devops.Agent.stream')
    def test_incident_analyst(self, mock_stream):
        """Test the IncidentAnalyst agent."""
        mock_stream.return_value = "Test analysis"
        analyst = IncidentAnalyst(model="test_model")
        result = analyst.analyze_logs("Test logs")

        self.assertEqual(result, "Test analysis")
        mock_stream.assert_called_with("Analyze the following incident logs:\n\nTest logs")

    @patch('src.agents.devops.Agent.stream')
    def test_runbook_writer(self, mock_stream):
        """Test the RunbookWriter agent."""
        mock_stream.return_value = "Test runbook"
        writer = RunbookWriter(model="test_model")
        result = writer.create_runbook("Test analysis")

        self.assertEqual(result, "Test runbook")
        mock_stream.assert_called_with("Using the following incident analysis:\n\nTest analysis")

if __name__ == '__main__':
    unittest.main()
