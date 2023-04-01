from django.contrib import admin
from .models import Tag, Ingredients, Recipe, RecipeTag, RecipeIngredients, Favorite, ShoppingCart
from users.models import User, Follow


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    search_fields = ('name', 'author', 'tags')

    def count_favorites(self, obj):
        return obj.favorite_recipes.count()

    count_favorites.short_description = 'Добавлено в избранное'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email')


admin.site.register(Tag)
admin.site.register(RecipeTag)
admin.site.register(Favorite)
admin.site.register(RecipeIngredients)
admin.site.register(ShoppingCart)
admin.site.register(Follow)