from lib.storage import game
from lib import helpers
from lib import telegram
from config import telegram_key

# getChat info
chat_id = 149053392

username = telegram.get_chat(chat_id, bot_token=telegram_key)['result']['username']
score = game.get_score(chat_id)
message = helpers.render_template('winner', username, score)
print(message)
