import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers, status
from rest_framework.validators import UniqueValidator

from recipes.models import IngredientItem, RecipeTag, Dish, DishIngredient, FavoriteRecipe, ShoppingList


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate(self, attrs):
        try:
            email = self.initial_data['email']
            username = self.initial_data['username']
        except KeyError:
            raise exceptions.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        if username == 'me':
            raise exceptions.ValidationError(
                f'Имя - {username} запрещено использовать для регистрации',
                code=status.HTTP_400_BAD_REQUEST)
        if re.match('^[\\w.@+-]+\\Z', username) is None:
            raise exceptions.ValidationError(
                'Имя пользователя не соответствует шаблону',
                code=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(username=username).first()
        if user and user.email != email:
            raise exceptions.ValidationError(
                f'Пользователь с username = {username} уже зарегистрирован',
                code=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if user and user.username != username:
            raise exceptions.ValidationError(
                f'Пользователь с email = {email} уже зарегистрирован',
                code=status.HTTP_400_BAD_REQUEST)
        return super().validate(attrs)


class TokenSerializator(serializers.ModelSerializer):
    """Сериализатор для авторизации пользователя и выдачи ему токена."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=32)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        try:
            username = data['username']
            confirmation_code = data['confirmation_code']
        except KeyError:
            raise exceptions.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(
            User, username=username)
        if user.confirmation_code != confirmation_code:
            raise exceptions.ValidationError('Неверный код подтверждения.',
                                             code=status.HTTP_400_BAD_REQUEST)
        return data


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователем."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
        max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
        )


class MeSerializer(UsersSerializer):
    """Сериализатор для работы пользователя со своими данными."""
    role = serializers.CharField(read_only=True)
    
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

