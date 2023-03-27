from rest_framework import viewsets
from foodgram.models import Tag, Ingredients, Recipe
from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer
from rest_framework import filters


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
