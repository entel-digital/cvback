import requests 
import os

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
        cid = os.environ["WHATSAPP_CLIENT_ID"]
        csec = os.environ["WHATSAPP_CLIENT_SECRET"]
        url = os.environ["WHATSAPP_AUTHENTICATION_URL"]

        return self.get_access_token(url, cid, csec)   
        
    
    def send_whatsapp(self, users_data,token,event_data):    
        
        url = os.environ["WHATSAPP_SEND_MESSAGES_URL"]
        data = { 
            "campaign": { 
            "name": "campaña API", 
            "type_campaign_id": os.environ["WHATSAPP_CAMPAIGN_ID"], 
            "type_action": os.environ['WHATSAPP_TYPE_ACTION'], 
            "registers": [ 
                    { 
                    "id": "", 
                    "name": users.get("username"), 
                    "phone": users.get("phone_number"), 
                    "email": users.get("email",""), 
                    "fecha": event_data.get("date",""), 
                    "hora": event_data.get("time",""), 
                    "placa_vehiculo": event_data.get("vehicle_licence_plate",'-'), 
                    "elementos_faltantes": event_data.get("missing_labels"), 
                    "link_detalles": event_data.get("details_link"), 
                    "imagenes": event_data.get("images")
                } for users in users_data
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
