from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name","email","username", "password", "avatar"]
        extra_kwargs = {
            'password' : {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ["first_name", "last_name"]

    
class BookSerializer(ModelSerializer):
    author = AuthorSerializer()  

    class Meta:
        model = Book
        fields = ["id", "title", "author", "price", "image"]


class CartItemSerializer(ModelSerializer):
    book = BookSerializer()

    class Meta:
        model  = CartItem
        fields = ["book", "quantity"]

class CartSerializer(ModelSerializer):
    items = CartItemSerializer()
    buyer = UserSerializer()

    class Meta:
        model = Cart
        fields = ["items","buyer"]