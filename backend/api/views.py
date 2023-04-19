from api.filters import IngredientFilter, RecipeFilter
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as UsersViewSet
from recipes.models import (Basket, Favorites, Ingredient, Recipe,
                            RecipeIngredients, Tag)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import MyUser, Subscriptions
from utils.helper import cart_to_pdf_dump, create_or_delete
from utils.paginators import RecipePagination, UsersPagination

from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, TagSerializer, UserSerializer,
                          UserSubscribersSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class UserViewSet(UsersViewSet):
    serializer_class = UserSerializer
    pagination_class = UsersPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(methods=['get'], detail=False)
    def subscriptions(self, request, pk=None):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipes_limit = self.request.query_params.get('recipes_limit', 6)
        user = self.request.user
        subscriptions = MyUser.objects.filter(followee__user=user)
        pages = self.paginate_queryset(subscriptions)
        serializer = UserSubscribersSerializer(pages, many=True,
                                               context={'request': request,
                                                        'recipes_limit':
                                                        recipes_limit})
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = self.request.user
        author = MyUser.objects.get(pk=id)
        if request.method == 'POST':
            subscription, created = Subscriptions.objects.get_or_create(
                user=user, author=author)
            if created:
                serializer = UserSubscribersSerializer(
                    author, many=False, context={'request': request,
                                                 'recipes_limit': 1})
                return Response(serializer.data)
            return Response({'message': 'Вы уже подписаны!'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            obj = get_object_or_404(Subscriptions, user=user, author=author)
            obj.delete()
            return Response({'message': 'Отписка произведена успешно!'})

    def get_serializer_context(self):
        user = self.request.user
        context = super().get_serializer_context()
        subscriptions = set(Subscriptions.objects.filter(user_id=user.pk).
                            values_list('author_id', flat=True))
        context.update({'subscriptions': subscriptions})
        return context

class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return RecipeCreateSerializer
        else:
            return RecipeSerializer

    def get_serializer_context(self):
        user = self.request.user
        context = super().get_serializer_context()
        is_favorited = set(Favorites.objects.filter(author_id=user.pk).
                           values_list('recipe_id', flat=True))
        is_in_shopping_cart = set(Basket.objects.filter(author_id=user.pk).
                                  values_list('recipe_id', flat=True))
        context.update({'favorited': is_favorited,
                        'shopping_cart': is_in_shopping_cart})
        return context

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return create_or_delete(pk, request, Favorites)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return create_or_delete(pk, request, Basket)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        query = (RecipeIngredients.objects.filter(recipe__in_cart__author=user)
                 .values('ingredients__name', 'ingredients__measurement_unit')
                 .annotate(amount=Sum('amount')))
        return cart_to_pdf_dump(query)
