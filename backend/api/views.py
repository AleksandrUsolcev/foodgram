from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
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


class FavorieViewSet(GenericViewSet):
    http_method_names = ('post', 'delete')
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        favorite = Favorite.objects.get_or_create(user=user, recipe=recipe)
        if favorite[1] is False:
            return Response(
                {'errors': 'already in favorited list'},
                status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'success'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def delete(self, request, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        favorite = Favorite.objects.filter(user=user, recipe=recipe)
        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'recipe not in favorited list'},
                        status=status.HTTP_400_BAD_REQUEST)
