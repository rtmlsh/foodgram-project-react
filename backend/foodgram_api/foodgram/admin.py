from django.contrib import admin
from .models import Tag, Ingredients, Recipe, RecipeTag, RecipeIngredients


admin.site.register(Tag)
admin.site.register(Ingredients)
admin.site.register(Recipe)
admin.site.register(RecipeTag)
admin.site.register(RecipeIngredients)


