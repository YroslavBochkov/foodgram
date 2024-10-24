from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from recipes.models import Favorite, Recipe
from users.models import CustomUser, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомного пользователя."""
    list_display = (
        'email',
        'username',
        'is_active',
        'is_staff',
        'is_superuser',
        'subscriptions_count',
        'recipes_count',
        'favorited_recipes_count'
    )
    search_fields = ('email', 'username')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'avatar')
        }),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_active'
            ),
        }),
    )
    ordering = ('username',)

    @admin.display(description='Количество подписок')
    def subscriptions_count(self, obj):
        """Возвращает количество подписок пользователя."""
        return Subscription.objects.filter(user=obj).count()

    @admin.display(description='Количество рецептов')
    def recipes_count(self, obj):
        """Возвращает количество рецептов пользователя."""
        return Recipe.objects.filter(author=obj).count()

    @admin.display(description='Число избранных рецептов')
    def favorited_recipes_count(self, obj):
        """Возвращает количество избранных рецептов пользователя."""
        return Favorite.objects.filter(user=obj).count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админка для подписок."""
    list_display = ('user', 'author')
