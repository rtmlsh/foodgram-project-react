from rest_framework import serializers
from foodgram.models import Tag, Ingredients, Recipe


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

    tags = serializers.StringRelatedField(many=True, read_only=True)
    ingredients = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('author', 'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')
