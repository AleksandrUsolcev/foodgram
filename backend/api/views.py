from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import RecipeFilter
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


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

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        url_path=r'(?P<recipe_id>\d+)/favorite',
        url_name='recipe_favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        favorite = Favorite.objects.filter(user=user, recipe=recipe)

        if request.method == 'POST' and favorite.exists():
            return Response(
                {'errors': 'already in favorited list'},
                status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'POST':
            Favorite.objects.create(user=user, recipe=recipe)
            return Response(
                {'detail': 'success'},
                status=status.HTTP_201_CREATED)

        if request.method == 'DELETE' and favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'DELETE':
            return Response({'errors': 'recipe not in favorited list'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        url_path=r'(?P<recipe_id>\d+)/shopping_cart',
        url_name='recipe_cart',
        permission_classes=[IsAuthenticated]
    )
    def cart(self, request, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        cart = ShoppingCart.objects.filter(user=user, recipe=recipe)

        if request.method == 'POST' and cart.exists():
            return Response(
                {'errors': 'already in shopping cart'},
                status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'POST':
            ShoppingCart.objects.create(user=user, recipe=recipe)
            return Response(
                {'detail': 'success'},
                status=status.HTTP_201_CREATED)

        if request.method == 'DELETE' and cart.exists():
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'DELETE':
            return Response({'errors': 'recipe not in shopping cart'},
                            status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    permission_classes = (AllowAny,)
    http_method_names = ('get',)
