from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientItemViewSet, DishViewSet, RecipeTagViewSet

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientItemViewSet)
router.register('tags', RecipeTagViewSet)
router.register('recipes', DishViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
