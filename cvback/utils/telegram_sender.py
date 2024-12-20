import requests
from django.conf import settings
from datetime import datetime


class TelegramSender():

    token = settings.TELEGRAM_BOT_TOKEN

    def send_telegram(self, chat_id, event_data):

        text = f"""📅 Fecha: {event_data['date']}
⏰ Hora del evento: {event_data['time']}
🚌 Placa Vehículo: {event_data['vehicle_license_plate']}
{event_data['event_label']}
Elementos faltantes: {','.join(event_data['missing_labels'])}
🔗 Para más detalles, visite:
{event_data['details_link']}
Hora de envío: {datetime.now().strftime("%H:%M:%S")}
"""
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={text}"
        response = requests.get(url).json()  # this sends the message
        for image in event_data["images"]:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendPhoto"

                response = requests.post(url, data={"photo": image, "chat_id": chat_id})
                print(response)
            except Exception as e:
                print(f"IMAGE:{image} can't be sended", e)
        for video in event_data["videos"]:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendVideo"
                response = requests.post(url, data={"video": video, "chat_id": chat_id})
                print(response)
            except Exception as e:
                print(f"Video:{video} can't be sended", e)

        return response
