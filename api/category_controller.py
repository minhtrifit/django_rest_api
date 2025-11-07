import math
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Category
from .serializers import CategorySerializer

@api_view(['GET'])
def get_list(request):
    try:
        queryset = Category.objects.all()

        is_active = request.GET.get('is_active', None)

        if is_active:
            is_active_bool = True if is_active == "true" else False

            queryset = queryset.filter(is_active=is_active_bool)

        serializer = CategorySerializer(queryset, many=True)

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


@api_view(['POST'])
def create_category(request):
    try:
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Create category successfully"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"Error creating category: {e}")

        return Response({
            "success": False,
            "message": "Something wrong",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['PATCH'])
def update_category(request, id):
    try:
        category = Category.objects.get(pk=id)

        # partial=True để chỉ update các key gửi từ body
        serializer = CategorySerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Update category successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        # Nếu is_valid = False
        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST) 

    except Category.DoesNotExist:
        return Response({
            "success": False,
            "message": "Category not found."
        }, status=status.HTTP_404_NOT_FOUND)

    except ValidationError as e:
        return Response({
            "success": False,
            "message": "Invalid data.",
            "errors": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error update category: {e}")

        return Response({
            "success": False,
            "message": "Something wrong",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
