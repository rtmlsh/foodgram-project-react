from rest_framework import viewsets, mixins, status, permissions
from foodgram.models import Tag, Ingredients, Recipe, Favorite, ShoppingCart, User
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(methods=['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        favorite_recipe = Favorite.objects.filter(user=request.user.pk, recipe=pk)
        if favorite_recipe.exists():
            if request.method == 'DELETE':
                favorite_recipe.delete()
                return Response({'alert': 'Рецепт убран из избранного'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Рецепт уже добавлен в избранное'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            recipe = Recipe.objects.get(id=pk)
            Favorite.objects.get_or_create(user=request.user, recipe=recipe)
            return Response({'alert': 'Рецепт добавлен в избранное'}, status=status.HTTP_201_CREATED)

    @action(methods=['POST', 'DELETE'], detail=True)
    def shopping_cart(self, request, pk):
        recipe = ShoppingCart.objects.filter(user=request.user.pk, recipe=pk)
        if recipe.exists():
            if request.method == 'DELETE':
                recipe.delete()
                return Response({'alert': 'Рецепт убран из списка покупок'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Рецепт уже добавлен в список покупок'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            recipe = Recipe.objects.get(id=pk)
            ShoppingCart.objects.get_or_create(user=request.user, recipe=recipe)
            return Response({'alert': 'Рецепт добавлен в список покупок'}, status=status.HTTP_201_CREATED)
