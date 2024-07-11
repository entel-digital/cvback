import requests
import os
class TelegramSender():
    token =  os.environ["TELEGRAM_BOT_TOKEN"]# TODO: env vars
    def send_telegram(self, text, chat_id,img_url):    
        text_url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={text}"
        response = requests.get(text_url).json() # this sends the message    
        if img_url:
            send_image_url = "https://api.telegram.org/bot"+self.token+"/sendPhoto?chat_id="+chat_id+"&photo="+img_url
            image_response = requests.post(send_image_url)

        return response