from rest_framework.routers import DefaultRouter
from django.urls import include, path, re_path
from api.views import UserViewSet, TagViewSet, IngredientsViewSet

app_name = 'api'
router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('users', UserViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
