from recipes.models import Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import Subscribe, User

from .permissions import UserPermission
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          TagSerializer, UserSerializer)
from .utils import StandardPagination


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (UserPermission,)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def get_profile(self, request):
        response = UserSerializer(request.user).data
        return Response(response, status=status.HTTP_200_OK)


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ('get',)


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filterset_fields = ('tags', 'author')
    search_fields = ('tags', 'author')
    pagination_class = StandardPagination


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
