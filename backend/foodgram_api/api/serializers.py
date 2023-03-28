from rest_framework import serializers
from foodgram.models import Tag, Ingredients, Recipe, RecipeTag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientsSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('author', 'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')


class RecipeTagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов у рецептов"""

    class Meta:
        model = RecipeTag
        fields = ('tag', 'recipe')

