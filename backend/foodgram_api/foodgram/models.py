from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"{self.tag} тег рецепта {self.recipe}"


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

    def __str__(self):
        return f"Ингредиент {self.ingredient} в рецепте {self.recipe}"


class Favorite(models.Model):
    """Модель для работы с избранными рецептами"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorite_recipes')

    def __str__(self):
        return f"{self.user} добавил в избранное {self.recipe}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_favorite"
            )
        ]


class ShoppingCart(models.Model):
    """Модель для работы со списком покупок"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} добавил {self.recipe} в список покупок"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_shopping_cart"
            )
        ]