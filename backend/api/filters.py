import django_filters
from recipes.models import Recipe, Tag


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
            return queryset.filter(users__user_id=user.id)

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']
