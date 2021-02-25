from lib.storage.game import CityGame

message = {
    'update_id': 34583062,
    'message': {
        'message_id': 165,
        'from': {
            'id': 3241740,
            'is_bot': False,
            'first_name': 'Alex',
            'username': 'lundgren',
            'language_code': 'en'
        },
        'chat': {
            'id': 3241740,
            'first_name': 'Alex',
            'username': 'lundgren',
            'type': 'private'
        },
        'date': 1613357117,
        'text': 'йошкар-ола'
    }
}

game = CityGame(message=message)
result = game.exists()
print(result)
