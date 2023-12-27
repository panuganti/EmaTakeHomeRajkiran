import unittest
from unittest.mock import MagicMock
from CRMAgent import CRMAgent

class TestCRMAgent(unittest.TestCase):
    def setUp(self):
        self.agent = CRMAgent()

    def test_run(self):
        utterance = "Retrieve contact information for John Doe"
        expected_response = "Here is the contact information for John Doe"

        # Mock the initialize_agent method and its run method
#        self.agent.initialize_agent = MagicMock()
#        self.agent.initialize_agent.return_value.run = MagicMock(return_value=expected_response)

        response = self.agent._run(utterance)

        self.assertEqual(response, expected_response)

    def test_arun(self):
        utterance = "Retrieve contact information for John Doe"

        with self.assertRaises(NotImplementedError):
            self.agent._arun(utterance)

if __name__ == "__main__":
    unittest.main()