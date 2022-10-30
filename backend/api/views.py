from recipes.models import Recipe, ShoppingCart, Tag
from rest_framework.viewsets import ModelViewSet
from users.models import User

from .serializers import (RecipeSerializer, ShoppingCartSerializer,
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
