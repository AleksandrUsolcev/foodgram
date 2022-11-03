import base64

from django.core.files.base import ContentFile
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers
from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_subscribed = serializers.SerializerMethodField('get_subscribed_info')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_subscribed_info(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            subscribed = request.user.subscribed.filter(author=obj)
            return subscribed.exists()
        return False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True, required=True)
    author = UserListSerializer(required=True)
    is_favorited = serializers.SerializerMethodField('get_favorited_info')
    is_in_shopping_cart = serializers.SerializerMethodField('get_cart_info')

    class Meta:
        model = Recipe
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def get_favorited_info(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            favorites = request.user.favorites.filter(recipe=obj)
            return favorites.exists()
        return False

    def get_cart_info(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            cart = request.user.cart.filter(recipe=obj)
            return cart.exists()
        return False
