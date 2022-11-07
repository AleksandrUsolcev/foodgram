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
        # check for successful subscribe POST response from utils.add_remove
        if request is None:
            return True
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


class RecipeShortSerializer(RecipeSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscribeSerializer(UserListSerializer):
    recipes = serializers.SerializerMethodField('recipes_limit')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def recipes_limit(self, obj):
        request = self.context.get('request')
        queryset = obj.recipes.all()
        if request:
            recipes_limit = request.query_params.get('recipes_limit', None)
            if recipes_limit:
                queryset = queryset[:int(recipes_limit)]
        serializer = RecipeShortSerializer(queryset, many=True)
        return serializer.data
