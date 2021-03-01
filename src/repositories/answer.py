from src.storage import mongo
from src.domain.answer import Answer


class AnswerRepository:

    def __init__(self):
        self.db = mongo.connect()

    def save(self, answer: Answer) -> bool:
        return self.db.bot.game.insert_one(answer.__dict__)

    def get_last(self, chat_id: int) -> Answer:
        messages = self.db.bot.game.find({
            'chat_id': chat_id,
        }, {'_id': False}).sort([('date', pymongo.DESCENDING)]).limit(1)
        try:
            return Answer(**([m for m in messages][0]))
        except IndexError:
            return None
