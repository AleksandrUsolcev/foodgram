from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Recipe, ShoppingCart, Tag
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from users.models import Subscribe

from .filters import RecipeFilter
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          TagSerializer)


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ('get',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (AllowAny,)
    http_method_names = ('get', 'post', 'patch', 'delete')


class ShoppingCartViewSet(ModelViewSet):
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()


class SubscribeViewSet(ModelViewSet):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    permission_classes = (AllowAny,)
    http_method_names = ('get',)
