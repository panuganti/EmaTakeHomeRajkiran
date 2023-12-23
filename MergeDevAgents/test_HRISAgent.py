import unittest
from unittest.mock import MagicMock

from HRISAgent import HRISAgent

class TestHRISAgent(unittest.TestCase):
    def setUp(self):
        self.agent = HRISAgent()

    def test_run(self):
        utterance = "What is time off balance for employee with id 12345?"
        expected_response = "The time off balance for the employee with ID 12345 is 10 hours."

        # Mock the initialize_agent and ai_agent.run methods
        self.agent.initialize_agent = MagicMock()
        self.agent.ai_agent.run = MagicMock(return_value=expected_response)

        response = self.agent._run(utterance)

        self.assertEqual(response, expected_response)
        self.agent.initialize_agent.assert_called_once_with(
            [self.agent.TimeOffBalanceTool()],
            self.agent.ChatOpenAI(model="gpt-3.5-turbo-0613"),
            agent=self.agent.AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )
        self.agent.ai_agent.run.assert_called_once_with(utterance)

    def test_arun(self):
        utterance = "Hello"

        with self.assertRaises(NotImplementedError):
            self.agent._arun(utterance)

if __name__ == "__main__":
    unittest.main()