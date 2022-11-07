from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from users.models import Subscribe, User

from .filters import IngredientFilter, RecipeFilter
from .paginators import CustomPagination
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeShortSerializer, TagSerializer,
                          UserSubscribeSerializer)
from .utils import add_remove, shopping_list_pdf


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = CustomPagination

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        url_path=r'(?P<recipe>\d+)/favorite',
        url_name='recipe_favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, *args, **kwargs):
        self.serializer_class = RecipeShortSerializer
        action = add_remove(self, request, 'recipe', Favorite, Recipe)
        return action

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        url_path=r'(?P<recipe>\d+)/shopping_cart',
        url_name='recipe_cart',
        permission_classes=[IsAuthenticated]
    )
    def cart(self, request, *args, **kwargs):
        self.serializer_class = RecipeShortSerializer
        action = add_remove(self, request, 'recipe', ShoppingCart, Recipe)
        return action


class CartDownloadView(APIView):
    def get(self, request):
        cart = request.user.cart.values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit').order_by(
            'recipe__ingredients__name').annotate(
            total=Sum('recipe__ingredients__amount'))
        response = shopping_list_pdf(cart)
        return response


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None
    http_method_names = ('get',)


class UserSubscribeViewSet(ModelViewSet):
    serializer_class = UserSubscribeSerializer
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        subscribed = User.objects.filter(subscribers__user=user)
        return subscribed


class UserSubscribeActionViewSet(ViewSet):
    http_method_names = ('post', 'delete')
    serializer_class = UserSubscribeSerializer

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        url_path=r'(?P<author>\d+)/subscribe',
        url_name='user_subscribe',
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, *args, **kwargs):
        action = add_remove(self, request, 'author', Subscribe, User)
        return action
