import math
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Product
from .serializers import ProductSerializer

########## Get list ##########
@api_view(["GET"])
def get_list(request):
    try:
        # Get data from database
        queryset = Product.objects.all()

        # Get query params
        q = request.GET.get('q', None)
        min_price = request.GET.get('min_price', None)
        max_price = request.GET.get('max_price', None)
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))
        offset = (page - 1) * limit

        # Filter by params
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
            )
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        total_items = queryset.count()
        total_pages = math.ceil(total_items / limit) if limit > 0 else 1

        # Case: page > total_pages
        if page > total_pages and total_pages > 0:
            return Response({
                "success": True,
                "paging": {
                    "current_page": page,
                    "total_page": total_pages,
                    "total_item": total_items
                },
                "data": []
            }, status=status.HTTP_200_OK)

        # Get pagination data
        products = queryset[offset:offset + limit]

        # Serialize
        serializer = ProductSerializer(products, many=True)

        # Return json
        return Response({
            "success": True,
            "paging": {
                "current_page": page,
                "total_page": total_pages,
                "total_item": total_items
            },
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Error in get_list: {e}")

        return Response({
            "success": False,
            "message": "Something wrong",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

########## Get detail ##########
@api_view(['GET'])
def get_detail(request, id):
    try:
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except (Product.DoesNotExist, ValidationError):
        return Response({
            "success": False,
            "message": "Product not found."
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(f"Error get detail product: {e}")

        return Response({
            "success": False,
            "message": "Something wrong",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

########## Create ##########
@api_view(["POST"])
def create_product(request):
    try:
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Create product successfully"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error creating product: {e}")

        return Response({
            "success": False,
            "message": "Something wrong",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PATCH"])
def update_product(request, id):
    try:
        # Find product
        product = Product.objects.get(pk=id)

        # partial=True để chỉ update các key gửi từ body
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Update product successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        # Nếu is_valid = False
        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return Response({
            "success": False,
            "message": "Product not found."
        }, status=status.HTTP_404_NOT_FOUND)

    except ValidationError as e:
        return Response({
            "success": False,
            "message": "Invalid data.",
            "errors": str(e)
        }, status=status.HTTP_400_BAD_REQUEST) 

    except Exception as e:
        print(f"Error update product: {e}")

        return Response({
            "success": False,
            "message": "Something wrong"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)