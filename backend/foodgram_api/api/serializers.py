from rest_framework import serializers
from foodgram.models import Tag, Ingredients, Recipe, RecipeTag, Favorite, User, ShoppingCart
from rest_framework.fields import SerializerMethodField


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
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('author', 'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        return Favorite.objects.filter(user=user.is_authenticated, recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        return ShoppingCart.objects.filter(user=user.is_authenticated, recipe=recipe).exists()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор данных к юзерам."""

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        model = User
