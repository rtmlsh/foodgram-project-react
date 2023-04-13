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
    queryset = User.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(methods=['POST', 'DELETE'], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        subscribe = Follow.objects.filter(user=request.user, following=author)

        if subscribe.exists():
            if request.method == 'DELETE':
                subscribe.delete()
                return Response({'alert': 'Автор убран из подписок'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Автор уже добавлен в подписки'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            Follow.objects.get_or_create(user=request.user, following=author)
            return Response({'alert': 'Автор добавлен в подписки'}, status=status.HTTP_201_CREATED)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
