from django_filters import rest_framework, filters

from foodgram.models import Recipe, Tag


class RecipeFilter(rest_framework.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    class Meta:
        model = Recipe
        fields = ('tags',)

