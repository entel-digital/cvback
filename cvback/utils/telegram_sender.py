import requests
from django.conf import settings

class TelegramSender():
    token = settings.TELEGRAM_BOT_TOKEN # TODO: env vars
    def send_telegram(self, text, chat_id):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={text}"
        response = requests.get(url).json() # this sends the message
        return response