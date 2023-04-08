from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from foodgram.models import Tag, Ingredients, Recipe, Favorite, ShoppingCart, RecipeIngredients
from rest_framework.decorators import action
from rest_framework.response import Response
from .pagination import RecipesPagination
from .filters import RecipeFilter

from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer, CreateUpdateRecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('id')
    serializer_class = RecipeSerializer
    pagination_class = RecipesPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action is 'create' or 'partial_update':
            return CreateUpdateRecipeSerializer
        return RecipeSerializer

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

    # @action(methods=['GET'], detail=True)
    # def download_shopping_cart(self, request):
    #     ingredients = RecipeIngredients.objects.filter(recipes__shopping_cart__user=request.user).values(
    #         'ingredient__name',
    #         'ingredient__measurement_unit'
    #     ).annotate(amount=Sum('amount'))

