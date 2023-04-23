from django_filters import rest_framework, filters, BooleanFilter

from foodgram.models import Recipe, Tag, User


class RecipeFilter(rest_framework.FilterSet):
    tag = filters.AllValuesFilter(field_name='tags__slug')
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = BooleanFilter(method="get_favorite_recipe")
    is_in_shopping_cart = BooleanFilter(method="get_shopping_cart")

    class Meta:
        model = Recipe
        fields = ("tags", "author", "is_favorited", "is_in_shopping_cart")

    def get_favorite_recipe(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipes__user=self.request.user)

    def get_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipes__user=self.request.user)
