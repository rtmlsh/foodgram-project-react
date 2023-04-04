from django_filters import rest_framework, filters, BooleanFilter

from foodgram.models import Recipe, Tag, User


class RecipeFilter(rest_framework.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = BooleanFilter(method='get_favorite_recipe')
    is_in_shopping_cart = BooleanFilter(method='get_shopping_cart')

    def get_favorite_recipe(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipes__user=self.request.user)

    def get_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipes__user=self.request.user)

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited')

