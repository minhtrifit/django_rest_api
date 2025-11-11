import math
import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Order, OrderItem, Product, User
from .serializers import OrderSerializer, OrderItemSerializer
from .constants import OrderStatus

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_list(request):
    try:
        queryset = Order.objects.all()

        # Get query params
        status_param = request.GET.get("status", None)
        payment_method_param = request.GET.get("payment_method", None)
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))
        offset = (page - 1) * limit

        # Filter by params
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        if payment_method_param:
            try:
                queryset = queryset.filter(payment_method=uuid.UUID(payment_method_param))
            except ValueError:
                queryset = queryset.none()

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
        orders = queryset[offset:offset + limit]

        serializer = OrderSerializer(orders, many=True)

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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_detail(request, id):
    try:
        order = Order.objects.get(pk=id)
        serializer = OrderSerializer(order)
        
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except (Order.DoesNotExist, ValidationError):
        return Response({
            "success": False,
            "message": "Order not found."
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(f"Error in get detail order: {e}")

        return Response({
            "success": False,
            "message": "Something went wrong"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        data = request.data
        user_id = request.data["user_id"]

        items_data = data.get("items", [])
        payment_method_id = data.get("payment_method")
        note = data.get("note", "")

        if not user_id:
            return Response({
                "success": False,
                "message": "User ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.filter(id=uuid.UUID(user_id)).first()
            except ValueError:
                return Response({
                    "success": False,
                    "message": "User not found",
                }, status=status.HTTP_400_BAD_REQUEST)

        if not items_data:
            return Response({
                "success": False,
                "message": "Order must have at least one item"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Tất cả các bước trong đây thành công thì mới write vào trong database
        with transaction.atomic():
            # ✅ Tạo đơn hàng trước
            order = Order.objects.create(
                user=user,
                payment_method_id=payment_method_id,
                note=note,
                status="pending",
                total_amount=0
            )

            total = 0

            # ✅ Tạo từng item
            for item in items_data:
                product_id = item.get("product")
                quantity = int(item.get("quantity", 1))
                price = float(item.get("price", 0))

                if not product_id:
                    raise ValueError("Missing product ID for order item")

                # Kiểm tra sản phẩm hợp lệ
                product = Product.objects.filter(id=product_id, is_active=True).first()
                
                if not product:
                    raise ValueError(f"Product with ID {product_id} not found or inactive")

                if price <= 0:
                    price = product.price  # lấy giá hiện tại của sản phẩm

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )

                total += quantity * price

            # ✅ Cập nhật tổng tiền
            order.total_amount = total
            order.save()

        serializer = OrderSerializer(order)

        return Response({
            "success": True,
            "message": "Order created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    except ValueError as ve:
        return Response({
            "success": False,
            "message": "Invalid data",
            "error": str(ve)
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error in create_order: {e}")

        return Response({
            "success": False,
            "message": "Something went wrong"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_order(request, id):
    try:
        data = request.data
        order = Order.objects.get(pk=id)

        if not order:
            return Response({
                "success": False,
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            # ✅ Cập nhật thông tin cơ bản
            if "user" in data:
                return Response({
                    "success": False,
                    "message": "User info of order can not change",
                }, status=status.HTTP_400_BAD_REQUEST)

            if "status" in data:
                status_body = data["status"]

                if status_body not in OrderStatus.values:
                    return Response({
                        "success": False,
                        "message": f"Invalid status '{status_body}'. Must be one of: {OrderStatus.values}"
                    }, status=status.HTTP_400_BAD_REQUEST)

                order.status = data["status"]

            if "payment_method" in data:
                try:
                    order.payment_method_id = uuid.UUID(data["payment_method"])
                except ValueError:
                    return Response({
                        "success": False,
                        "message": "Invalid payment method",
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            if "note" in data:
                order.note = data["note"]

            items_data = data.get("items", None)
            total = 0

            if items_data is not None:
                # ✅ Xóa item cũ
                order.items.all().delete()

                # ✅ Tạo lại danh sách item mới
                for item in items_data:
                    product_id = item.get("product")
                    quantity = int(item.get("quantity", 1))
                    price = float(item.get("price", 0))

                    if not product_id:
                        raise ValueError("Missing product ID for order item")

                    product = Product.objects.filter(id=product_id, is_active=True).first()

                    if not product:
                        raise ValueError(f"Product {product_id} not found or inactive")

                    if price <= 0:
                        price = product.price

                    sub_total = quantity * price

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=price,
                    )

                    total += sub_total

                # ✅ Cập nhật lại tổng tiền
                order.total_amount = total

            order.save()

        serializer = OrderSerializer(order)

        return Response({
            "success": True,
            "message": "Order updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except ValueError as ve:
        return Response({
            "success": False,
            "message": "Invalid data",
            "error": str(ve)
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error in update_order: {e}")

        return Response({
            "success": False,
            "message": "Something went wrong"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)