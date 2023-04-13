from djoser.serializers import UserSerializer
from rest_framework.fields import SerializerMethodField

from .models import Follow, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, following):
        user = self.context.get('request').user
        return Follow.objects.filter(user=user, following=following).exists()


class FollowSerializer(UserSerializer):
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, following):
        user = self.context.get('request').user
        return Follow.objects.filter(user=user, following=following).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        return obj.recipes.all()