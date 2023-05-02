from django.contrib import admin

from users.models import Follow, User

from .models import (Favorite, Ingredients, Recipe, RecipeIngredients,
                     RecipeTag, ShoppingCart, Tag)


class IngredientsInline(admin.StackedInline):
    model = Ingredients


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "count_favorites")
    search_fields = ("name", "author", "tags")
    inlines = [IngredientsInline]

    def count_favorites(self, obj):
        return obj.favorite_recipes.count()

    count_favorites.short_description = "Добавлено в избранное"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("username", "email")


admin.site.register(Tag)
admin.site.register(RecipeTag)
admin.site.register(Favorite)
admin.site.register(RecipeIngredients)
admin.site.register(ShoppingCart)
admin.site.register(Follow)
