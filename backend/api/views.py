from recipes.models import Ingredient, Recipe, ShoppingCart, Tag
from rest_framework.viewsets import ModelViewSet
from users.models import Subscribe, User

from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          TagSerializer, UserSerializer)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filterset_fields = ('tags', 'author')
    search_fields = ('tags', 'author')


class ShoppingCartViewSet(ModelViewSet):
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()


class SubscribeViewSet(ModelViewSet):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filterset_fields = ('name', 'measurement_unit')
    search_fields = ('name',)
