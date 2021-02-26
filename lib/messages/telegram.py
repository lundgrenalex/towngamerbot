import requests
from urllib.parse import urlencode
import json


class TelegramBotApi(object):
    """docstring for ."""

    api_url = 'https://api.telegram.org/bot'

    def __init__(self, token):
        self.token = token

    def get_updates(params: dict = None) -> dict:
        params = urlencode(params) or ''
        res = requests.get(f'{api_url}{self.token}/getUpdates?{params}', timeout=10)
        return res.json()

    def send_message(chat_id, message: str, params: dict = None) -> dict:
        if not message:
            return
        params = params or {}
        params.update({'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'})
        res = requests.post(f'{api_url}{self.token}/sendMessage', data=params, timeout=10)
        return res.json()

    def edit_message(chat_id, message: str, params: dict = None) -> dict:
        if not message:
            return
        params = params or {}
        params.update({'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'})
        res = requests.post(f'{api_url}{self.token}/editMessageText', data=params, timeout=10)
        return res.json()

    def get_chat(chat_id: int) -> dict:
        params = {'chat_id': chat_id}
        res = requests.post(f'{api_url}{self.token}/getChat', data=params, timeout=10)
        return res.json()

    def send_photo(chat_id, url: str, params: dict = None) -> dict:
        params = params or {}
        params.update({
            'photo': url,
            'chat_id': chat_id,
            'caption': params.get('caption', ''),
            'parse_mode': 'Markdown'
        })
        res = requests.post(f'{api_url}{self.token}/sendPhoto', data=params, timeout=10)
        return res.json()

    def answer_callback_query(callback_query_id, message: str, params: dict = None):
        if not message:
            return
        params = params or {}
        params.update({'callback_query_id': callback_query_id, 'text': message})
        res = requests.post(f'{api_url}{self.token}/answerCallbackQuery', data=params, timeout=10)
        return res.json()

    def sendMediaGroup(chat_id, media: list = [], params: dict = None):
        params = params or {}
        params.update({'media': json.dumps(media), 'chat_id': chat_id})
        res = requests.post(f'{api_url}{self.token}/sendMediaGroup', data=params, timeout=30)
        return res.json()
