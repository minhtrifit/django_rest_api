from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import PaymentMethod
from .serializers import PaymentMethodSerializer

@api_view(["GET"])
@permission_classes([AllowAny])
def get_list(request):
    try:
        queryset = PaymentMethod.objects.all()

        is_active = request.GET.get('is_active', None)

        if is_active:
            is_active_bool = True if is_active == "true" else False

            queryset = queryset.filter(is_active=is_active_bool)

        serializer = PaymentMethodSerializer(queryset, many=True)

        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"Error in get_list: {e}")

        return Response({
            "success": False,
            "message": "Something wrong",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_payment_method(request):
    try:
        serializer = PaymentMethodSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "success": True,
                "message": "Create payment method successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error in create payment method: {e}")

        return Response({
            "success": False,
            "message": "Something wrong",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)