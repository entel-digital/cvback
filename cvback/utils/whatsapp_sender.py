import requests
from django.conf import settings

class WhatsappSender():
    def get_access_token(self, url, client_id, client_secret):
        response = requests.post(
            url,
            data={"grant_type": "client_credentials"},
            auth=(client_id, client_secret),
        )
        json_response = response.json()
        print(json_response)
        return json_response["access_token"]


    def authenticate_whatsapp(self):
        cid = settings.WHATSAPP_CLIENT_ID
        csec = settings.WHATSAPP_CLIENT_SECRET
        url = settings.WHATSAPP_AUTHENTICATION_URL

        return self.get_access_token(url, cid, csec)


    def send_whatsapp(self, phone_numbers,token,username,images,details_link,missing_labels,vehicle_license_plate,date,time):

        url = os.environ["WHATSAPP_SEND_MESSAGES_URL"]
        data = {
            "campaign": {
            "name": "campaña API",
            "type_campaign_id": settings.WHATSAPP_CAMPAIGN_ID,
            "type_action": settings.WHATSAPP_TYPE_ACTION,
            "registers": [
                {
                    "id": "",
                    "name": username,
                    "phone": phone_number,
                    "email": "",
                    "fecha": date,
                    "hora": time,
                    "placa_vehiculo": vehicle_license_plate,
                    "elementos_faltantes": missing_labels,
                    "link_detalles": details_link,
                    "imagenes": [images]
                } for phone_number in phone_numbers
                ]
            }
        }

        token = f"Bearer {token}"


        response = requests.post(
            url,
            headers={
                "Authorization": token,
                },json=data
        )
        return response
