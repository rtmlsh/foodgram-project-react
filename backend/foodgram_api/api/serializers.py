from rest_framework import serializers
from foodgram.models import Tag, Ingredients, Recipe, RecipeTag, Favorite, ShoppingCart, RecipeIngredients
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from users.models import User
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
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для чтения"""

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


class AddIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор добавления ингредиентов"""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
        validators=[UniqueValidator(queryset=Ingredients.objects.all())]
    )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class CreateUpdateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для добавления и редактирования"""

    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = AddIngredientsSerializer(many=True)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ('author', 'ingredients', 'tags', 'name', 'text', 'cooking_time')

    def validate_tags(self, value):
        if not value:
            raise ValidationError(
                {'error': 'Для создания рецепта нужно выбрать теги'})

    def validate_ingredients(self, value):
        if not value:
            raise ValidationError(
                {'error': 'Для создания рецепта нужно выбрать ингредиенты'})

    def add_tags(self, recipe, tags):
        for tag in tags:
            recipe.tags.add(tag)
        return recipe

    def add_ingredients(self, ingredients, tags, recipe):
        recipe = self.add_tags(recipe, tags)

        for ingredient in ingredients:
            RecipeIngredients.objects.update_or_create(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['id']
            )
        return recipe

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        if Recipe.objects.filter(**validated_data).exists():
            raise ValidationError(
                {'error': 'Рецепт уже создан'})

        recipe = Recipe.objects.create(**validated_data)
        recipe = self.add_ingredients(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.ingredients.clear()
        self.add_ingredients(ingredients, tags, instance)
        recipe = super().update(instance, validated_data)
        return recipe


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор данных юзера"""

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        model = User
