from rest_framework import generics
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from recipes.models import IngredientItem, RecipeTag, Dish, DishIngredient, FavoriteRecipe, ShoppingList
from users.models import CustomUser
from rest_framework import filters, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import IngredientItemSerializer, RecipeTagSerializer, DishSerializer, DishIngredientSerializer, FavoriteRecipeSerializer, ShoppingListSerializer, CustomUserSerializer
from .utils import get_confirmation_code
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from .paginators import CustomPaginator
from .permissions import (IsAdminPermission)

User = get_user_model()


class SignUpViewSet(APIView):
    """Регистрируем пользователя и высылаем ему код подтверждения."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = get_confirmation_code(user.email,
                                                  user.username)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(user.username,
                  f'Ваш код подтверждения: {confirmation_code}',
                  settings.SERVER_EMAIL,
                  [user.email, ],
                  fail_silently=False,)
        return Response(request.data,
                        status=status.HTTP_200_OK)


class TokenApiView(APIView):
    """Авторизуем пользователя и выдаем токен."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.TokenSerializator(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'])
        token = RefreshToken.for_user(user)
        token.payload.update({
            'user_id': user.id,
            'username': user.username
        })
        return Response({'confirmation_code': str(token.access_token)},
                        status=status.HTTP_201_CREATED)
    

class UsersViewSet(viewsets.ModelViewSet):
    """Позволяет админу работать с пользователями."""
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer
    permission_classes = IsAdminPermission,
    filter_backends = filters.SearchFilter,
    search_fields = 'username',
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    pagination_class = CustomPaginator

    @action(detail=True, methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        """Позволяет пользователю изменить свои данные."""
        user = request.user
        if request.method == 'GET':
            serializer = serializers.MeSerializer(user)
            return Response(serializer.data)
        serializer = serializers.MeSerializer(user, data=request.data,
                                              partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

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
