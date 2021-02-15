from pymongo import MongoClient, ASCENDING, DESCENDING

db = MongoClient('mongodb://localhost:27017')

result = []

result.append(db.bot.updates.create_index('update_id'))
result.append(db.bot.updates.create_index('callback_query.message.message_id'))
result.append(db.bot.updates.create_index('callback_query.message.message_id'))
result.append(db.bot.updates.create_index('message.message.message_id'))
result.append(db.bot.updates.create_index('edited_message.message_id'))
result.append(db.bot.updates.create_index('callback_query.chat.id'))
result.append(db.bot.updates.create_index('message.chat.id'))
result.append(db.bot.updates.create_index('edited_message.chat.id'))

print(result)
