from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from slugify import slugify


class AddSlugNameFieldsModel(models.Model):
    """Абстрактная базовая модель."""

    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        """Генерирует slug из названия, если он не указан."""
        if not self.slug:
            self.slug = slugify(self.title)
        super(AddSlugNameFieldsModel, self).save(*args, **kwargs)

    class Meta:
        """Мета класс абстрактной базовой модели."""

        abstract = True
        ordering = ('title',)

    def __str__(self):
        """Описание объекта."""
        return self.title


class IngredientItem(AddSlugNameFieldsModel):
    """Модель для ингредиента."""

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


class RecipeTag(AddSlugNameFieldsModel):
    """Модель для тега."""

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Dish(models.Model):
    """Модель для рецепта."""

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
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
