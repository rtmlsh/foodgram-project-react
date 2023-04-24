from django_filters import rest_framework, filters, BooleanFilter

from foodgram.models import Recipe, Tag, User


class RecipeFilter(rest_framework.FilterSet):
    tag = filters.AllValuesFilter(field_name='tags__slug')
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = BooleanFilter(method="get_favorite_filter")
    is_in_shopping_cart = BooleanFilter(method="get_shopping_cart_filter")

    class Meta:
        model = Recipe
        fields = ("tags", "author",)

    def get_favorite_filter(self, queryset, name, value):
        recipes = Recipe.objects.filter(favorite_recipes__user=self.request.user)
        return recipes

    def get_shopping_cart_filter(self, queryset, name, value):
        recipes = Recipe.objects.filter(recipes_in_shopping_cart__user=self.request.user)
        return recipes



    # def get_favorite_recipe(self, queryset, name, value):
    #     if value:
    #         return queryset.filter(favorite_recipes__user=self.request.user)
    #
    # def get_shopping_cart(self, queryset, name, value):
    #     if value:
    #         return queryset.filter(recipes_in_shopping_cart__user=self.request.user)
