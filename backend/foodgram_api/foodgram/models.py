from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель тега"""

    name = models.CharField(
        verbose_name="Название тега",
        max_length=256,
    )
    color = models.CharField(
        verbose_name="Цвет",
        max_length=256,
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Модель ингредиента"""

    MESURES = (
        ("килограмм", "кг"),
        ("миллилитр", "мл"),
        ("грамм", "г"),
        ("столовая ложка", "ст. л."),
    )

    name = models.CharField(
        verbose_name="Название ингредиента",
        max_length=256,
    )
    measurement_unit = models.CharField(
        verbose_name="Единицы измерения", max_length=256, choices=MESURES
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through="RecipeIngredients",
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        through="RecipeTag",
        verbose_name="Теги",
    )
    image = models.ImageField(upload_to="recipes/", verbose_name="Картинка")
    name = models.CharField(
        verbose_name="Название рецепта",
        max_length=256,
    )
    text = models.TextField(verbose_name="Описание рецепта")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления в минутах",
        default=0,
        validators=(
            MinValueValidator(1, "Время не может быть меньше одной минуты"),
        ),
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    """Промежуточная модель между рецептом и тегом"""

    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="tags", verbose_name="Тег"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipes", verbose_name="Рецепт"
    )

    class Meta:
        verbose_name = "Рецепт и тег"
        verbose_name_plural = "Рецепты и теги"

    def __str__(self):
        return f"{self.tag} тег рецепта {self.recipe}"


class RecipeIngredients(models.Model):
    """Промежуточная модель между рецептом и ингредиентом"""

    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name="ingredient",
        verbose_name="Ингредиенты",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe", verbose_name="Рецепт"
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество",
    )

    class Meta:
        verbose_name = "Рецепт и ингредиент"
        verbose_name_plural = "Рецепты и ингредиенты"

    def __str__(self):
        return f"Ингредиент {self.ingredient} в рецепте {self.recipe}"


class Favorite(models.Model):
    """Модель для работы с избранными рецептами"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite_recipes"
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("user", "recipe"), name="unique_favorite"),
        )
        verbose_name = "Избранное"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user} добавил в избранное {self.recipe}"


class ShoppingCart(models.Model):
    """Модель для работы со списком покупок"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shopping_cart"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipes_in_shopping_cart"
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_cart"
            ),
        )
        verbose_name = "Лист покупок"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user} добавил {self.recipe} в список покупок"
