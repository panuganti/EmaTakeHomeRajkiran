import unittest
from unittest.mock import MagicMock
from ResponsibleAIAgent import ResponsibleAIAgent

class TestResponsibleAIAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ResponsibleAIAgent()

    def test_shouldFlag(self):
        user_utterance = "This is a test message."
        expected_flagged = False

        # Mock the OpenAI client and its moderations.create method
        self.agent.OpenAI = MagicMock()
        self.agent.OpenAI.moderations.create = MagicMock(return_value={"results": [{"flagged": expected_flagged}]} )

        flagged = self.agent.shouldFlag(user_utterance)

        self.assertEqual(flagged, expected_flagged)
        self.agent.OpenAI.moderations.create.assert_called_once_with(input=user_utterance)

    def test_detectPromptInjection(self):
        user_utterance = "This is a test message."
        expected_result = False

        # Mock the _get_completion method
        self.agent._get_completion = MagicMock(return_value="N")

        result = self.agent.detectPromptInjection(user_utterance)

        self.assertEqual(result, expected_result)
        self.agent._get_completion.assert_called_once()

if __name__ == "__main__":
    unittest.main()