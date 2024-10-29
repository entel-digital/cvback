from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

def generate_auth_link_for_events(user_id, event_id):
    try:
        User = get_user_model()  # Así obtienes el modelo correcto        
        user = User.objects.get(id=user_id)
        
        # Genera un token de autenticación con duración de 1 hora
        token = AccessToken.for_user(user)
        token.set_exp(lifetime=timezone.timedelta(hours=1))

        # Construye la URL de autenticación
        auth_url = f"{settings.FRONTEND_URL_EVENT}?token={str(token)}&eventid={event_id}"
        
        return auth_url
    except User.DoesNotExist:
        return None
