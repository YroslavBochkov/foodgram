from rest_framework import serializers
from recipes.models import IngredientItem, RecipeTag, Dish, DishIngredient, FavoriteRecipe, ShoppingList

class IngredientItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientItem
        fields = ['id', 'title', 'unit_of_measurement']

class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeTag
        fields = ['id', 'title', 'slug']

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'photo', 'preparation_method', 'publication_date', 'cooking_duration', 'creator']

class DishIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishIngredient
        fields = ['id', 'dish', 'ingredient', 'quantity']

class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ['id', 'user', 'dish']

class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ['id', 'user', 'dish']


