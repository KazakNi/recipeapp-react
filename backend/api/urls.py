from api.views import (IngredientsViewSet, RecipeViewSet, TagViewSet,
                       UserViewSet)
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

app_name = 'api'
router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('users', UserViewSet, basename='users')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
