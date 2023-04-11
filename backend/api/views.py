from recipes.models import Tag, Ingredient, Recipe, Favorites
from rest_framework.viewsets import ReadOnlyModelViewSet
from djoser.views import UserViewSet as UsersViewSet
from .serializers import (TagSerializer, UserSerializer,
                          UserSubscribersSerializer, IngredientSerializer,
                          RecipeSerializer)
from users.models import MyUser, Subscription
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.paginators import UsersPagination, RecipePagination
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

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


class RecipeViewSet(ModelViewSet):
    pagination_class = RecipePagination
    serializer_class = RecipeSerializer

    def get_queryset(self):
        SEARCH_PARAMS = ('1', 'true')
        queryset = Recipe.objects.select_related('author')
        is_favorited = self.get_serializer_context()['is_favorited']
        print(is_favorited)
        tags = self.request.query_params.getlist('tags')
        author = self.request.query_params.get('author')
        is_in_shopping_cart = self.get_serializer_context()[
            'is_in_shopping_cart']
        user = self.request.user
        if tags:
            queryset = queryset.filter(tags__slug__in=tags)
        if is_favorited in SEARCH_PARAMS:
            queryset = queryset.filter(favorite_recipes__author=user)
        if is_in_shopping_cart in SEARCH_PARAMS:
            queryset = queryset.filter(in_cart__author=user)
        if author:
            queryset = queryset.filter(author__username=author)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        context.update({'request': self.request, 'is_favorited': is_favorited,
                        'is_in_shopping_cart': is_in_shopping_cart})
        
        return context
