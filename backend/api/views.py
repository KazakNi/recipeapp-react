from recipes.models import Tag, Ingredient
from rest_framework.viewsets import ReadOnlyModelViewSet
from djoser.views import UserViewSet as UsersViewSet
from .serializers import (TagSerializer, UserSerializer,
                          UserSubscribersSerializer, IngredientSerializer)
from users.models import MyUser, Subscription
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.paginators import UsersPagination
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import generics
from rest_framework import status

class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination
    # permission_classes


class UserViewSet(UsersViewSet):
    serializer_class = UserSerializer
    pagination_class = UsersPagination

    @action(methods=['get'], detail=True)
    def subscriptions(self, request, pk=None):
        recipes_limit = self.request.query_params.get('recipes_limit', 5)
        user = self.request.user
        if request.method == 'GET':
            subscriptions = MyUser.objects.filter(followee__user=user)
            serializer = UserSubscribersSerializer(subscriptions, many=True,
                                                   context={'request': request,
                                                            'recipes_limit':
                                                            recipes_limit})
            return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id=None):
        user = self.get_object()
        author = MyUser.objects.get(pk=id)
        if request.method == 'POST':
            subscription, created = Subscription.objects.get_or_create(
                user=user, author=author)
            if created:
                instance = MyUser.objects.get(followee__author=author)
                serializer = UserSubscribersSerializer(
                    instance, many=False, context={'request': request,
                                                   'recipes_limit': 1})
                return Response(serializer.data)
            return Response({'message': 'Вы уже подписаны!'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            obj = get_object_or_404(Subscription, user=user, author=author)
            obj.delete()
            return Response({'message': 'Отписка произведена успешно!'})


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']