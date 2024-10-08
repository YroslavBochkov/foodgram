from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from slugify import slugify


class Ingredient(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='Unique name and measurement units combo',
            ),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
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
        if not self.slug:
            self.slug = slugify(self.name)  # Генерация slug на основе названия
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка',
    )
    description = models.TextField(verbose_name='Способ приготовления')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги', related_name='Tags',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (минуты)',
        validators=(MinValueValidator(limit_value=1),),
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )


    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipeingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='recipeingredients',
    )
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_ingredient_for_a_recipe',
            ),
        )
    
    def __str__(self):
        return (
            f'{self.ingredient.name}, {self.amount}'
            f'{self.ingredient.measurement_unit} for {self.recipe}'

        )


class Favorite(models.Model):
    """Избранное"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name='Избранное',
        verbose_name='Закладки',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, 
        related_name='Избранное',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_for_a_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в Избранное'


class ShoppingCart(models.Model):
    """Список покупок"""
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='Список покупок',
        verbose_name='Покупатель',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='Список покупок',
        verbose_name='Рецепт из списка покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user','recipe'),
                name='unique_user_for_a_recipe_in_cart',
            ),
        )

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в Список покупок'
