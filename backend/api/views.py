from recipes.models import Tag
from rest_framework.viewsets import ReadOnlyModelViewSet
from djoser.views import UserViewSet as UsersViewSet
from .serializers import TagSerializer, UserSerializer
from rest_framework import serializers
from users.models import MyUser, Subscription
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.paginators import UsersPagination

class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes


class UserViewSet(UsersViewSet):
    serializer_class = UserSerializer
    pagination_class = UsersPagination
