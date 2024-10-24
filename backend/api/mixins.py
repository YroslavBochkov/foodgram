from api.serializers import RecipeDemoSerializer
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import status
from rest_framework.response import Response


class AddDelMixin:
    """Миксин для добавления и удаления объектов."""

    def handle_add_remove(self, request, pk, model):
        """Обрабатывает добавление или удаление объекта."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'DELETE':
            try:
                item = model.objects.get(user=user, recipe=recipe)
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except model.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        _, created = model.objects.get_or_create(user=user, recipe=recipe)
        if created:
            serializer = RecipeDemoSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
