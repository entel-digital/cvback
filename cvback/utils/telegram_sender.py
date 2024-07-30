import requests
from django.conf import settings
from datetime import datetime


class TelegramSender():

    token = settings.TELEGRAM_BOT_TOKEN

    def send_telegram(self, chat_id, event_data):

        text = f"""📅 Fecha: {event_data['date']}
⏰ Hora del evento: {event_data['time']}
🚌 Placa Vehículo: {event_data['vehicle_license_plate']}
Elementos faltantes: {','.join(event_data['missing_labels'])}
🔗 Para más detalles, visite:
https://app-beta.sgscm.vision.enteldigital.cl/kTdTNssbOrlOBTyv4gYWZeaYqY06K5IC/events/event/{event_data['id']}/change/
Mensaje enviado a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}"""
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={text}"
        response = requests.get(url).json()  # this sends the message
        for image in event_data["images"]:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendPhoto?chat_id={chat_id}&photo={image}"
                response = requests.get(url)
                print(response)
            except Exception as e:
                print(f"IMAGE:{image} can't be sended", e)
        for video in event_data["videos"]:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendVideo?chat_id={chat_id}&video={video}"
                response = requests.get(url)
            except Exception as e:
                print(f"Video:{video} can't be sended", e)

        return response
