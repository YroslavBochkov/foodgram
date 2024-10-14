from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import (
    IngredientItemList, IngredientItemDetail,
    RecipeTagList, RecipeTagDetail,
    DishList, DishDetail,
    DishIngredientList, DishIngredientDetail,
    FavoriteRecipeList, FavoriteRecipeDetail,
    ShoppingListList, ShoppingListDetail,
    UserDetail,
)

# Создаем роутер
router = SimpleRouter()

# Регистрируем маршруты для моделей
router.register('ingredients', IngredientItemList, basename='ingredient')
router.register('tags', RecipeTagList, basename='tag')
router.register('dishes', DishList, basename='dish')
router.register('dish-ingredients', DishIngredientList, basename='dish-ingredient')
router.register('favorite-recipes', FavoriteRecipeList, basename='favorite-recipe')
router.register('shopping-lists', ShoppingListList, basename='shopping-list')

# Определяем urlpatterns
urlpatterns = [
    path('api/', include(router.urls)),  # Подключаем маршруты API
    path('api/ingredients/<int:pk>/', IngredientItemDetail.as_view(), name='ingredient-detail'),
    path('api/tags/<int:pk>/', RecipeTagDetail.as_view(), name='tag-detail'),
    path('api/dishes/<int:pk>/', DishDetail.as_view(), name='dish-detail'),
    path('api/dish-ingredients/<int:pk>/', DishIngredientDetail.as_view(), name='dish-ingredient-detail'),
    path('api/favorite-recipes/<int:pk>/', FavoriteRecipeDetail.as_view(), name='favorite-recipe-detail'),
    path('api/shopping-lists/<int:pk>/', ShoppingListDetail.as_view(), name='shopping-list-detail'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),  # Добавляем маршрут для пользователя
]
