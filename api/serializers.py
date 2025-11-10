from rest_framework import serializers
from .models import Product, Category, User, PaymentMethod

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_active']

class ProductSerializer(serializers.ModelSerializer):
    # Dùng để hiển thị nested data khi GET (read_only)
    categories = CategorySerializer(many=True, read_only=True)

    # Dùng để nhận ID từ client khi POST/PUT (write_only)
    category_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'categories', 'category_ids', 'is_active']

    # Hàm này tự trigger khi serializer.is_valid() chạy ở product_controller
    def validate_category_ids(self, value):
        # Lấy danh sách ID của các category hiện có
        existing_ids = set(Category.objects.filter(id__in=value).values_list('id', flat=True))

        # Tìm category_id không tồn tại
        invalid_ids = [str(v) for v in value if v not in existing_ids]

        if invalid_ids:
            raise serializers.ValidationError({
                "message": "These category_ids do not exist",
                "invalid_ids": invalid_ids
            })

        return value

    def create(self, validated_data):
        # related models
        category_ids = validated_data.pop('category_ids', [])

        product = Product.objects.create(**validated_data)

        if category_ids:
            product.categories.set(category_ids)

        return product

    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if category_ids is not None:
            instance.categories.set(category_ids)

        return instance
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'key', 'name', 'is_active']