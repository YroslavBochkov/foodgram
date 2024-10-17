from django.conf import settings
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import IngredientItem, RecipeTag, Dish, FavoriteRecipe, ShoppingList, DishIngredient
from rest_framework import filters, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import get_confirmation_code
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers
from .paginators import CustomPaginator
from .permissions import (IsAdminAuthorOrReadOnly, IsAdminOrReadOnlyPermission)
from .filters import IngredientItemFilter, RecipeFilter

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
    permission_classes = IsAdminAuthorOrReadOnly,
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


class IngredientItemViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели ингредиента."""
    queryset = IngredientItem.objects.all()
    serializer_class = serializers.IngredientItemSerializer
    permission_classes = (IsAdminOrReadOnlyPermission)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientItemFilter


class RecipeTagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели тега."""
    queryset = RecipeTag.objects.all()
    serializer_class = serializers.RecipeTagSerializer
    permission_classes = (IsAdminOrReadOnlyPermission)  # Доступ для всех пользователей


class DishViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели рецепта."""
    queryset = Dish.objects.all()
    serializer_class = serializers.DishSerializer
    permission_classes = (permissions.IsAuthenticated,)  # Доступ только для аутентифицированных пользователей
    filter_backends = (DjangoFilterBackend,)  # Фильтрация
    filterset_class = RecipeFilter  # Убедитесь, что у вас есть фильтр для рецептов

    def perform_create(self, serializer):
        """Сохраняем рецепт с текущим пользователем как автором."""
        serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        """Возвращает соответствующий сериализатор в зависимости от метода запроса."""
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.RecipeReadSerializer
        return serializers.RecipeWriteSerializer

    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        """Метод для добавления/удаления рецепта в избранное."""
        recipe = get_object_or_404(Dish, pk=pk)
        if request.method == 'POST':
            favorite, created = FavoriteRecipe.objects.get_or_create(user=request.user, dish=recipe)
            if created:
                return Response({'detail': 'Рецепт добавлен в избранное.'}, status=201)
            return Response({'detail': 'Рецепт уже в избранном.'}, status=400)
        else:
            favorite = get_object_or_404(FavoriteRecipe, user=request.user, dish=recipe)
            favorite.delete()
            return Response({'detail': 'Рецепт удален из избранного.'}, status=204)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """Метод для добавления/удаления рецепта из списка покупок."""
        recipe = get_object_or_404(Dish, pk=pk)
        if request.method == 'POST':
            ShoppingList.objects.get_or_create(user=request.user, dish=recipe)
            return Response({'detail': 'Рецепт добавлен в список покупок.'}, status=201)
        else:
            shopping_list_item = get_object_or_404(ShoppingList, user=request.user, dish=recipe)
            shopping_list_item.delete()
            return Response({'detail': 'Рецепт удален из списка покупок.'}, status=204)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        """Метод для скачивания списка покупок."""
        user = request.user
        if not user.shopping_lists.exists():
            return Response({'detail': 'Список покупок пуст.'}, status=400)

        ingredients = DishIngredient.objects.filter(
            dish__in=user.shopping_lists.values_list('dish', flat=True)
        ).values(
            'ingredient__title',
            'ingredient__unit_of_measurement'
        ).annotate(amount=Sum('quantity'))

        shopping_list = '\n'.join([
            f"{ingredient['ingredient__title']} - {ingredient['amount']} {ingredient['ingredient__unit_of_measurement']}"
            for ingredient in ingredients
        ])

        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
        return response