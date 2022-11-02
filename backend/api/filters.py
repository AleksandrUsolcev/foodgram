import django_filters
from recipes.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug')

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
