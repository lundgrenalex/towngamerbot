import re


class TelegramMessageAdapter:

    def __init__(self, message: dict):
        self.message = message
        self.message['meta'] = {}
        self.message['meta']['type'] = 'message'

    def __is_command(self) -> bool:
        if 'entities' not in self.message['message']:
            return False
        for entity in self.message['message']['entities']:
            if entity['type'] == 'bot_command':
                return True
        return False

    def __parse_command(self) -> str:
        return re.search(
            r'^\/([a-z_]{,10})',
            self.message['message']['text'])[1]

    def add_meta(self) -> dict:
        if self.__is_command():
            self.message['meta']['type'] = 'command'
            self.message['meta']['command'] = self.__parse_command()
        return self.message
