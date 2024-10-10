from django.urls import path
from .views import (
    IngredientItemList, IngredientItemDetail,
    RecipeTagList, RecipeTagDetail,
    DishList, DishDetail,
    DishIngredientList, DishIngredientDetail,
    FavoriteRecipeList, FavoriteRecipeDetail,
    ShoppingListList, ShoppingListDetail,
    UserDetail,
)

urlpatterns = [
    path('api/ingredients/', IngredientItemList.as_view(), name='ingredient-list'),
    path('api/ingredients/<int:pk>/', IngredientItemDetail.as_view(), name='ingredient-detail'),
    path('api/tags/', RecipeTagList.as_view(), name='tag-list'),
    path('api/tags/<int:pk>/', RecipeTagDetail.as_view(), name='tag-detail'),
    path('api/dishes/', DishList.as_view(), name='dish-list'),
    path('api/dishes/<int:pk>/', DishDetail.as_view(), name='dish-detail'),
    path('api/dish-ingredients/', DishIngredientList.as_view(), name='dish-ingredient-list'),
    path('api/dish-ingredients/<int:pk>/', DishIngredientDetail.as_view(), name='dish-ingredient-detail'),
    path('api/favorite-recipes/', FavoriteRecipeList.as_view(), name='favorite-recipe-list'),
    path('api/favorite-recipes/<int:pk>/', FavoriteRecipeDetail.as_view(), name='favorite-recipe-detail'),
    path('api/shopping-lists/', ShoppingListList.as_view(), name='shopping-list-list'),
    path('api/shopping-lists/<int:pk>/', ShoppingListDetail.as_view(), name='shopping-list-detail'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]