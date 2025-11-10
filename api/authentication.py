import uuid
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer

class UUIDJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # 🔹 Lấy view hiện tại từ resolver_match
        resolver = getattr(request, "resolver_match", None)
        if resolver:
            view = resolver.func
            # 🔹 Kiểm tra xem view có decorator @permission_classes([AllowAny]) không
            if hasattr(view, "cls"):
                permissions = getattr(view.cls, "permission_classes", [])
            else:
                permissions = getattr(view, "permission_classes", [])

            # 🔹 Nếu view có AllowAny thì bỏ qua luôn
            if any(perm == AllowAny for perm in permissions):
                return None

        # 🔹 Nếu không có header → bỏ qua (để public route chạy)
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        return (user, validated_token)

    def get_user(self, validated_token):
        user_id_claim = api_settings.USER_ID_CLAIM
        user_id = validated_token.get(user_id_claim)

        if not user_id:
            return None

        try:
            user = User.objects.get(id=uuid.UUID(str(user_id)))
            serializer = UserSerializer(user)
            print("AUTHEN USER:", serializer.data)

            return user
        except User.DoesNotExist:
            return None
