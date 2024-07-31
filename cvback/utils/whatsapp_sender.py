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
        return json_response["access_token"]

    def authenticate_whatsapp(self):
        cid = settings.WHATSAPP_CLIENT_ID
        csec = settings.WHATSAPP_CLIENT_SECRET
        url = settings.WHATSAPP_AUTHENTICATION_URL

        return self.get_access_token(url, cid, csec)

    def send_whatsapp(self, users_data, event_data, token):
        url = settings.WHATSAPP_SEND_MESSAGES_URL
        data = {
                    "campaign":
                    {
                        "name": "campaña API",
                        "type_campaign_id": settings.WHATSAPP_CAMPAIGN_ID,
                        "type_action": settings.WHATSAPP_TYPE_ACTION,
                        "registers":
                            [
                                {
                                    "id": "",
                                    "name": user_data["username"],
                                    "phone": user_data["phone_number"],
                                    "email": "",
                                    "fecha": event_data["date"],
                                    "hora": event_data["time"],
                                    "placa_vehiculo": event_data["vehicle_license_plate"],
                                    "elementos_faltantes": ','.join(event_data["missing_labels"]),
                                    "link_detalles": event_data["details_link"],
                                    "imagenes": event_data["images"]
                                } for user_data in users_data
                            ]
                    }
                }

        token = f"Bearer {token}"

        response = requests.post(
            url,
            headers={
                "Authorization": token,
                }, json=data
        )
        return response
