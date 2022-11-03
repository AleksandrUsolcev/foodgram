from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from users.models import Subscribe, User

from .filters import RecipeFilter
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserSubscribeSerializer)
from .utils import add_remove, pdf_list_response


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
        url_path=r'(?P<recipe>\d+)/favorite',
        url_name='recipe_favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, *args, **kwargs):
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
        action = add_remove(self, request, 'recipe', ShoppingCart, Recipe)
        return action


class CartDownloadView(APIView):
    def get(self, request):
        return pdf_list_response()


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    permission_classes = (AllowAny,)
    http_method_names = ('get',)


class UserSubscribeViewSet(ModelViewSet):
    serializer_class = UserSubscribeSerializer
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        subscribed = User.objects.filter(subscribers__user=user)
        return subscribed


class UserSubscribeActionViewSet(ViewSet):
    http_method_names = ('post', 'delete')

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
