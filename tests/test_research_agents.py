import unittest
from unittest.mock import patch, MagicMock
from src.agents.research import Researcher, Writer, Editor

class TestResearchAgents(unittest.TestCase):

    @patch('src.agents.research.DDGS')
    @patch('src.agents.research.Agent.invoke')
    def test_researcher(self, mock_invoke, MockDDGS):
        """Test the Researcher agent."""
        # Mock DDGS
        mock_ddgs_instance = MockDDGS.return_value.__enter__.return_value
        mock_ddgs_instance.text.return_value = [
            {'title': 'Test Title', 'body': 'Test body.', 'link': 'http://example.com'}
        ]

        # Mock Agent.invoke
        mock_invoke.return_value = "Test summary"

        researcher = Researcher(model="test_model")
        summary = researcher.research("Test topic")

        self.assertEqual(summary, "Test summary")
        self.assertEqual(len(researcher.references), 1)
        self.assertIn("Test Title", researcher.references[0])

        # Check that invoke was called with the correct prompt
        mock_invoke.assert_called_once()
        call_args = mock_invoke.call_args[0][0]
        self.assertIn("Topic: Test topic", call_args)
        self.assertIn("Test Title: Test body.", call_args)

    @patch('src.agents.research.Agent.invoke')
    def test_writer(self, mock_invoke):
        """Test the Writer agent."""
        mock_invoke.return_value = "Test article"
        writer = Writer(model="test_model")
        article = writer.write_article("Test summary")

        self.assertEqual(article, "Test article")
        mock_invoke.assert_called_with("Research notes:\n\nTest summary")

    @patch('src.agents.research.Agent.invoke')
    def test_editor(self, mock_invoke):
        """Test the Editor agent."""
        mock_invoke.return_value = "Edited article"
        editor = Editor(model="test_model")
        edited_article = editor.edit_article("Test article")

        self.assertEqual(edited_article, "Edited article")
        mock_invoke.assert_called_with("Article:\n\nTest article")

if __name__ == '__main__':
    unittest.main()
