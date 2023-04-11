from djoser.views import UserViewSet
from .serializers import CustomUserSerializer
from .models import User
from api.pagination import CustomPagination


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
