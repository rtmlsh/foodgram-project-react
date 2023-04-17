from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.models import (Favorite, Ingredients, Recipe, RecipeIngredients,
                             ShoppingCart, Tag)

from .filters import RecipeFilter
from .pagination import CustomPagination
from .serializers import (CreateUpdateRecipeSerializer, IngredientsSerializer,
                          RecipeSerializer, TagSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by("id")
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action is "create" or "partial_update":
            return CreateUpdateRecipeSerializer
        return RecipeSerializer

    @staticmethod
    def add_favorite(request, pk):
        if Favorite.objects.filter(user=request.user.pk, recipe=pk).exists():
            return Response(
                {"errors": "Рецепт уже добавлен в избранное"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recipe = Recipe.objects.get(id=pk)
        Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        return Response(
            {"alert": "Рецепт добавлен в избранное"}, status=status.HTTP_201_CREATED
        )

    @staticmethod
    def delete_favorite(request, pk):
        favorite_recipe = Favorite.objects.filter(user=request.user.pk, recipe=pk)
        if favorite_recipe.exists():
            favorite_recipe.delete()
            return Response(
                {"alert": "Рецепт убран из избранного"},
                status=status.HTTP_204_NO_CONTENT,
            )

    @staticmethod
    def add_in_shopping_cart(request, pk):
        if ShoppingCart.objects.filter(user=request.user.pk, recipe=pk).exists():
            return Response(
                {"errors": "Рецепт уже добавлен в список покупок"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recipe = Recipe.objects.get(id=pk)
        ShoppingCart.objects.get_or_create(user=request.user, recipe=recipe)
        return Response(
            {"alert": "Рецепт добавлен в список покупок"},
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def delete_from_shopping_cart(request, pk):
        recipe = ShoppingCart.objects.filter(user=request.user.pk, recipe=pk)
        if recipe.exists():
            recipe.delete()
            return Response(
                {"alert": "Рецепт убран из списка покупок"},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(methods=("POST", "DELETE"), detail=True, permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        if request.method == "POST":
            return self.add_favorite(request, pk)

        return self.delete_favorite(request, pk)

    @action(methods=("POST", "DELETE"), detail=True, permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        if request.method == "POST":
            return self.add_in_shopping_cart(request, pk)

        return self.delete_from_shopping_cart(request, pk)

    @action(methods=("GET",), detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredients.objects.filter(
                recipe__recipes_in_shopping_cart__user=request.user
            )
                .values("ingredient__name", "ingredient__measurement_unit")
                .annotate(amount=Sum("amount"))
        )

        shopping_cart = [
            f' {ingredient["ingredient__name"]} ({ingredient["ingredient__measurement_unit"]}) — {ingredient["amount"]}'
            for ingredient in ingredients
        ]

        filename = "shopping_cart.txt"
        response = HttpResponse(shopping_cart, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response
