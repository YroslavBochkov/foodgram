from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import IngredientItem, RecipeTag, Dish, DishIngredient, FavoriteRecipe, ShoppingList
from users.forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


@admin.register(IngredientItem)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit_of_measurement')  # Отображаем название и единицу измерения
    search_fields = ('title',)  # Поиск по названию
    ordering = ('title',)  # Сортировка по названию

@admin.register(RecipeTag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')  # Отображаем название и slug
    search_fields = ('title',)  # Поиск по названию
    ordering = ('title',)  # Сортировка по названию

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'publication_date', 'cooking_duration', 'get_favorited_count')  # Добавлено поле для избранного
    search_fields = ('name', 'creator__username')  # Поиск по названию и имени пользователя
    list_filter = ('tags',)  # Фильтрация по тегам
    ordering = ('-publication_date',)  # Сортировка по дате публикации

    def get_favorited_count(self, obj):
        """Возвращает количество добавлений рецепта в избранное."""
        return FavoriteRecipe.objects.filter(dish=obj).count()  # Подсчет избранных рецептов
    get_favorited_count.short_description = 'Количество добавлений в избранное'  # Название столбца

class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1  # Количество пустых форм для добавления

@admin.register(DishIngredient)
class DishIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity', 'dish')  # Отображаем ингредиент, количество и рецепт
    list_filter = ('dish',)  # Фильтрация по рецепту
    ordering = ('dish',)  # Сортировка по рецепту

@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish')  # Отображаем пользователя и избранный рецепт
    list_filter = ('user',)  # Фильтрация по пользователю
    ordering = ('user',)  # Сортировка по пользователю

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish')  # Отображаем пользователя и рецепт из списка покупок
    list_filter = ('user',)  # Фильтрация по пользователю
    ordering = ('user',)  # Сортировка по пользователю
