from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(
        verbose_name='Название тега',
        max_length=256,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=256,
    )
    slug = models.SlugField(unique=True)


class Ingredients(models.Model):
    """Модель ингредиента"""
    MESURES = (
        ('kilo', 'kg'),
        ('milliliter', 'ml'),
        ('gram', 'gr'),
    )

    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=256,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=256,
        choices=MESURES
    )


class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredients',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка')
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=256,
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        default=0,
        validators=[
            MinValueValidator(1, 'Время не может быть меньше одной минуты'),
        ],
    )


class RecipeTag(models.Model):
    """Промежуточная модель между рецептом и тегом"""
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Тег'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )


class RecipeIngredients(models.Model):
    """Промежуточная модель между рецептом и ингредиентом"""
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиенты'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепт'
    )
