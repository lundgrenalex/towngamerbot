import unittest
from src.domain.answer import Answer


class TestAnswerModel(unittest.TestCase):

    def test_model(self):
        answer = Answer(user_id=1, chat_id=2, message='3243')
        self.assertEqual(type(answer.date), float)
        self.assertEqual(type(answer.user_id), int)
        self.assertEqual(type(answer.chat_id), int)
        self.assertEqual(type(answer.message), str)

if __name__ == '__main__':
    unittest.main()
