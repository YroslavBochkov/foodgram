from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                       TagViewSet)

app_name = 'api'  # Имя приложения для использования в пространстве имен URL

# Создание маршрутизатора для API
router_v1 = DefaultRouter()
# Регистрация маршрутов для пользователей
router_v1.register('users', CustomUserViewSet, basename='users')
# Регистрация маршрутов для тегов
router_v1.register('tags', TagViewSet, basename='tags')
# Регистрация маршрутов для ингредиентов
router_v1.register('ingredients', IngredientViewSet, basename='ingredient')
# Регистрация маршрутов для рецептов
router_v1.register('recipes', RecipeViewSet, basename='recipe')

# Определение конечных точек версии 1 API
v1_endpoints = [
    path('', include(router_v1.urls)),  # Включение маршрутов из маршрутизатора
    # Включение маршрутов аутентификации Djoser
    path('auth/', include('djoser.urls')),
    # Включение маршрутов для токенов аутентификации Djoser
    path('auth/', include('djoser.urls.authtoken')),
]

# Определение окончательных маршрутов для API
urlpatterns = [
    path('', include(v1_endpoints)),  # Включение конечных точек версии 1 API
]
