from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Amount, Favorite, Ingredient, Recipe, ShoppingCart,
                            Tag)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from users.models import Subscribe, User
from users.permissions import AllowAuthorOrReadOnly

from .filters import IngredientFilter, RecipeFilter
from .paginators import CustomPagination
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipePatchSerializer, RecipeSerializer,
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
    permission_classes = (AllowAuthorOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = RecipeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {}
        data['author'] = request.user
        data['image'] = serializer.validated_data.get('image')
        data['name'] = serializer.validated_data.get('name')
        data['text'] = serializer.validated_data.get('text')
        data['cooking_time'] = serializer.validated_data.get('cooking_time')
        ingredients = serializer.validated_data.get('ingredients')
        tags = serializer.validated_data.get('tags')
        recipe = Recipe.objects.create(**data)
        [recipe.tags.add(tag) for tag in tags]
        for ingredient in ingredients:
            Amount.objects.create(
                recipe=recipe, amount=ingredient.get('amount'),
                ingredient_id=ingredient.get('id')
            )
        return Response(RecipeShortSerializer(recipe).data,
                        status=HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        serializer = RecipePatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        instance.name = serializer.validated_data.get('name')
        instance.image = serializer.validated_data.get('image', instance.image)
        instance.text = serializer.validated_data.get('text')
        instance.cooking_time = serializer.validated_data.get('cooking_time')
        tags = serializer.validated_data.get('tags')
        instance.tags.clear()
        instance.save()
        ingredients = serializer.validated_data.get('ingredients')
        Amount.objects.filter(recipe_id=pk).delete()
        [instance.tags.add(tag) for tag in tags]
        for ingredient in ingredients:
            Amount.objects.create(
                recipe_id=pk, amount=ingredient.get('amount'),
                ingredient_id=ingredient.get('id')
            )
        serializer = RecipeShortSerializer(instance)
        return Response(serializer.data, HTTP_200_OK)

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
            'recipe__ingredients__ingredient__name',
            'recipe__ingredients__ingredient__measurement_unit').order_by(
            'recipe__ingredients__ingredient__name').annotate(
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
