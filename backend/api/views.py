from recipes.models import Ingredient, Recipe, ShoppingCart, Tag
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from users.models import Subscribe

from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          TagSerializer)
from .utils import StandardPagination


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ('get',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filterset_fields = ('tags', 'author')
    search_fields = ('tags', 'author')
    pagination_class = StandardPagination
    permission_classes = (AllowAny,)
    http_method_names = ('get', 'post')


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
