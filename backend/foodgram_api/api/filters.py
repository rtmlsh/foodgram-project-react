from django_filters import rest_framework, filters, BooleanFilter

from foodgram.models import Recipe, Tag, User


class RecipeFilter(rest_framework.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="slug"
    )
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = NumberFilter(method="get_favorite_filter")
    is_in_shopping_cart = NumberFilter(method="get_shopping_cart_filter")

    class Meta:
        model = Recipe
        fields = ("tags", "author",)

    def get_favorite_filter(self, queryset, name, value):
        return queryset.filter(favorite_recipes__user=self.request.user)

    def get_shopping_cart_filter(self, queryset, name, value):
        return queryset.filter(recipes_in_shopping_cart__user=self.request.user)
