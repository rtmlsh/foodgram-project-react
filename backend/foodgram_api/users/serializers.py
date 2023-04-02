from rest_framework import serializers
from .models import User


сlass UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ('id', 'name', 'color', 'slug')