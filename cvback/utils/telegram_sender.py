import requests
from django.conf import settings


class TelegramSender():

    token = settings.TELEGRAM_BOT_TOKEN  # TODO: env vars

    def send_telegram(self, text, chat_id, images):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={text}"
        response = requests.get(url).json()  # this sends the message
        if images:
            for image in images:
                try:
                    url = f"https://api.telegram.org/bot{self.token}/sendPhoto?chat_id={chat_id}&photo={image}"
                    response = requests.get(url)
                except Exception as e:
                    print(f"IMAGE:{image} can't be sended", e)

        return response
