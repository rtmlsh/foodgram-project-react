from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import CustomPagination

from .models import Follow, User
from .serializers import CustomUserSerializer, FollowSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @staticmethod
    def add_subscriber(request, author, subscribe):
        if subscribe.exists():
            return Response(
                {"errors": "Автор уже добавлен в подписки"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Follow.objects.get_or_create(user=request.user, following=author)
        return Response(
            {"alert": "Автор добавлен в подписки"}, status=status.HTTP_201_CREATED
        )

    @staticmethod
    def delete_subscriber(subscribe):
        if subscribe.exists():
            subscribe.delete()
            return Response(
                {"alert": "Автор убран из подписок"},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(
        methods=("POST", "DELETE"), detail=True, permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get("id"))
        subscribe = Follow.objects.filter(user=request.user, following=author)
        if request.method == "POST":
            return self.add_subscriber(request, author, subscribe)
        else:
            return self.delete_subscriber(subscribe)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
