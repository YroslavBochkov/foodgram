from api.fields import Base64ImageField
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import serializers
from users.models import Subscription

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password')
        extra_kwargs = {'password': {'write_only': True}}


class BaseCustomUserSerializer(UserSerializer):
    """Базовый сериализатор для пользователя с дополнительным полем."""
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на данного автора."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, author=obj).exists()
        return False


class CustomUserSerializer(BaseCustomUserSerializer):
    """Сериализатор для пользователя с аватаром."""
    avatar = Base64ImageField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
            'avatar',
        )

    def validate(self, attrs):
        """Проверяет наличие аватара в данных."""
        request = self.context.get('request')
        if request and 'avatar' not in attrs or attrs.get('avatar') is None:
            raise serializers.ValidationError('Отсутствует поле "avatar"')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        """Обновляет данные пользователя, включая аватар."""
        if avatar := validated_data.get('avatar', None):
            if instance.avatar:
                instance.avatar.delete()
            instance.avatar = avatar
        return super().update(instance, validated_data)


class UserSubscriptionSerializer(BaseCustomUserSerializer):
    """Сериализатор для подписки на пользователя."""
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
            'avatar',
            'recipes_count',
            'recipes',
        )

    def get_recipes(self, obj):
        """Возвращает рецепты автора с учетом лимита."""
        queryset = obj.recipes.all()
        if limit := self.context.get('recipes_limit'):
            queryset = queryset[: int(limit)]
        return RecipeDemoSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """Возвращает количество рецептов автора."""
        return obj.recipes.count()


class CustomUserPasswordSerializer(serializers.Serializer):
    """Сериализатор для изменения пароля пользователя."""
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, validators=[validate_password])

    def validate(self, data):
        """Проверяет правильность текущего пароля."""
        user = self.context['request'].user
        if not user.check_password(data.get('current_password')):
            raise serializers.ValidationError(
                'Неравильный пароль.')
        return data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов рецепта."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeDemoSerializer(serializers.ModelSerializer):
    """Сериализатор для мини-информации о рецепте."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, required=True, source='recipeingredient_set')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_ingredients(self, value):
        """Проверяет наличие ингредиентов и их уникальность."""
        if not value:
            raise serializers.ValidationError('Укажите ингредиенты.')
        ingredient_ids = set()
        for ingredient in value:
            ingredient_id = ingredient['ingredient']['id']
            if ingredient_id in ingredient_ids:
                raise serializers.ValidationError(
                    'Ингредиенты не могут повторяться.')
            ingredient_ids.add(ingredient_id)
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError('Ингредиент отсуствует.')
        return value

    def validate_tags(self, value):
        """Проверяет наличие тегов и их уникальность."""
        if not value:
            raise serializers.ValidationError('Укажите тег.')
        tags = set()
        for tag in value:
            if tag in tags:
                raise serializers.ValidationError(
                    'Тэги не могут повторяться.')
            tags.add(tag)
        return value

    def recipe_ingredients_create(self, recipe, ingredients_data):
        """Создает ингредиенты для рецепта."""
        recipe_ingredients_to_create = [
            RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient_data['ingredient']['id'],
                amount=ingredient_data['amount'])
            for ingredient_data in ingredients_data
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients_to_create)

    @transaction.atomic
    def create(self, validated_data):
        """Создает новый рецепт."""
        ingredients_data = validated_data.pop('recipeingredient_set')
        tags_data = validated_data.pop('tags')
        image_data = validated_data.pop('image')

        recipe = Recipe.objects.create(**validated_data)
        recipe.image.save(image_data.name, image_data, save=True)

        self.recipe_ingredients_create(recipe, ingredients_data)

        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):
        """Обновляет существующий рецепт."""
        tags_data = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('recipeingredient_set', None)

        self.validate_ingredients(ingredients_data)
        self.validate_tags(tags_data)

        instance = super().update(instance, validated_data)

        if tags_data is not None:
            instance.tags.set(tags_data)

        if ingredients_data is not None:
            instance.recipeingredient_set.all().delete()
            self.recipe_ingredients_create(instance, ingredients_data)

        return instance

    def to_representation(self, instance):
        """Преобразует представление рецепта для ответа."""
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(
            instance.tags.all(), many=True).data
        return representation

    def get_is_favorited(self, obj):
        """Проверяет, добавлен ли рецепт в избранное."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(
                user=request.user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        """Проверяет, находится ли рецепт в корзине покупок."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=request.user, recipe=obj).exists()
        return False
