from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Subscribe, User
from users.permissions import AllowAuthorOrReadOnly
from .filters import IngredientFilter, RecipeFilter
from .paginators import CustomPagination
from .serializers import (IngredientSerializer, RecipeCreateUpdateSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          TagSerializer, UserSubscribeSerializer)
from .utils import add_remove, shopping_list_pdf


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = CustomPagination
    permission_classes = (AllowAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        url_path=r'(?P<recipe>\d+)/favorite',
        url_name='recipe_favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, *args, **kwargs):
        self.serializer_class = RecipeShortSerializer
        return add_remove(self, request, 'recipe', Favorite, Recipe)

    @action(
        methods=['POST', 'DELETE'],
        detail=False,
        url_path=r'(?P<recipe>\d+)/shopping_cart',
        url_name='recipe_cart',
        permission_classes=[IsAuthenticated]
    )
    def cart(self, request, *args, **kwargs):
        self.serializer_class = RecipeShortSerializer
        return add_remove(self, request, 'recipe', ShoppingCart, Recipe)


class CartDownloadView(APIView):
    def get(self, request):
        cart = request.user.cart.values(
            'recipe__ingredients__ingredient__name',
            'recipe__ingredients__ingredient__measurement_unit').order_by(
            'recipe__ingredients__ingredient__name').annotate(
            total=Sum('recipe__ingredients__amount'))
        return shopping_list_pdf(cart)


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
        return User.objects.filter(subscribers__user=user)


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
        return add_remove(self, request, 'author', Subscribe, User)
