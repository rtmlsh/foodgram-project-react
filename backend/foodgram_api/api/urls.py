from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientsViewSet, RecipeViewSet


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]