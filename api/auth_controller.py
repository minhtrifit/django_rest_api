from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from .models import User

@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    try:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            # Get username, password from client body
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            # Get user from database
            user = User.objects.filter(username=username)

            # Kiểm tra trùng username
            if user.exists():
                return Response({
                    "success": False,
                    "message": "Username already exists",
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Hashed password
            hased_password = make_password(password)

            # save to database
            serializer.save(password=hased_password)

            return Response({
                "success": True,
                "message": "Create user successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
                "success": False,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error in create user: {e}")

        return Response({
            "success": False,
            "message": "Something wrong",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        # Get user from database
        user = User.objects.get(username=username)

        # Check password
        is_correct_password = check_password(password, user.password)

        # Password not match
        if not is_correct_password:
            return Response({
                "success": False,
                "message": "Username or password not match"
            }, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = UserSerializer(user)
        access_token = AccessToken.for_user(user)
        
        return Response({
            "success": True,
            "message": "Login successfully",
            "data": {
                **serializer.data,
                "token": str(access_token),
            }
        }, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({
            "success": False,
            "message": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(f"Error in login: {e}")

        return Response({
            "success": False,
            "message": "Something wrong",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated]) # Thêm decorator này với các controller cần authen
def get_profile(request):
    try:
        # request.user đã là user hiện tại nếu JWT hợp lệ
        user = request.user;

        serializer = UserSerializer(user)

        return Response({
            "success": True,
            "message": "Get user profile successfully",
            "data": serializer.data
        })

    except Exception as e:
        print(f"Error in get user profile: {e}")
        return Response({
            "success": False,
            "message": "Something wrong",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
