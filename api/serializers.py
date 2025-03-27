from rest_framework import serializers

from shop.models import Category, Product
from cart.models import Cart
from orders.models import Order, PostCode, OrderItem


# сериалйзер для продуктов или продукта
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "pk",
            "name",
            "image",
            "description",
            "price",
            "discount",
            "new",
            "quantyty",
            "available",
            "sell_price",
        ]

# сериалайзер для категорий
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ["id", "name"]

# сериалайзер для корзины, проверяет существования продукта в корзине перед созданием
class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = ["id", "user", "product", "quantity", "products_price"]

    def create(self, validated_data):
        cart = Cart.objects.filter(
            user=validated_data["user"], product=validated_data["product"]
        )
        if cart.exists():
            raise serializers.ValidationError("Этот продукт уже есть в Корзине")
        else:
            return super().create(validated_data)


# серилайзер для модели Заказа
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
    
    class Meta:
        model = Order
        fields = ["id","user","first_name","last_name","email","address","postal_code","city", 'text', 'get_total_cost']

# сериалайзер для почтового кода
class PostCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PostCode
        fields = ['status']


# Дополнительный сериализатор для OrderItemSerializer, чтобы выводить id, название и фото продукта
class OrderItemProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'image']


# сериалайзер элементов заказа   
class OrderItemSerializer(serializers.ModelSerializer):
      product = OrderItemProductSerializer()

      class Meta:
          model = OrderItem
          fields = ['product', 'quantity', 'products_price']
