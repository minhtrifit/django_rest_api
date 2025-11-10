import uuid
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from .models import User

class UUIDJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id_claim = api_settings.USER_ID_CLAIM
        user_id = validated_token.get(user_id_claim)

        if not user_id:
            return None

        try:
            return User.objects.get(id=uuid.UUID(str(user_id)))
        except User.DoesNotExist:
            return None
