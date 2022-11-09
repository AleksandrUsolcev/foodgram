import django_filters

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug')
    is_favorited = django_filters.filters.NumberFilter(
        method='favorite_filter')
    is_in_shopping_cart = django_filters.filters.NumberFilter(
        method='cart_filter')

    def favorite_filter(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            return queryset.filter(favorited__user_id=user.id)
        return queryset

    def cart_filter(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            return queryset.filter(in_shopping_cart__user_id=user.id)
        return queryset

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.filters.CharFilter(
        field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name', )
