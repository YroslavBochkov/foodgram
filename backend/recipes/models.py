import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from slugify import slugify


class IngredientItem(models.Model):
    """Модель для ингредиента."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название ингредиента',
    )
    unit_of_measurement = models.CharField(
        max_length=100,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'unit_of_measurement'),
                name='unique_ingredient_combination',
            ),
        )

    def __str__(self):
        return f'{self.title}, {self.unit_of_measurement}'


class RecipeTag(models.Model):
    """Модель для тега."""

    title = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        unique=True,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def save(self, *args, **kwargs):
        if not self.slug:  # Генерация slug, если он не указан
            self.slug = slugify(self.title)  # Генерация slug на основе названия
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Dish(models.Model):
    """Модель для рецепта."""

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='dishes',
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    photo = models.ImageField(
        upload_to='dishes/images/',
        verbose_name='Картинка',
    )
    preparation_method = models.TextField(verbose_name='Способ приготовления')
    publication_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    ingredients = models.ManyToManyField(
        IngredientItem, through='DishIngredient',
        verbose_name='Ингредиенты',
        related_name='dishes',
    )
    tags = models.ManyToManyField(
        RecipeTag, verbose_name='Теги', related_name='tags',
    )
    cooking_duration = models.PositiveIntegerField(
        verbose_name='Время приготовления (минуты)',
        validators=(MinValueValidator(limit_value=1),),
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-publication_date', )

    def __str__(self):
        return self.title


class DishIngredient(models.Model):
    """Связь между рецептом и ингредиентом."""

    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name='dish_ingredients',
    )
    ingredient = models.ForeignKey(
        IngredientItem, on_delete=models.CASCADE,
        related_name='ingredient_dishes',
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = (
            models.UniqueConstraint(
                fields=('dish', 'ingredient'),
                name='unique_ingredient_in_dish',
            ),
        )

    def __str__(self):
        return f'{self.ingredient.title}, {self.quantity} {self.ingredient.unit_of_measurement} для {self.dish.title}'


class FavoriteRecipe(models.Model):
    """Модель для избранных рецептов."""
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Закладки',
    )
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'dish'),
                name='unique_user_favorite_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} добавил {self.dish} в Избранное'


class ShoppingList(models.Model):
    """Модель для списка покупок."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='Покупатель',
    )
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE,
        related_name='in_shopping_lists',
        verbose_name='Рецепт из списка покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'dish'),
                name='unique_user_shopping_list_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} добавил {self.dish} в Список покупок'
