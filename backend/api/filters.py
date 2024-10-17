from django.contrib.auth import get_user_model
from django_filters import FilterSet, filters
from recipes.models import RecipeTag, Dish, IngredientItem

User = get_user_model()

class RecipeTagFilter(FilterSet):
    """Фильтр для модели тега."""
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=RecipeTag.objects.all(),
    )

    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = RecipeTag
        fields = ('tags',)  # Убедитесь, что здесь нет поля author

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)
        return queryset


class IngredientItemFilter(FilterSet):
    """Фильтр для модели ингредиента."""
    title = filters.CharFilter(field_name='title', lookup_expr='startswith')  # Фильтр по названию

    class Meta:
        model = IngredientItem
        fields = ['title']  # Убедитесь, что здесь указаны правильные поля

class RecipeFilter(FilterSet):
    """Фильтр для модели рецепта."""
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')  # Фильтр по названию рецепта
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=RecipeTag.objects.all(),
    )

    class Meta:
        model = Dish
        fields = ['name', 'tags']  # Убедитесь, что здесь указаны правильные поля



    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)
        return queryset
