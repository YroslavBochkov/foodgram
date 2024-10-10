from rest_framework import generics
from recipes.models import IngredientItem, RecipeTag, Dish, DishIngredient, FavoriteRecipe, ShoppingList
from recipes.models import CustomUser
from .serializers import IngredientItemSerializer, RecipeTagSerializer, DishSerializer, DishIngredientSerializer, FavoriteRecipeSerializer, ShoppingListSerializer, CustomUserSerializer


class IngredientItemList(generics.ListCreateAPIView):
    queryset = IngredientItem.objects.all()
    serializer_class = IngredientItemSerializer

class IngredientItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IngredientItem.objects.all()
    serializer_class = IngredientItemSerializer

class RecipeTagList(generics.ListCreateAPIView):
    queryset = RecipeTag.objects.all()
    serializer_class = RecipeTagSerializer

class RecipeTagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeTag.objects.all()
    serializer_class = RecipeTagSerializer

class DishList(generics.ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class DishDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class DishIngredientList(generics.ListCreateAPIView):
    queryset = DishIngredient.objects.all()
    serializer_class = DishIngredientSerializer

class DishIngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DishIngredient.objects.all()
    serializer_class = DishIngredientSerializer

class FavoriteRecipeList(generics.ListCreateAPIView):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer

class FavoriteRecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer

class ShoppingListList(generics.ListCreateAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

class ShoppingListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

class UserDetail(generics.RetrieveAPIView):
    """Представление для получения информации о пользователе."""
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
